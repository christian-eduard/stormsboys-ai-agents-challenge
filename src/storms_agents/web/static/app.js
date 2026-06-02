const state = {
  characters: [],
  demoUsers: [],
  language: "en",
  marketplace: null,
  session: null,
};

const els = {
  bookTitle: document.querySelector("#bookTitle"),
  bookSummary: document.querySelector("#bookSummary"),
  characterCount: document.querySelector("#characterCount"),
  placeCount: document.querySelector("#placeCount"),
  sceneCount: document.querySelector("#sceneCount"),
  characterSelect: document.querySelector("#characterSelect"),
  modeSelect: document.querySelector("#modeSelect"),
  languageSelect: document.querySelector("#languageSelect"),
  userSelect: document.querySelector("#userSelect"),
  loginButton: document.querySelector("#loginButton"),
  logoutButton: document.querySelector("#logoutButton"),
  activeUser: document.querySelector("#activeUser"),
  questionInput: document.querySelector("#questionInput"),
  askCharacter: document.querySelector("#askCharacter"),
  askFuture: document.querySelector("#askFuture"),
  characterResponse: document.querySelector("#characterResponse"),
  scenePrompt: document.querySelector("#scenePrompt"),
  runScene: document.querySelector("#runScene"),
  sceneResponse: document.querySelector("#sceneResponse"),
  narrationInput: document.querySelector("#narrationInput"),
  runNarration: document.querySelector("#runNarration"),
  narrationResponse: document.querySelector("#narrationResponse"),
  runPublisher: document.querySelector("#runPublisher"),
  publisherMetrics: document.querySelector("#publisherMetrics"),
  publisherResponse: document.querySelector("#publisherResponse"),
  publisherAccess: document.querySelector("#publisherAccess"),
  refreshAdmin: document.querySelector("#refreshAdmin"),
  roleList: document.querySelector("#roleList"),
  marketplaceSummary: document.querySelector("#marketplaceSummary"),
  adminAccess: document.querySelector("#adminAccess"),
  catalogList: document.querySelector("#catalogList"),
  runEvaluation: document.querySelector("#runEvaluation"),
  evaluationResults: document.querySelector("#evaluationResults"),
  traceList: document.querySelector("#traceList"),
  refreshDemo: document.querySelector("#refreshDemo"),
  runtimeStatus: document.querySelector(".status-panel p"),
  runtimeGemini: document.querySelector("#runtimeGemini"),
  runtimeStorage: document.querySelector("#runtimeStorage"),
  runtimeSeed: document.querySelector("#runtimeSeed"),
  runtimeRetrieval: document.querySelector("#runtimeRetrieval"),
};

const copy = {
  en: {
    "nav.reader": "Reader",
    "nav.agents": "Agents",
    "nav.publisher": "Publisher",
    "nav.admin": "Admin",
    "nav.evaluation": "Evaluation",
    "nav.runtime": "Runtime",
    "nav.architecture": "Architecture",
    "status.track": "Marketplace refactor",
    "login.eyebrow": "Demo access",
    "login.account": "Account",
    "login.signIn": "Sign in",
    "login.signOut": "Sign out",
    "login.none": "Not signed in",
    "login.active": "Signed in as",
    "login.required": "Sign in with a demo account to use role-based access.",
    "login.publisherRequired": "Publisher Admin or Super Admin access required.",
    "login.superRequired": "Super Admin access required.",
    "login.allowed": "Access granted",
    "top.eyebrow": "Judge demo",
    "top.title": "Multi-agent literary intelligence",
    "book.eyebrow": "Demo book",
    "metrics.characters": "Characters",
    "metrics.places": "Places",
    "metrics.scenes": "Scenes",
    "character.eyebrow": "Character Agent",
    "character.title": "Grounded character chat",
    "character.prompt": "Prompt",
    "character.ask": "Ask character",
    "character.future": "Out-of-canon test",
    "scene.eyebrow": "Scene Orchestrator",
    "scene.title": "Multi-character response",
    "scene.prompt": "Scene prompt",
    "scene.run": "Run scene",
    "voice.eyebrow": "Voice / Narration Agent",
    "voice.title": "Scene narration plan",
    "voice.prepare": "Prepare",
    "voice.sceneText": "Scene text",
    "publisher.eyebrow": "Publisher Insights Agent",
    "publisher.title": "Admin value view",
    "publisher.analyze": "Analyze",
    "publisher.engagement": "Engagement",
    "publisher.quality": "Quality",
    "admin.eyebrow": "Marketplace Admin",
    "admin.title": "Roles and operations",
    "admin.refresh": "Refresh",
    "admin.running": "Loading roles and marketplace operations.",
    "admin.permissions": "Permissions",
    "admin.marketplaceStatus": "Marketplace status",
    "marketplace.eyebrow": "Track 3 readiness",
    "marketplace.title": "Publisher catalog console",
    "marketplace.catalog": "Catalog",
    "marketplace.operations": "Operations",
    "evaluation.eyebrow": "Track 2 evidence",
    "evaluation.title": "Before / after evaluation",
    "evaluation.run": "Run",
    "trace.eyebrow": "Observability",
    "trace.title": "Agent trace",
    "runtime.eyebrow": "Runtime proof",
    "runtime.title": "Google Cloud services",
    "runtime.seed": "Demo book seed",
    "runtime.retrieval": "Retrieval path",
    "architecture.eyebrow": "Google Cloud target",
    "character.initial": "Select a character and run the demo prompt.",
    "character.running": "Running retrieval, character response, and consistency check.",
    "scene.running": "Coordinating scene agents.",
    "voice.running": "Preparing narration handoff.",
    "publisher.running": "Generating publisher insights.",
    "evaluation.running": "Running before and after evaluation.",
    "labels.fictionBranch": "Fiction branch",
    "labels.consistency": "Consistency",
    "labels.passed": "passed",
    "labels.needsReview": "needs review",
    "labels.language": "Language",
    questionDefault: "Why do you attack the windmills?",
    futureDefault: "Tell me what happens ten years after the ending.",
    sceneDefault: "Discuss whether the windmills are giants or only windmills.",
    narrationDefault: "Don Quijote charges at the windmills while Sancho warns him from the road.",
  },
  es: {
    "nav.reader": "Lector",
    "nav.agents": "Agentes",
    "nav.publisher": "Editorial",
    "nav.admin": "Admin",
    "nav.evaluation": "Evaluacion",
    "nav.runtime": "Runtime",
    "nav.architecture": "Arquitectura",
    "status.track": "Refactor Marketplace",
    "login.eyebrow": "Acceso demo",
    "login.account": "Cuenta",
    "login.signIn": "Entrar",
    "login.signOut": "Salir",
    "login.none": "Sin sesion iniciada",
    "login.active": "Sesion iniciada como",
    "login.required": "Inicia sesion con una cuenta demo para usar accesos por rol.",
    "login.publisherRequired": "Se requiere Publisher Admin o Super Admin.",
    "login.superRequired": "Se requiere Super Admin.",
    "login.allowed": "Acceso concedido",
    "top.eyebrow": "Demo para jueces",
    "top.title": "Inteligencia literaria multiagente",
    "book.eyebrow": "Libro demo",
    "metrics.characters": "Personajes",
    "metrics.places": "Lugares",
    "metrics.scenes": "Escenas",
    "character.eyebrow": "Agente de personaje",
    "character.title": "Chat fundamentado con personaje",
    "character.prompt": "Pregunta",
    "character.ask": "Preguntar",
    "character.future": "Prueba fuera de canon",
    "scene.eyebrow": "Orquestador de escena",
    "scene.title": "Respuesta multipersonaje",
    "scene.prompt": "Prompt de escena",
    "scene.run": "Ejecutar escena",
    "voice.eyebrow": "Agente de voz / narracion",
    "voice.title": "Plan de narracion de escena",
    "voice.prepare": "Preparar",
    "voice.sceneText": "Texto de escena",
    "publisher.eyebrow": "Agente de insights editoriales",
    "publisher.title": "Vista de valor admin",
    "publisher.analyze": "Analizar",
    "publisher.engagement": "Engagement",
    "publisher.quality": "Calidad",
    "admin.eyebrow": "Admin Marketplace",
    "admin.title": "Roles y operaciones",
    "admin.refresh": "Actualizar",
    "admin.running": "Cargando roles y operacion Marketplace.",
    "admin.permissions": "Permisos",
    "admin.marketplaceStatus": "Estado Marketplace",
    "marketplace.eyebrow": "Preparacion Track 3",
    "marketplace.title": "Consola de catalogo editorial",
    "marketplace.catalog": "Catalogo",
    "marketplace.operations": "Operaciones",
    "evaluation.eyebrow": "Evidencia Track 2",
    "evaluation.title": "Evaluacion antes / despues",
    "evaluation.run": "Ejecutar",
    "trace.eyebrow": "Observabilidad",
    "trace.title": "Traza de agentes",
    "runtime.eyebrow": "Prueba de runtime",
    "runtime.title": "Servicios Google Cloud",
    "runtime.seed": "Libro demo cargado",
    "runtime.retrieval": "Ruta de recuperacion",
    "architecture.eyebrow": "Objetivo Google Cloud",
    "character.initial": "Selecciona un personaje y ejecuta la pregunta demo.",
    "character.running": "Ejecutando recuperacion, respuesta del personaje y control de consistencia.",
    "scene.running": "Coordinando agentes de escena.",
    "voice.running": "Preparando entrega a narracion.",
    "publisher.running": "Generando insights para editorial.",
    "evaluation.running": "Ejecutando evaluacion antes y despues.",
    "labels.fictionBranch": "Rama de ficcion",
    "labels.consistency": "Consistencia",
    "labels.passed": "aprobada",
    "labels.needsReview": "requiere revision",
    "labels.language": "Idioma",
    questionDefault: "Por que atacas los molinos?",
    futureDefault: "Cuentame que ocurre diez anos despues del final.",
    sceneDefault: "Debatid si los molinos son gigantes o solo molinos.",
    narrationDefault: "Don Quijote carga contra los molinos mientras Sancho le advierte desde el camino.",
  },
};

function t(key) {
  return copy[state.language][key] ?? copy.en[key] ?? key;
}

function applyLanguage(language) {
  const previousCopy = copy[state.language];
  state.language = language;
  document.documentElement.lang = language;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  if (!els.questionInput.value || els.questionInput.value === previousCopy.questionDefault) {
    els.questionInput.value = t("questionDefault");
  }
  if (!els.scenePrompt.value || els.scenePrompt.value === previousCopy.sceneDefault) {
    els.scenePrompt.value = t("sceneDefault");
  }
  if (!els.narrationInput.value || els.narrationInput.value === previousCopy.narrationDefault) {
    els.narrationInput.value = t("narrationDefault");
  }
  if (els.characterResponse.textContent.trim() === previousCopy["character.initial"]) {
    els.characterResponse.textContent = t("character.initial");
  }
  renderSession();
  applyAccess();
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "content-type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

async function loadAuth() {
  const data = await api("/api/v1/auth/demo-users");
  state.demoUsers = data.users;
  els.userSelect.innerHTML = "";
  data.users.forEach((user) => {
    const option = document.createElement("option");
    option.value = user.user_id;
    option.textContent = `${user.name} (${user.role})`;
    els.userSelect.appendChild(option);
  });
  const savedSession = localStorage.getItem("stormsboys-demo-session");
  if (savedSession) {
    state.session = JSON.parse(savedSession);
    els.userSelect.value = state.session.user.user_id;
  }
  renderSession();
  applyAccess();
}

async function login() {
  const data = await api("/api/v1/auth/demo-login", {
    method: "POST",
    body: JSON.stringify({ user_id: els.userSelect.value }),
  });
  state.session = data;
  localStorage.setItem("stormsboys-demo-session", JSON.stringify(data));
  renderSession();
  applyAccess();
}

function logout() {
  state.session = null;
  localStorage.removeItem("stormsboys-demo-session");
  renderSession();
  applyAccess();
}

function renderSession() {
  if (!state.session) {
    els.activeUser.textContent = t("login.none");
    els.activeUser.className = "active-user";
    return;
  }
  const { user } = state.session;
  els.activeUser.textContent = `${t("login.active")} ${user.name} | ${user.role}`;
  els.activeUser.className = "active-user signed-in";
}

function hasPermission(permission) {
  return Boolean(state.session?.user?.permissions?.includes(permission));
}

function applyAccess() {
  const canPublish = hasPermission("manage_catalog") || hasPermission("manage_tenants");
  const canOperate = hasPermission("manage_tenants");
  els.runPublisher.disabled = !canPublish;
  els.refreshAdmin.disabled = !canPublish;
  els.publisherAccess.textContent = canPublish
    ? `${t("login.allowed")}: publisher catalog`
    : state.session
      ? t("login.publisherRequired")
      : t("login.required");
  els.adminAccess.textContent = canOperate
    ? `${t("login.allowed")}: platform operations`
    : state.session
      ? t("login.superRequired")
      : t("login.required");
  els.publisherAccess.className = canPublish ? "access-box granted" : "access-box locked";
  els.adminAccess.className = canOperate ? "access-box granted" : "access-box locked";
  if (state.marketplace) {
    renderMarketplace(state.marketplace);
  }
}

function renderTraces(traces = []) {
  els.traceList.innerHTML = "";
  traces.forEach((trace) => {
    const item = document.createElement("article");
    item.className = "trace-item";
    item.innerHTML = `
      <div>
        <strong>${trace.agent_name}</strong>
        <p>${trace.operation}</p>
      </div>
      <span>${trace.latency_ms ?? 0} ms</span>
    `;
    els.traceList.appendChild(item);
  });
  const retrievalTrace = traces.find((trace) => trace.agent_name === "RetrievalAgent");
  if (retrievalTrace) {
    els.runtimeRetrieval.textContent = retrievalTrace.operation.replace("retrieval.", "");
  }
}

function renderCharacters(characters) {
  els.characterSelect.innerHTML = "";
  characters.forEach((character) => {
    const option = document.createElement("option");
    option.value = character.character_id;
    option.textContent = character.name;
    els.characterSelect.appendChild(option);
  });
}

async function loadBook() {
  await loadAuth();
  await loadCapabilities();
  await loadStorage();
  await loadAdmin();
  const data = await api("/api/v1/demo/book");
  state.characters = data.analysis.characters;
  els.bookTitle.textContent = data.title;
  els.bookSummary.textContent = data.analysis.summary;
  els.characterCount.textContent = data.analysis.characters.length;
  els.placeCount.textContent = data.analysis.places.length;
  els.sceneCount.textContent = data.analysis.scenes.length;
  renderCharacters(state.characters);
  renderTraces(data.traces);
}

async function loadAdmin() {
  els.roleList.textContent = t("admin.running");
  els.marketplaceSummary.textContent = t("admin.running");
  const [roles, marketplace] = await Promise.all([
    api("/api/v1/admin/roles"),
    api("/api/v1/admin/marketplace"),
  ]);
  state.marketplace = marketplace;
  renderRoles(roles.roles);
  renderMarketplace(marketplace);
}

function renderRoles(roles = []) {
  els.roleList.innerHTML = "";
  roles.forEach((role) => {
    const item = document.createElement("article");
    item.className = "role-item";
    item.innerHTML = `
      <div>
        <strong>${role.label}</strong>
        <span>${role.role}</span>
      </div>
      <p>${role.description}</p>
      <small>${t("admin.permissions")}: ${role.permissions.join(", ")}</small>
    `;
    els.roleList.appendChild(item);
  });
}

function renderMarketplace(marketplace) {
  const canPublish = hasPermission("manage_catalog") || hasPermission("manage_tenants");
  if (!canPublish) {
    els.marketplaceSummary.innerHTML = "";
    els.catalogList.innerHTML = "";
    return;
  }
  const readiness = marketplace.listingReadiness;
  const operations = marketplace.operations;
  els.marketplaceSummary.innerHTML = `
    <div>
      <strong>${readiness.marketplaceStatus}</strong>
      <span>${t("admin.marketplaceStatus")}</span>
    </div>
    <div>
      <strong>${marketplace.tenant.plan}</strong>
      <span>${marketplace.tenant.name}</span>
    </div>
    <div>
      <strong>${operations.agentHealth}</strong>
      <span>${operations.optimizedEvaluationCases}/${operations.totalEvaluationCases} evaluation cases</span>
    </div>
    <div>
      <strong>${operations.publishedBooks}</strong>
      <span>${t("marketplace.catalog")}</span>
    </div>
  `;
  els.catalogList.innerHTML = "";
  marketplace.catalog.forEach((book) => {
    const item = document.createElement("article");
    item.className = "catalog-item";
    item.innerHTML = `
      <strong>${book.title}</strong>
      <p>${book.rights} | ${book.availability} | ${book.languages.join(", ")}</p>
      <small>${book.characters} characters | ${book.scenes} scenes | ${
        book.agent_modes.join(" / ")
      } | quality ${Math.round(book.quality_score * 100)}%</small>
    `;
    els.catalogList.appendChild(item);
  });
}

async function loadCapabilities() {
  const data = await api("/api/v1/challenge/capabilities");
  els.runtimeStatus.textContent = `${data.runtime.geminiMode} | ${data.runtime.geminiModel}`;
  els.runtimeGemini.textContent = data.runtime.configured ? data.runtime.geminiModel : "fallback";
}

async function loadStorage() {
  const [storage, seed] = await Promise.all([
    api("/api/v1/challenge/storage"),
    api("/api/v1/challenge/storage/demo-seed"),
  ]);
  els.runtimeStorage.textContent = storage.status.pgvector_ready ? "pgvector ready" : "fallback";
  const embeddingModel = seed.embedding?.model ?? storage.embedding?.model ?? "unknown embedding";
  els.runtimeSeed.textContent = seed.seeded
    ? `${seed.sections} sections | ${embeddingModel}`
    : "not seeded";
}

async function askCharacter(question) {
  els.characterResponse.textContent = t("character.running");
  const data = await api("/api/v1/demo/chat/character", {
    method: "POST",
    body: JSON.stringify({
      character_id: els.characterSelect.value,
      mode: els.modeSelect.value,
      language: els.languageSelect.value,
      question,
    }),
  });
  els.characterResponse.innerHTML = `
    <strong>${data.reply.character_name} | ${data.mode} | ${t("labels.language")}: ${
      data.language
    }</strong>
    <p>${data.reply.response}</p>
    ${
      data.fictionBranch
        ? `<p>${t("labels.fictionBranch")}: ${data.fictionBranch.branch_id}</p>
           <p>${data.fictionBranch.premise}</p>`
        : ""
    }
    <p>${t("labels.consistency")}: ${
      data.consistency.passed ? t("labels.passed") : t("labels.needsReview")
    }</p>
  `;
  renderTraces(data.traces);
}

async function runScene() {
  els.sceneResponse.textContent = t("scene.running");
  const data = await api("/api/v1/demo/chat/scene", {
    method: "POST",
    body: JSON.stringify({ prompt: els.scenePrompt.value }),
  });
  els.sceneResponse.innerHTML = "";
  data.scene.forEach((reply) => {
    const item = document.createElement("article");
    item.className = "scene-item";
    item.innerHTML = `
      <strong>${reply.character_name}</strong>
      <p>${reply.response}</p>
    `;
    els.sceneResponse.appendChild(item);
  });
  renderTraces(data.traces);
}

async function runNarration() {
  els.narrationResponse.textContent = t("voice.running");
  const data = await api("/api/v1/demo/narration", {
    method: "POST",
    body: JSON.stringify({ scene_text: els.narrationInput.value }),
  });
  els.narrationResponse.innerHTML = `
    <strong>${data.narration.voice_id}</strong>
    <p>${data.narration.style}</p>
    <p>${data.narration.script}</p>
    <p>Ready for TTS: ${data.narration.ready_for_tts ? "yes" : "no"} | ${
      data.narration.estimated_seconds
    } seconds</p>
  `;
  renderTraces(data.traces);
}

async function runPublisher() {
  if (!(hasPermission("manage_catalog") || hasPermission("manage_tenants"))) {
    applyAccess();
    return;
  }
  els.publisherResponse.textContent = t("publisher.running");
  const data = await api("/api/v1/demo/publisher");
  els.publisherMetrics.innerHTML = `
    <div>
      <strong>${Math.round(data.report.engagement_score * 100)}%</strong>
      <span>Engagement</span>
    </div>
    <div>
      <strong>${Math.round(data.report.quality_score * 100)}%</strong>
      <span>Quality</span>
    </div>
  `;
  els.publisherResponse.innerHTML = "";
  data.report.insights.forEach((insight) => {
    const item = document.createElement("article");
    item.className = "scene-item";
    item.innerHTML = `
      <strong>${insight.metric}: ${insight.value}</strong>
      <p>${insight.recommendation}</p>
    `;
    els.publisherResponse.appendChild(item);
  });
  renderTraces(data.traces);
}

async function runEvaluation() {
  els.evaluationResults.textContent = t("evaluation.running");
  const data = await api("/api/v1/demo/evaluation");
  els.evaluationResults.innerHTML = "";
  const summary = document.createElement("article");
  summary.className = "eval-item pass";
  summary.innerHTML = `
    <strong>${data.summary.optimizedPassed}/${data.summary.totalCases} optimized cases passed</strong>
    <p>Baseline passed ${data.summary.baselinePassed}/${data.summary.totalCases}. Improvement rate: ${
      data.summary.improvementRate
    }</p>
  `;
  els.evaluationResults.appendChild(summary);
  data.cases.forEach((result) => {
    const item = document.createElement("article");
    item.className = `eval-item ${result.optimized_passed ? "pass" : "fail"}`;
    item.innerHTML = `
      <strong>${result.case_id}</strong>
      <p>Category: ${result.category} | Character: ${result.character_id}</p>
      <p>Risk: ${result.risk}</p>
      <p>Baseline: ${result.baseline_passed ? "passed" : "failed"} | Optimized: ${
        result.optimized_passed ? "passed" : "failed"
      }</p>
      <p>Expected: ${result.expected_behavior}</p>
      <p>${result.improvement}</p>
    `;
    els.evaluationResults.appendChild(item);
  });
}

els.askCharacter.addEventListener("click", () => askCharacter(els.questionInput.value));
els.askFuture.addEventListener("click", () => {
  els.modeSelect.value = "CANON";
  els.questionInput.value = t("futureDefault");
  askCharacter(els.questionInput.value);
});
els.loginButton.addEventListener("click", login);
els.logoutButton.addEventListener("click", logout);
els.languageSelect.addEventListener("change", () => applyLanguage(els.languageSelect.value));
els.runScene.addEventListener("click", runScene);
els.runNarration.addEventListener("click", runNarration);
els.runPublisher.addEventListener("click", runPublisher);
els.refreshAdmin.addEventListener("click", loadAdmin);
els.runEvaluation.addEventListener("click", runEvaluation);
els.refreshDemo.addEventListener("click", loadBook);

applyLanguage(els.languageSelect.value);

loadBook()
  .then(runEvaluation)
  .catch((error) => {
    els.bookTitle.textContent = "Demo unavailable";
    els.bookSummary.textContent = error.message;
  });
