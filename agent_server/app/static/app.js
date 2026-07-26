const $ = (selector) => document.querySelector(selector);

const state = {
  activeProfile: "owner",
  speakingReplies: false,
  isBusy: false,
  lastAssistantReply: "",
  cameraStream: null,
  wakeWordEnabled: false,
  wakeRecognition: null,
  wakePhrase: "jarvis",
};

const elements = {
  chat: $("#chat"),
  welcome: $("#welcomeCard"),
  form: $("#chatForm"),
  input: $("#messageInput"),
  send: $("#sendButton"),
  web: $("#webToggle"),
  status: $("#statusLine"),
  profiles: $("#profileSelect"),
  health: $("#healthDot"),
  skills: $("#skillsList"),
  sidePanel: $("#sidePanel"),
  scrim: $("#panelScrim"),
  profileDialog: $("#profileDialog"),
  profileForm: $("#profileForm"),
  profileName: $("#profileName"),
  profileId: $("#profileId"),
  profileConsent: $("#profileConsent"),
  cameraDialog: $("#cameraDialog"),
  cameraPreview: $("#cameraPreview"),
  cameraCanvas: $("#cameraCanvas"),
  cameraHint: $("#cameraHint"),
  cameraStart: $("#startCameraButton"),
  cameraStop: $("#stopCameraButton"),
  wakeWord: $("#wakeWordButton"),
  cameraCapture: $("#captureCameraButton"),
  enrollmentConsent: $("#enrollmentConsent"),
  enrollCamera: $("#enrollCameraButton"),
  driveStatus: $("#driveStatus"),
  driveFiles: $("#driveFiles"),
};

function setStatus(message) {
  elements.status.textContent = message;
}

function setBusy(busy) {
  state.isBusy = busy;
  elements.send.disabled = busy;
  elements.input.disabled = busy;
  elements.send.textContent = busy ? "…" : "↑";
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) {
    const detail = typeof payload === "object" ? payload.detail : payload;
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return payload;
}

function scrollToEnd() {
  requestAnimationFrame(() => window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" }));
}

function createMessage(role, content = "") {
  const node = $("#messageTemplate").content.firstElementChild.cloneNode(true);
  node.classList.add(role === "user" ? "is-user" : "is-assistant");
  node.querySelector(".message-label").textContent = role === "user" ? "YOU" : "JARVIS";
  node.querySelector(".message-body").textContent = content;
  elements.chat.appendChild(node);
  scrollToEnd();
  return node;
}

function addSources(messageNode, sources) {
  if (!sources?.length) return;
  const wrap = document.createElement("section");
  wrap.className = "sources";
  const heading = document.createElement("h4");
  heading.textContent = "SOURCES";
  wrap.appendChild(heading);
  sources.forEach((source) => {
    const link = document.createElement("a");
    link.className = "source-card";
    link.href = source.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = `[${source.number}] ${source.title || "Untitled source"}`;
    if (source.snippet) {
      const snippet = document.createElement("span");
      snippet.textContent = source.snippet;
      link.appendChild(snippet);
    }
    wrap.appendChild(link);
  });
  messageNode.appendChild(wrap);
}

function autosize() {
  elements.input.style.height = "auto";
  elements.input.style.height = `${Math.min(elements.input.scrollHeight, 130)}px`;
}

async function submitMessage(message = elements.input.value.trim()) {
  if (!message || state.isBusy) return;
  elements.welcome.hidden = true;
  createMessage("user", message);
  elements.input.value = "";
  autosize();
  setBusy(true);
  setStatus("Connecting to Jarvis…");
  const assistantNode = createMessage("assistant", "");
  const body = assistantNode.querySelector(".message-body");
  let sourceData = [];
  let fullAnswer = "";

  try {
    const response = await fetch("/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        profile_id: state.activeProfile,
        message,
        include_web: elements.web.checked,
        speak: state.speakingReplies,
      }),
    });
    if (!response.ok || !response.body) {
      throw new Error(`Chat service failed (${response.status})`);
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const rows = buffer.split("\n");
      buffer = rows.pop() || "";
      for (const row of rows) {
        if (!row.trim()) continue;
        handleChatEvent(JSON.parse(row), body, assistantNode, (answer) => { fullAnswer = answer; }, (sources) => { sourceData = sources; });
      }
    }
    if (buffer.trim()) {
      handleChatEvent(JSON.parse(buffer), body, assistantNode, (answer) => { fullAnswer = answer; }, (sources) => { sourceData = sources; });
    }
    if (sourceData.length) addSources(assistantNode, sourceData);
    state.lastAssistantReply = fullAnswer || body.textContent.trim();
    if (state.speakingReplies && state.lastAssistantReply) speak(state.lastAssistantReply);
    setStatus("Ready");
  } catch (error) {
    body.textContent = `I could not complete that request: ${error.message}`;
    setStatus("Connection issue");
  } finally {
    setBusy(false);
    scrollToEnd();
  }
}

function handleChatEvent(event, body, node, setAnswer, setSources) {
  if (event.type === "status") {
    setStatus(event.message);
  } else if (event.type === "token") {
    body.textContent += event.text;
    scrollToEnd();
  } else if (event.type === "sources") {
    setSources(event.sources || []);
  } else if (event.type === "error") {
    body.textContent += `\n\n${event.message}`;
    setStatus("Request finished with an issue");
  } else if (event.type === "done") {
    setAnswer(event.answer || body.textContent);
  }
}

function speak(text) {
  if (!("speechSynthesis" in window)) {
    setStatus("This browser does not provide text-to-speech.");
    return;
  }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text.slice(0, 7000));
  utterance.rate = 1;
  utterance.pitch = 1;
  window.speechSynthesis.speak(utterance);
}

function updateWakeWordButton() {
  elements.wakeWord.textContent = `Wake word: ${state.wakeWordEnabled ? "On" : "Off"}`;
  elements.wakeWord.setAttribute("aria-pressed", String(state.wakeWordEnabled));
}

function stopWakeWord() {
  state.wakeWordEnabled = false;
  const recognition = state.wakeRecognition;
  state.wakeRecognition = null;
  if (recognition) {
    recognition.onend = null;
    try { recognition.stop(); } catch { /* Already stopped. */ }
  }
  updateWakeWordButton();
}

function startWakeWord() {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    setStatus("Wake-word listening is not supported by this browser. Use the talk button instead.");
    return;
  }
  const recognition = new Recognition();
  recognition.lang = navigator.language || "en-AU";
  recognition.interimResults = true;
  recognition.continuous = true;
  state.wakeWordEnabled = true;
  state.wakeRecognition = recognition;
  updateWakeWordButton();
  setStatus(`Wake-word listener is visibly on. Say ${state.wakePhrase} to prepare a message; it cannot send or control anything.`);
  recognition.onresult = (event) => {
    for (let index = event.resultIndex; index < event.results.length; index += 1) {
      const transcript = event.results[index][0].transcript.trim();
      if (transcript.toLowerCase().includes(state.wakePhrase)) {
        setStatus(`${state.wakePhrase[0].toUpperCase()}${state.wakePhrase.slice(1)} heard. Tap talk or type your request; no action has been performed.`);
        break;
      }
    }
  };
  recognition.onerror = (event) => {
    if (event.error === "not-allowed" || event.error === "service-not-allowed") {
      setStatus("Wake-word microphone permission was not granted.");
      stopWakeWord();
    } else {
      setStatus(`Wake-word listener issue: ${event.error}`);
    }
  };
  recognition.onend = () => {
    if (!state.wakeWordEnabled || state.wakeRecognition !== recognition) return;
    window.setTimeout(() => {
      if (state.wakeWordEnabled && state.wakeRecognition === recognition) {
        try { recognition.start(); } catch { /* Browser may be restarting the recognizer. */ }
      }
    }, 250);
  };
  try {
    recognition.start();
  } catch (error) {
    setStatus(`Could not start wake-word listening: ${error.message}`);
    stopWakeWord();
  }
}

function toggleWakeWord() {
  if (state.wakeWordEnabled) stopWakeWord();
  else startWakeWord();
}

function startRecognition() {
  if (state.wakeWordEnabled) stopWakeWord();
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    setStatus("Speech recognition is not supported by this browser. You can still type or use text-to-speech.");
    return;
  }
  const recognition = new Recognition();
  recognition.lang = navigator.language || "en-AU";
  recognition.interimResults = true;
  recognition.continuous = false;
  let finalText = "";
  setStatus("Listening… speak now.");
  $("#voiceButton").classList.add("is-listening");
  recognition.onresult = (event) => {
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      if (event.results[i].isFinal) finalText += event.results[i][0].transcript;
      else interim += event.results[i][0].transcript;
    }
    elements.input.value = `${finalText} ${interim}`.trim();
    autosize();
  };
  recognition.onerror = (event) => setStatus(`Voice input issue: ${event.error}`);
  recognition.onend = () => {
    $("#voiceButton").classList.remove("is-listening");
    if (finalText.trim()) setStatus("Voice input ready. Tap send when you are ready.");
    else if (elements.status.textContent === "Listening… speak now.") setStatus("Ready");
  };
  recognition.start();
}

async function refreshHealth() {
  try {
    const health = await api("/health");
    const ok = health.ollama?.reachable;
    elements.health.classList.toggle("is-pending", false);
    elements.health.classList.toggle("is-down", !ok);
    elements.health.title = ok ? "Local model service is reachable" : "Local model service needs attention";
    if (!ok) setStatus("Local model is not yet reachable. Check the Docker host and Ollama settings.");
  } catch {
    elements.health.classList.remove("is-pending");
    elements.health.classList.add("is-down");
    elements.health.title = "Agent server is unavailable";
  }
}

async function loadProfiles() {
  const profiles = await api("/api/profiles");
  elements.profiles.replaceChildren();
  profiles.forEach((profile) => {
    const option = document.createElement("option");
    option.value = profile.profile_id;
    option.textContent = profile.display_name;
    elements.profiles.appendChild(option);
  });
  if (!profiles.some((profile) => profile.profile_id === state.activeProfile)) state.activeProfile = profiles[0]?.profile_id || "owner";
  elements.profiles.value = state.activeProfile;
}

async function loadSkills() {
  const { skills } = await api("/api/skills");
  elements.skills.replaceChildren();
  skills.forEach((skill) => {
    const card = document.createElement("article");
    card.className = "skill";
    const top = document.createElement("div");
    top.className = "skill-top";
    const text = document.createElement("div");
    const heading = document.createElement("h3");
    heading.textContent = skill.display_name;
    const category = document.createElement("small");
    category.textContent = `${skill.category}${skill.requires_configuration ? " · setup required" : ""}`;
    text.append(heading, category);
    const switchLabel = document.createElement("label");
    switchLabel.className = "switch";
    switchLabel.title = `Enable ${skill.display_name}`;
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = skill.enabled;
    input.addEventListener("change", async () => {
      input.disabled = true;
      try {
        await api(`/api/skills/${encodeURIComponent(skill.skill_id)}`, { method: "POST", body: JSON.stringify({ enabled: input.checked }) });
        setStatus(`${skill.display_name}: ${input.checked ? "enabled" : "disabled"}`);
      } catch (error) {
        input.checked = !input.checked;
        setStatus(error.message);
      } finally {
        input.disabled = false;
      }
    });
    const slider = document.createElement("span");
    slider.className = "slider";
    switchLabel.append(input, slider);
    top.append(text, switchLabel);
    const description = document.createElement("p");
    description.textContent = skill.description;
    card.append(top, description);
    elements.skills.appendChild(card);
  });
}

async function loadDriveFiles() {
  try {
    const response = await api("/api/google-drive/files");
    const { status, files } = response;
    elements.driveStatus.textContent = status.message;
    elements.driveFiles.replaceChildren();
    if (!status.ready) return;
    if (!files.length) {
      const empty = document.createElement("p");
      empty.className = "drive-empty";
      empty.textContent = "No supported text documents are available in the mounted Drive folder.";
      elements.driveFiles.appendChild(empty);
      return;
    }
    files.forEach((file) => {
      const row = document.createElement("article");
      row.className = "drive-file";
      const title = document.createElement("strong");
      title.textContent = file.relative_path;
      const size = document.createElement("small");
      size.textContent = `${Math.max(1, Math.ceil(file.size_bytes / 1024))} KB`;
      const rememberLabel = document.createElement("label");
      rememberLabel.className = "drive-remember";
      const remember = document.createElement("input");
      remember.type = "checkbox";
      rememberLabel.append(remember, document.createTextNode("Add excerpt to profile memory"));
      const importButton = document.createElement("button");
      importButton.type = "button";
      importButton.className = "text-button";
      importButton.textContent = "Import to active profile";
      importButton.addEventListener("click", async () => {
        importButton.disabled = true;
        try {
          await api("/api/google-drive/import", {
            method: "POST",
            body: JSON.stringify({
              profile_id: state.activeProfile,
              relative_path: file.relative_path,
              remember_excerpt: remember.checked,
            }),
          });
          setStatus(`Imported ${file.relative_path} into this profile’s private vault.`);
        } catch (error) {
          setStatus(error.message);
        } finally {
          importButton.disabled = false;
        }
      });
      row.append(title, size, rememberLabel, importButton);
      elements.driveFiles.appendChild(row);
    });
  } catch (error) {
    elements.driveStatus.textContent = `Drive mirror unavailable: ${error.message}`;
  }
}

function openPanel() {
  elements.sidePanel.classList.add("is-open");
  elements.sidePanel.setAttribute("aria-hidden", "false");
  elements.scrim.hidden = false;
}

function closePanel() {
  elements.sidePanel.classList.remove("is-open");
  elements.sidePanel.setAttribute("aria-hidden", "true");
  elements.scrim.hidden = true;
}

async function createProfile(event) {
  event.preventDefault();
  const displayName = elements.profileName.value.trim();
  const profileId = elements.profileId.value.trim();
  if (!displayName || !profileId) return;
  try {
    await api("/api/profiles", {
      method: "POST",
      body: JSON.stringify({ profile_id: profileId, display_name: displayName, consented: elements.profileConsent.checked, preferences: {} }),
    });
    state.activeProfile = profileId;
    await loadProfiles();
    elements.profileDialog.close();
    elements.profileForm.reset();
    setStatus(`Profile ${displayName} is active.`);
  } catch (error) {
    setStatus(error.message);
  }
}

async function startCamera() {
  if (!navigator.mediaDevices?.getUserMedia) {
    elements.cameraHint.textContent = "This browser does not expose camera access. Use a recent Chromium or Firefox browser over HTTPS.";
    return;
  }
  try {
    state.cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
    elements.cameraPreview.srcObject = state.cameraStream;
    elements.cameraCapture.disabled = false;
    elements.enrollCamera.disabled = !elements.enrollmentConsent.checked;
    elements.cameraHint.textContent = "Camera is on. Capture audit stores no image. Saving an enrollment photo requires the visible consent box and stores only a local profile image.";
  } catch (error) {
    elements.cameraHint.textContent = `Camera access was not granted: ${error.message}`;
  }
}

function stopCamera() {
  if (state.cameraStream) state.cameraStream.getTracks().forEach((track) => track.stop());
  state.cameraStream = null;
  elements.cameraPreview.srcObject = null;
  elements.cameraCapture.disabled = true;
  elements.enrollCamera.disabled = true;
  elements.cameraHint.textContent = "Camera is off. Start it only when you are ready.";
}

function drawCameraFrame() {
  const video = elements.cameraPreview;
  const sourceWidth = video.videoWidth || 640;
  const sourceHeight = video.videoHeight || 480;
  const scale = Math.min(1, 640 / sourceWidth, 480 / sourceHeight);
  elements.cameraCanvas.width = Math.max(1, Math.round(sourceWidth * scale));
  elements.cameraCanvas.height = Math.max(1, Math.round(sourceHeight * scale));
  elements.cameraCanvas.getContext("2d").drawImage(video, 0, 0, elements.cameraCanvas.width, elements.cameraCanvas.height);
  return elements.cameraCanvas;
}

async function captureCamera() {
  if (!state.cameraStream) return;
  drawCameraFrame();
  try {
    await api("/api/media/capture", {
      method: "POST",
      body: JSON.stringify({ profile_id: state.activeProfile, kind: "camera", consented: true, label: "Galaxy Book explicit capture" }),
    });
    elements.cameraHint.textContent = "Capture acknowledged. Image analysis/storage adapters are intentionally disabled until configured.";
  } catch (error) {
    elements.cameraHint.textContent = error.message;
  }
}

async function saveEnrollmentImage() {
  if (!state.cameraStream) {
    elements.cameraHint.textContent = "Start the camera before saving an enrollment photo.";
    return;
  }
  if (!elements.enrollmentConsent.checked) {
    elements.cameraHint.textContent = "Check the visible consent box before saving a profile enrollment photo.";
    return;
  }
  elements.enrollCamera.disabled = true;
  try {
    const imageDataUrl = drawCameraFrame().toDataURL("image/jpeg", 0.82);
    const record = await api(`/api/profiles/${encodeURIComponent(state.activeProfile)}/enrollment-image`, {
      method: "POST",
      body: JSON.stringify({ image_data_url: imageDataUrl, consented: true, label: "Galaxy Book explicit profile enrollment" }),
    });
    elements.cameraHint.textContent = `Enrollment photo saved locally for ${state.activeProfile}. No background recognition or matching was performed.`;
    setStatus(`Saved ${record.file_name} to the active profile’s local enrollment folder.`);
  } catch (error) {
    elements.cameraHint.textContent = `Enrollment image was not saved: ${error.message}`;
  } finally {
    elements.enrollCamera.disabled = !elements.enrollmentConsent.checked || !state.cameraStream;
  }
}

async function planTask() {
  const request = elements.input.value.trim();
  if (!request || state.isBusy) {
    setStatus("Type or dictate a task first, then choose Plan task.");
    return;
  }
  elements.welcome.hidden = true;
  createMessage("user", `Plan task: ${request}`);
  elements.input.value = "";
  autosize();
  setBusy(true);
  setStatus("Planning a safe next step…");
  const assistantNode = createMessage("assistant", "Planning this task…");
  const body = assistantNode.querySelector(".message-body");
  try {
    const plan = await api("/api/tasks/plan", {
      method: "POST",
      body: JSON.stringify({ profile_id: state.activeProfile, request }),
    });
    body.textContent = `TASK PLAN\n\n${plan.steps.map((step, index) => `${index + 1}. ${step}`).join("\n")}`;
    if (plan.proposal) addActionControls(assistantNode, plan.proposal, plan.note);
    else body.textContent += `\n\n${plan.note}`;
    state.lastAssistantReply = body.textContent;
    setStatus("Task plan ready.");
  } catch (error) {
    body.textContent = `I could not plan that task: ${error.message}`;
    setStatus("Task plan unavailable");
  } finally {
    setBusy(false);
    scrollToEnd();
  }
}

function addActionControls(messageNode, proposal, note = "") {
  const previous = messageNode.querySelector(".action-card");
  if (previous) previous.remove();
  const card = document.createElement("section");
  card.className = "action-card";
  const title = document.createElement("h4");
  title.textContent = "EXTERNAL ACTION";
  const summary = document.createElement("p");
  summary.textContent = proposal.summary;
  const stateText = document.createElement("p");
  stateText.className = "action-state";
  stateText.textContent = note || `Status: ${proposal.status}`;
  const controls = document.createElement("div");
  controls.className = "action-controls";
  card.append(title, summary, stateText, controls);
  messageNode.appendChild(card);

  const addButton = (label, handler) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "text-button";
    button.textContent = label;
    button.addEventListener("click", handler);
    controls.appendChild(button);
  };
  const refresh = (next, nextNote = "") => addActionControls(messageNode, next, nextNote);

  if (proposal.status === "awaiting_confirmation") {
    const typedEntry = document.createElement("div");
    typedEntry.className = "confirmation-entry";
    const phraseInput = document.createElement("input");
    phraseInput.type = "text";
    phraseInput.maxLength = 80;
    phraseInput.placeholder = "Type confirm";
    phraseInput.setAttribute("aria-label", "Type confirm to approve this action");
    const typedButton = document.createElement("button");
    typedButton.type = "button";
    typedButton.className = "text-button";
    typedButton.textContent = "Confirm typed";
    typedButton.addEventListener("click", () => confirmAction(proposal.action_id, phraseInput.value, refresh));
    typedEntry.append(phraseInput, typedButton);
    controls.appendChild(typedEntry);
    addButton("Confirm by voice", () => captureActionConfirmation(proposal.action_id, refresh));
  } else if (["confirmed", "authorized", "connector_unavailable", "execution_failed"].includes(proposal.status)) {
    addButton("Deliver to configured connector", async () => {
      try {
        const outcome = await api(`/api/actions/${encodeURIComponent(proposal.action_id)}/execute`, { method: "POST" });
        refresh(outcome.action, outcome.delivery.message || `Delivery status: ${outcome.delivery.status}`);
        setStatus(`Action delivery: ${outcome.delivery.status}`);
      } catch (error) {
        setStatus(error.message);
      }
    });
  }
}

async function confirmAction(actionId, phrase, refresh) {
  try {
    const action = await api(`/api/actions/${encodeURIComponent(actionId)}/confirm`, {
      method: "POST",
      body: JSON.stringify({ confirmation_phrase: phrase }),
    });
    refresh(action, "Confirmed. Review once more, then choose delivery to the configured connector.");
    setStatus("Action confirmed; it has not been delivered yet.");
  } catch (error) {
    setStatus(error.message);
  }
}

function captureActionConfirmation(actionId, refresh) {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    setStatus("Voice confirmation is not supported here. Use typed confirmation instead.");
    return;
  }
  const recognition = new Recognition();
  recognition.lang = navigator.language || "en-AU";
  recognition.interimResults = false;
  recognition.continuous = false;
  setStatus("Listening for confirmation. Say confirm when ready.");
  recognition.onresult = (event) => confirmAction(actionId, event.results[0][0].transcript, refresh);
  recognition.onerror = (event) => setStatus(`Voice confirmation issue: ${event.error}`);
  recognition.start();
}

async function saveLastReply() {
  if (!state.lastAssistantReply) {
    setStatus("There is no completed Jarvis reply to save yet.");
    return;
  }
  try {
    await api("/api/vault", {
      method: "POST",
      body: JSON.stringify({
        profile_id: state.activeProfile,
        title: "Saved Jarvis response",
        content: state.lastAssistantReply,
        category: "saved-responses",
      }),
    });
    setStatus("Saved to this profile’s private content folder.");
  } catch (error) {
    setStatus(error.message);
  }
}

function bindEvents() {
  elements.form.addEventListener("submit", (event) => { event.preventDefault(); submitMessage(); });
  elements.input.addEventListener("input", autosize);
  elements.profiles.addEventListener("change", () => { state.activeProfile = elements.profiles.value; setStatus("Profile changed. Memory is now separated for this person."); });
  $("#voiceButton").addEventListener("click", startRecognition);
  $("#speakToggle").addEventListener("click", (event) => {
    state.speakingReplies = !state.speakingReplies;
    event.currentTarget.textContent = `Voice replies: ${state.speakingReplies ? "On" : "Off"}`;
    event.currentTarget.setAttribute("aria-pressed", String(state.speakingReplies));
  });
  elements.wakeWord.addEventListener("click", toggleWakeWord);
  $("#saveMemoryButton").addEventListener("click", saveLastReply);
  $("#planTaskButton").addEventListener("click", planTask);
  $("#refreshDriveButton").addEventListener("click", loadDriveFiles);
  $("#menuButton").addEventListener("click", openPanel);
  $("#closePanelButton").addEventListener("click", closePanel);
  elements.scrim.addEventListener("click", closePanel);
  $("#newProfileButton").addEventListener("click", () => elements.profileDialog.showModal());
  elements.profileForm.addEventListener("submit", createProfile);
  $("#cameraButton").addEventListener("click", () => elements.cameraDialog.showModal());
  elements.cameraStart.addEventListener("click", startCamera);
  elements.cameraStop.addEventListener("click", stopCamera);
  elements.cameraCapture.addEventListener("click", captureCamera);
  elements.enrollmentConsent.addEventListener("change", () => {
    elements.enrollCamera.disabled = !elements.enrollmentConsent.checked || !state.cameraStream;
  });
  elements.enrollCamera.addEventListener("click", saveEnrollmentImage);
  elements.cameraDialog.addEventListener("close", stopCamera);
  document.querySelectorAll(".suggestion").forEach((button) => button.addEventListener("click", () => submitMessage(button.textContent)));
  window.addEventListener("beforeunload", stopWakeWord);
}

async function initialize() {
  bindEvents();
  autosize();
  try {
    await Promise.all([loadProfiles(), loadSkills(), loadDriveFiles(), refreshHealth()]);
  } catch (error) {
    setStatus(`Startup issue: ${error.message}`);
  }
  window.setInterval(refreshHealth, 30000);
}

initialize();
