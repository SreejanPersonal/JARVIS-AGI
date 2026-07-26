from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.adapters.ollama import OllamaClient
from app.adapters.searxng import SearxngClient
from app.config import get_settings
from app.db import Database
from app.models import (
    ActionConfirmation,
    ActionProposalRequest,
    ActionResponse,
    ActionRuleCreate,
    ChatRequest,
    DriveImportRequest,
    EnrollmentImageRequest,
    MediaCaptureRequest,
    MemoryCreate,
    ProfileCreate,
    ProfileResponse,
    SkillStateUpdate,
    TaskPlanRequest,
    VaultSaveRequest,
)
from app.services.actions import ActionPolicyService
from app.services.agent import AgentService
from app.services.executor import ActionExecutor
from app.services.google_drive import GoogleDriveMirror
from app.services.memory import MemoryService
from app.services.skills import SkillRegistry
from app.services.tasks import TaskPlanner
from app.services.vault import ProfileVault


settings = get_settings()
static_dir = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings.database_path)
    database.initialize(settings.owner_profile_name)
    memory = MemoryService(database, settings.max_context_chars)
    app.state.database = database
    app.state.ollama = OllamaClient(settings)
    app.state.searxng = SearxngClient(settings)
    app.state.memory = memory
    app.state.agent = AgentService(settings, database, app.state.ollama, app.state.searxng, memory)
    app.state.actions = ActionPolicyService(database)
    app.state.executor = ActionExecutor(settings, database)
    app.state.tasks = TaskPlanner(database, app.state.ollama, app.state.actions)
    app.state.skills = SkillRegistry(database)
    app.state.skills.initialize()
    app.state.vault = ProfileVault(settings)
    app.state.google_drive = GoogleDriveMirror(settings, database, app.state.vault)
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
if settings.public_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[item.strip() for item in settings.public_origin.split(",") if item.strip()],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def database(request: Request) -> Database:
    return request.app.state.database


def actions(request: Request) -> ActionPolicyService:
    return request.app.state.actions


@app.get("/health")
async def health(request: Request) -> dict:
    ollama = await request.app.state.ollama.health()
    search = await request.app.state.searxng.health()
    return {
        "status": "ok" if ollama.get("reachable") else "degraded",
        "service": settings.app_name,
        "ollama": ollama,
        "search": search,
        "database": str(settings.database_path),
    }


@app.get("/api/profiles", response_model=list[ProfileResponse])
def list_profiles(request: Request) -> list[dict]:
    return database(request).list_profiles()


@app.post("/api/profiles", response_model=ProfileResponse, status_code=201)
def create_profile(payload: ProfileCreate, request: Request) -> dict:
    try:
        profile = database(request).create_profile(
            payload.profile_id, payload.display_name, payload.consented, payload.preferences
        )
        database(request).audit("profile_created", {"display_name": payload.display_name}, payload.profile_id)
        return profile
    except Exception as error:
        raise HTTPException(status_code=409, detail=f"Could not create profile: {error}") from error


@app.get("/api/conversations/{profile_id}")
def recent_conversation(profile_id: str, request: Request) -> dict:
    if not database(request).get_profile(profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {"profile_id": profile_id, "turns": database(request).recent_turns(profile_id, limit=40)}


@app.get("/api/skills")
def list_skills(request: Request) -> dict:
    return {"skills": request.app.state.skills.list()}


@app.post("/api/skills/{skill_id}")
def set_skill_state(skill_id: str, payload: SkillStateUpdate, request: Request) -> dict:
    skill = request.app.state.skills.set_enabled(skill_id, payload.enabled)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found.")
    return skill


@app.post("/api/memories", status_code=201)
def create_memory(payload: MemoryCreate, request: Request) -> dict:
    if not database(request).get_profile(payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    memory = request.app.state.memory.remember(payload.profile_id, payload.content, payload.category, payload.importance)
    database(request).audit("memory_saved", {"memory_id": memory["memory_id"], "category": payload.category}, payload.profile_id)
    return memory


@app.post("/api/vault", status_code=201)
def save_to_vault(payload: VaultSaveRequest, request: Request) -> dict:
    if not database(request).get_profile(payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    record = request.app.state.vault.save_text(payload.profile_id, payload.title, payload.content, payload.category)
    database(request).audit("vault_item_saved", record, payload.profile_id)
    return record


@app.get("/api/vault/{profile_id}")
def list_vault(profile_id: str, request: Request) -> dict:
    if not database(request).get_profile(profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {"profile_id": profile_id, "files": request.app.state.vault.list_files(profile_id)}


@app.get("/api/google-drive")
def google_drive_status(request: Request) -> dict:
    return request.app.state.google_drive.status()


@app.get("/api/google-drive/files")
def list_google_drive_files(request: Request) -> dict:
    drive = request.app.state.google_drive
    return {"status": drive.status(), "files": drive.list_files()}


@app.post("/api/google-drive/import", status_code=201)
def import_google_drive_file(payload: DriveImportRequest, request: Request) -> dict:
    try:
        return request.app.state.google_drive.import_file(
            payload.profile_id, payload.relative_path, payload.remember_excerpt
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/chat/stream")
async def chat_stream(payload: ChatRequest, request: Request) -> StreamingResponse:
    async def events() -> AsyncIterator[str]:
        async for event in request.app.state.agent.stream_chat(payload.profile_id, payload.message, payload.include_web):
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(events(), media_type="application/x-ndjson", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/tasks/plan")
async def plan_task(payload: TaskPlanRequest, request: Request) -> dict:
    try:
        return await request.app.state.tasks.plan(payload.profile_id, payload.request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/action-rules", status_code=201)
def create_action_rule(payload: ActionRuleCreate, request: Request) -> dict:
    try:
        return actions(request).create_rule(
            payload.rule_id,
            payload.profile_id,
            payload.action_type,
            payload.display_name,
            payload.allowed_targets,
            payload.expires_at,
            payload.enabled,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/actions/propose", response_model=ActionResponse, status_code=201)
def propose_action(payload: ActionProposalRequest, request: Request) -> dict:
    try:
        return actions(request).propose(
            payload.profile_id, payload.action_type, payload.summary, payload.payload, payload.rule_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/actions/{action_id}/confirm", response_model=ActionResponse)
def confirm_action(action_id: str, payload: ActionConfirmation, request: Request) -> dict:
    try:
        return actions(request).confirm(action_id, payload.confirmation_phrase)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/actions/{action_id}/execute")
async def execute_action(action_id: str, request: Request) -> dict:
    try:
        return await request.app.state.executor.execute(action_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/profiles/{profile_id}/enrollment-image", status_code=201)
def save_enrollment_image(profile_id: str, payload: EnrollmentImageRequest, request: Request) -> dict:
    profile = database(request).get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    if not profile["consented"] or not payload.consented:
        raise HTTPException(status_code=400, detail="A consenting profile and explicit capture consent are required.")
    try:
        record = request.app.state.vault.save_enrollment_image(profile_id, payload.image_data_url, payload.label)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    database(request).audit("profile_enrollment_image_saved", record, profile_id)
    return {
        **record,
        "message": "Enrollment image stored locally for this consenting profile. No recognition or background matching was performed.",
    }


@app.post("/api/media/capture", status_code=202)
def record_media_capture(payload: MediaCaptureRequest, request: Request) -> dict:
    if not payload.consented:
        raise HTTPException(status_code=400, detail="Explicit browser consent is required before media input is recorded.")
    if not database(request).get_profile(payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    database(request).audit("media_capture_authorized", {"kind": payload.kind, "label": payload.label}, payload.profile_id)
    return {"accepted": True, "message": "Media permission state was recorded. Raw media upload is disabled until a dedicated opt-in adapter is configured."}


@app.get("/", include_in_schema=False)
def kiosk() -> FileResponse:
    return FileResponse(static_dir / "index.html")
