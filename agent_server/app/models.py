from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    message: str = Field(min_length=1, max_length=6000)
    include_web: bool = True
    speak: bool = False


class ProfileCreate(BaseModel):
    profile_id: str = Field(min_length=1, max_length=96, pattern=r"^[a-zA-Z0-9_-]+$")
    display_name: str = Field(min_length=1, max_length=96)
    consented: bool = False
    preferences: dict[str, Any] = Field(default_factory=dict)


class ProfileResponse(BaseModel):
    profile_id: str
    display_name: str
    consented: bool
    preferences: dict[str, Any]
    created_at: datetime


class ActionProposalRequest(BaseModel):
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    action_type: Literal["message", "booking", "file_transfer", "location_share", "device_control"]
    summary: str = Field(min_length=1, max_length=800)
    payload: dict[str, Any] = Field(default_factory=dict)
    rule_id: str | None = Field(default=None, max_length=96)


class ActionConfirmation(BaseModel):
    confirmation_phrase: str = Field(min_length=2, max_length=160)


class ActionResponse(BaseModel):
    action_id: str
    action_type: str
    summary: str
    status: str
    requires_confirmation: bool
    reason: str
    expires_at: datetime | None = None


class ActionRuleCreate(BaseModel):
    rule_id: str = Field(min_length=1, max_length=96, pattern=r"^[a-zA-Z0-9_-]+$")
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    action_type: Literal["file_transfer", "location_share", "device_control"]
    display_name: str = Field(min_length=1, max_length=120)
    allowed_targets: list[str] = Field(min_length=1, max_length=32)
    expires_at: datetime | None = None
    enabled: bool = True


class SkillStateUpdate(BaseModel):
    enabled: bool


class DriveImportRequest(BaseModel):
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    relative_path: str = Field(min_length=1, max_length=512)
    remember_excerpt: bool = False


class TaskPlanRequest(BaseModel):
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    request: str = Field(min_length=3, max_length=4000)


class VaultSaveRequest(BaseModel):
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=12000)
    category: str = Field(default="saved", min_length=1, max_length=64)


class EnrollmentImageRequest(BaseModel):
    image_data_url: str = Field(min_length=32, max_length=2_800_000)
    consented: bool
    label: str = Field(default="Galaxy Book explicit profile enrollment", max_length=160)


class MediaCaptureRequest(BaseModel):
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    kind: Literal["camera", "microphone"]
    consented: bool
    label: str = Field(default="", max_length=160)


class MemoryCreate(BaseModel):
    profile_id: str = Field(default="owner", min_length=1, max_length=96)
    content: str = Field(min_length=1, max_length=4000)
    category: str = Field(default="note", min_length=1, max_length=64)
    importance: int = Field(default=2, ge=1, le=5)
