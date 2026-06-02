const state = {
  characters: [],
  demoUsers: [],
  language: "en",
  marketplace: null,
  currentView: "dashboard",
  session: null,
};

const els = {
  accessAccounts: document.querySelector("#accessAccounts"),
  accessScreen: document.querySelector("#accessScreen"),
  appShell: document.querySelector("#appShell"),
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
  authorAccess: document.querySelector("#authorAccess"),
  authorResponse: document.querySelector("#authorResponse"),
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
  refreshOperations: document.querySelector("#refreshOperations"),
  roleList: document.querySelector("#roleList"),
  marketplaceSummary: document.querySelector("#marketplaceSummary"),
  adminAccess: document.querySelector("#adminAccess"),
  catalogList: document.querySelector("#catalogList"),
  operationsList: document.querySelector("#operationsList"),
  operationsSummary: document.querySelector("#operationsSummary"),
  runEvaluation: document.querySelector("#runEvaluation"),
  runAuthorWorkflow: document.querySelector("#runAuthorWorkflow"),
  evaluationResults: document.querySelector("#evaluationResults"),
  traceList: document.querySelector("#traceList"),
  refreshDemo: document.querySelector("#refreshDemo"),
  runtimeStatus: document.querySelector(".status-panel p"),
  runtimeGemini: document.querySelector("#runtimeGemini"),
  runtimeStorage: document.querySelector("#runtimeStorage"),
  runtimeSeed: document.querySelector("#runtimeSeed"),
  runtimeRetrieval: document.querySelector("#runtimeRetrieval"),
  roleActions: document.querySelector("#roleActions"),
  roleDescription: document.querySelector("#roleDescription"),
  roleTitle: document.querySelector("#roleTitle"),
  roleWorkflow: document.querySelector("#roleWorkflow"),
  viewEyebrow: document.querySelector("#viewEyebrow"),
  viewTitle: document.querySelector("#viewTitle"),
};

const copy = {
  en: {
    "nav.reader": "Reader",
    "nav.dashboard": "Dashboard",
    "nav.agents": "Agents",
    "nav.author": "Author",
    "nav.publisher": "Publisher",
    "nav.admin": "Admin",
    "nav.evaluation": "Evaluation",
    "nav.runtime": "Runtime",
    "nav.architecture": "Architecture",
    "status.track": "Marketplace refactor",
    "dashboard.eyebrow": "Role workspace",
    "product.case.eyebrow": "Business case",
    "product.case.title": "Literary IP becomes interactive catalog revenue",
    "product.case.body":
      "Authors and publishers can turn owned or public-domain books into managed reader experiences with measurable engagement.",
    "product.roles.eyebrow": "Role model",
    "product.roles.title": "Each account sees its own workspace",
    "product.roles.body":
      "Reader, author, publisher, superadmin, and judge accounts are separated by permissions and protected API access.",
    "product.judge.eyebrow": "Judge route",
    "product.judge.title": "One account reviews the full submission",
    "product.judge.body":
      "The Judge Access account exposes the full tour: reader, agents, publisher, admin, evaluation, runtime, and architecture.",
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
    "login.denied": "Access denied by API",
    "top.eyebrow": "Judge demo",
    "top.title": "Multi-agent literary intelligence",
    "book.eyebrow": "Demo book",
    "author.eyebrow": "Author Workspace",
    "author.title": "Book submission pipeline",
    "author.review": "Review",
    "author.running": "Running author analysis and approval workflow.",
    "author.current": "Current title",
    "author.readiness": "Don Quijote readiness",
    "author.characterAgents": "Character agents",
    "author.modes": "Canon / Fiction modes",
    "author.stepUpload": "1. Upload manuscript",
    "author.stepUploadBody": "Author uploads an owned or public-domain book for analysis.",
    "author.stepAnalysis": "2. Gemini literary analysis",
    "author.stepAnalysisBody":
      "Characters, scenes, places, psychology, and canon constraints are prepared.",
    "author.stepReview": "3. Review generated agents",
    "author.stepReviewBody": "Author validates character voice before making the book available.",
    "author.stepPublish": "4. Submit for publishing",
    "author.stepPublishBody":
      "Publisher or superadmin approval moves the book into catalog availability.",
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
    "operations.eyebrow": "Superadmin operations",
    "operations.title": "Platform controls",
    "operations.refresh": "Refresh",
    "operations.running": "Loading platform operations.",
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
    "nav.dashboard": "Panel",
    "nav.agents": "Agentes",
    "nav.author": "Autor",
    "nav.publisher": "Editorial",
    "nav.admin": "Admin",
    "nav.evaluation": "Evaluacion",
    "nav.runtime": "Runtime",
    "nav.architecture": "Arquitectura",
    "status.track": "Refactor Marketplace",
    "dashboard.eyebrow": "Espacio por rol",
    "product.case.eyebrow": "Caso de negocio",
    "product.case.title": "La propiedad literaria se convierte en ingresos de catalogo interactivo",
    "product.case.body":
      "Autores y editoriales pueden convertir libros propios o libres de derechos en experiencias gestionadas para lectores con engagement medible.",
    "product.roles.eyebrow": "Modelo de roles",
    "product.roles.title": "Cada cuenta ve su propio espacio de trabajo",
    "product.roles.body":
      "Lector, autor, editorial, superadmin y juez estan separados por permisos y acceso protegido de API.",
    "product.judge.eyebrow": "Ruta para jueces",
    "product.judge.title": "Una cuenta revisa toda la entrega",
    "product.judge.body":
      "La cuenta Judge Access muestra el recorrido completo: lector, agentes, editorial, admin, evaluacion, runtime y arquitectura.",
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
    "login.denied": "Acceso denegado por API",
    "top.eyebrow": "Demo para jueces",
    "top.title": "Inteligencia literaria multiagente",
    "book.eyebrow": "Libro demo",
    "author.eyebrow": "Espacio de autor",
    "author.title": "Pipeline de envio de libro",
    "author.review": "Revisar",
    "author.running": "Ejecutando analisis de autor y flujo de aprobacion.",
    "author.current": "Titulo actual",
    "author.readiness": "Preparacion de Don Quijote",
    "author.characterAgents": "Agentes de personaje",
    "author.modes": "Modos canon / ficcion",
    "author.stepUpload": "1. Subir manuscrito",
    "author.stepUploadBody": "El autor sube un libro propio o libre de derechos para analisis.",
    "author.stepAnalysis": "2. Analisis literario con Gemini",
    "author.stepAnalysisBody":
      "Se preparan personajes, escenas, lugares, psicologia y restricciones canonicas.",
    "author.stepReview": "3. Revisar agentes generados",
    "author.stepReviewBody": "El autor valida la voz del personaje antes de publicar.",
    "author.stepPublish": "4. Enviar a publicacion",
    "author.stepPublishBody":
      "La editorial o superadmin aprueba el paso del libro al catalogo.",
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
    "operations.eyebrow": "Operaciones superadmin",
    "operations.title": "Controles de plataforma",
    "operations.refresh": "Actualizar",
    "operations.running": "Cargando operaciones de plataforma.",
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

const roleContent = {
  reader: {
    title: { en: "Reader workspace", es: "Espacio de lector" },
    description: {
      en: "Read available books, talk to characters, explore canon answers, and create fiction branches.",
      es: "Lee libros disponibles, habla con personajes, explora respuestas canonicas y crea ramas de ficcion.",
    },
    views: ["dashboard", "reader", "agents"],
    actions: [
      { label: { en: "Open reader", es: "Abrir lector" }, view: "reader" },
      { label: { en: "Ask Don Quijote", es: "Preguntar a Don Quijote" }, view: "agents" },
      { label: { en: "Try fiction mode", es: "Probar ficcion" }, view: "agents" },
    ],
    workflow: [
      [
        { en: "Read", es: "Leer" },
        {
          en: "Open Don Quijote and inspect extracted literary structure.",
          es: "Abre Don Quijote y revisa la estructura literaria extraida.",
        },
      ],
      [
        { en: "Chat", es: "Chat" },
        {
          en: "Ask grounded questions to characters with canon safeguards.",
          es: "Haz preguntas fundamentadas a personajes con control canonico.",
        },
      ],
      [
        { en: "Branch", es: "Rama" },
        {
          en: "Switch to fiction mode to create an alternate, separated story path.",
          es: "Cambia a ficcion para crear una ruta alternativa separada del canon.",
        },
      ],
    ],
  },
  author: {
    title: { en: "Author workspace", es: "Espacio de autor" },
    description: {
      en: "Prepare owned or public-domain books, review generated agents, and submit titles for publishing.",
      es: "Prepara libros propios o libres de derechos, revisa agentes generados y envia titulos a publicacion.",
    },
    views: ["dashboard", "author", "agents", "reader"],
    actions: [
      { label: { en: "Review analysis", es: "Revisar analisis" }, view: "author" },
      { label: { en: "Test character voice", es: "Probar voz" }, view: "agents" },
      { label: { en: "Submit title", es: "Enviar titulo" }, view: "author" },
    ],
    workflow: [
      [
        { en: "Upload", es: "Subir" },
        { en: "Submit a manuscript or public-domain title.", es: "Envia un manuscrito o titulo libre de derechos." },
      ],
      [
        { en: "Review", es: "Revisar" },
        {
          en: "Inspect Gemini analysis, characters, scenes, and psychology.",
          es: "Inspecciona analisis Gemini, personajes, escenas y psicologia.",
        },
      ],
      [
        { en: "Approve", es: "Aprobar" },
        {
          en: "Validate agent behavior before catalog publication.",
          es: "Valida el comportamiento de agentes antes de publicar en catalogo.",
        },
      ],
    ],
  },
  publisher_admin: {
    title: { en: "Publisher admin workspace", es: "Espacio de editorial" },
    description: {
      en: "Manage catalog availability, inspect engagement, and validate title quality for a publisher tenant.",
      es: "Gestiona disponibilidad de catalogo, engagement y calidad de titulos para una editorial.",
    },
    views: ["dashboard", "publisher", "admin", "evaluation", "reader", "agents"],
    actions: [
      { label: { en: "Open catalog", es: "Abrir catalogo" }, view: "admin" },
      { label: { en: "Analyze engagement", es: "Analizar engagement" }, view: "publisher" },
      { label: { en: "Review quality", es: "Revisar calidad" }, view: "evaluation" },
    ],
    workflow: [
      [
        { en: "Catalog", es: "Catalogo" },
        {
          en: "Manage titles and availability across the publisher tenant.",
          es: "Gestiona titulos y disponibilidad dentro de la editorial.",
        },
      ],
      [
        { en: "Engagement", es: "Engagement" },
        {
          en: "Use conversations and scenes as measurable reader signals.",
          es: "Usa conversaciones y escenas como senales medibles de lectores.",
        },
      ],
      [
        { en: "Quality", es: "Calidad" },
        {
          en: "Review evaluation, grounding, and consistency before rollout.",
          es: "Revisa evaluacion, fundamentacion y consistencia antes de desplegar.",
        },
      ],
    ],
  },
  super_admin: {
    title: { en: "Super admin workspace", es: "Espacio superadmin" },
    description: {
      en: "Operate tenants, users, costs, platform readiness, and Google Cloud runtime health.",
      es: "Opera tenants, usuarios, costes, preparacion de plataforma y salud en Google Cloud.",
    },
    views: [
      "dashboard",
      "admin",
      "publisher",
      "evaluation",
      "runtime",
      "architecture",
      "reader",
      "agents",
      "author",
    ],
    actions: [
      { label: { en: "Operate platform", es: "Operar plataforma" }, view: "admin" },
      { label: { en: "Inspect runtime", es: "Ver runtime" }, view: "runtime" },
      { label: { en: "Review Marketplace", es: "Revisar Marketplace" }, view: "architecture" },
    ],
    workflow: [
      [
        { en: "Tenants", es: "Tenants" },
        { en: "Manage publishers, roles, and platform access.", es: "Gestiona editoriales, roles y acceso." },
      ],
      [
        { en: "Runtime", es: "Runtime" },
        {
          en: "Inspect Cloud Run, Gemini, Cloud SQL pgvector, and traces.",
          es: "Inspecciona Cloud Run, Gemini, Cloud SQL pgvector y trazas.",
        },
      ],
      [
        { en: "Marketplace", es: "Marketplace" },
        {
          en: "Prepare listing evidence for Google Cloud Marketplace.",
          es: "Prepara evidencias para publicar en Google Cloud Marketplace.",
        },
      ],
    ],
  },
  judge_access: {
    title: { en: "Judge review tour", es: "Recorrido para jueces" },
    description: {
      en: "A guided full-access review account for the challenge: reader flow, agents, publisher value, admin readiness, runtime, and evaluation.",
      es: "Cuenta guiada con acceso completo para el desafio: lector, agentes, valor editorial, admin, runtime y evaluacion.",
    },
    views: [
      "dashboard",
      "reader",
      "agents",
      "author",
      "publisher",
      "admin",
      "evaluation",
      "runtime",
      "architecture",
    ],
    actions: [
      { label: { en: "Run 3-minute demo", es: "Demo de 3 minutos" }, view: "reader" },
      { label: { en: "Check protected admin", es: "Ver admin protegido" }, view: "admin" },
      { label: { en: "Inspect Cloud proof", es: "Ver prueba Cloud" }, view: "runtime" },
    ],
    workflow: [
      [
        { en: "1. Reader", es: "1. Lector" },
        {
          en: "Open Don Quijote, chat with a character in English or Spanish.",
          es: "Abre Don Quijote y habla con un personaje en ingles o espanol.",
        },
      ],
      [
        { en: "2. Agents", es: "2. Agentes" },
        {
          en: "Switch between canon and fiction branch behavior.",
          es: "Cambia entre comportamiento canonico y rama de ficcion.",
        },
      ],
      [
        { en: "3. Publisher", es: "3. Editorial" },
        {
          en: "Use protected token access to inspect catalog and insights.",
          es: "Usa acceso protegido por token para revisar catalogo e insights.",
        },
      ],
      [
        { en: "4. Platform", es: "4. Plataforma" },
        {
          en: "Review roles, runtime, evaluation, and Marketplace readiness.",
          es: "Revisa roles, runtime, evaluacion y preparacion Marketplace.",
        },
      ],
    ],
  },
};

const viewTitles = {
  dashboard: ["Workspace", "Role dashboard"],
  reader: ["Reader", "Book experience"],
  agents: ["Agents", "Character and scene agents"],
  author: ["Author", "Book submission pipeline"],
  publisher: ["Publisher", "Catalog and engagement"],
  admin: ["Admin", "Roles and Marketplace readiness"],
  evaluation: ["Evaluation", "Before / after quality evidence"],
  runtime: ["Runtime", "Google Cloud proof"],
  architecture: ["Architecture", "Cloud target architecture"],
};

function t(key) {
  return copy[state.language][key] ?? copy.en[key] ?? key;
}

function localize(value) {
  if (typeof value === "string") {
    return value;
  }
  return value[state.language] ?? value.en ?? "";
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
  renderRoleDashboard();
}

async function api(path, options = {}) {
  const headers = { "content-type": "application/json", ...(options.headers ?? {}) };
  const response = await fetch(path, {
    ...options,
    headers,
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function authHeaders() {
  return state.session ? { authorization: `Bearer ${state.session.token}` } : {};
}

async function loadAuth() {
  const data = await api("/api/v1/auth/demo-users");
  state.demoUsers = data.users;
  els.userSelect.innerHTML = "";
  els.accessAccounts.innerHTML = "";
  data.users.forEach((user) => {
    const option = document.createElement("option");
    option.value = user.user_id;
    option.textContent = `${user.name} (${user.role})`;
    els.userSelect.appendChild(option);

    const account = document.createElement("button");
    account.className = user.role === "judge_access" ? "account-card judge" : "account-card";
    account.innerHTML = `
      <strong>${user.name}</strong>
      <span>${user.role}</span>
      <small>${user.tenant_id}</small>
    `;
    account.addEventListener("click", () => loginAs(user.user_id));
    els.accessAccounts.appendChild(account);
  });
  const savedSession = localStorage.getItem("stormsboys-demo-session");
  if (savedSession) {
    state.session = JSON.parse(savedSession);
    els.userSelect.value = state.session.user.user_id;
  }
  renderSession();
  applyAccess();
  renderShell();
  renderRoleDashboard();
  applyViewAccess();
}

async function login() {
  await loginAs(els.userSelect.value);
}

async function loginAs(userId) {
  const data = await api("/api/v1/auth/demo-login", {
    method: "POST",
    body: JSON.stringify({ user_id: userId }),
  });
  state.session = data;
  els.userSelect.value = data.user.user_id;
  localStorage.setItem("stormsboys-demo-session", JSON.stringify(data));
  renderSession();
  applyAccess();
  renderShell();
  renderRoleDashboard();
  applyViewAccess();
  setView("dashboard");
  await loadAdmin();
}

function logout() {
  state.session = null;
  state.marketplace = null;
  localStorage.removeItem("stormsboys-demo-session");
  renderSession();
  applyAccess();
  renderShell();
  renderRoleDashboard();
  applyViewAccess();
}

function renderShell() {
  const signedIn = Boolean(state.session);
  els.accessScreen.classList.toggle("is-hidden", signedIn);
  els.appShell.classList.toggle("is-hidden", !signedIn);
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
  const canAuthor = hasPermission("upload_owned_books") || hasPermission("manage_tenants");
  const canPublish = hasPermission("manage_catalog") || hasPermission("manage_tenants");
  const canOperate = hasPermission("manage_tenants");
  els.runAuthorWorkflow.disabled = !canAuthor;
  els.runPublisher.disabled = !canPublish;
  els.refreshAdmin.disabled = !canPublish;
  els.refreshOperations.disabled = !canOperate;
  els.authorAccess.textContent = canAuthor
    ? `${t("login.allowed")}: author workflow`
    : state.session
      ? "Author or Super Admin access required."
      : t("login.required");
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
  els.authorAccess.className = canAuthor ? "access-box granted" : "access-box locked";
  els.publisherAccess.className = canPublish ? "access-box granted" : "access-box locked";
  els.adminAccess.className = canOperate ? "access-box granted" : "access-box locked";
  if (state.marketplace) {
    renderMarketplace(state.marketplace);
  }
}

function activeRoleConfig() {
  return roleContent[state.session?.user?.role] ?? roleContent.reader;
}

function renderRoleDashboard() {
  if (!state.session) {
    els.roleTitle.textContent = "Sign in to continue";
    els.roleDescription.textContent = "Choose a demo account to see the correct product area.";
    els.roleActions.innerHTML = "";
    els.roleWorkflow.innerHTML = "";
    return;
  }
  const config = activeRoleConfig();
  els.roleTitle.textContent = localize(config.title);
  els.roleDescription.textContent = localize(config.description);
  els.roleActions.innerHTML = "";
  config.actions.forEach((action) => {
    const button = document.createElement("button");
    button.className = "secondary";
    button.textContent = localize(action.label);
    button.addEventListener("click", () => setView(action.view));
    els.roleActions.appendChild(button);
  });
  els.roleWorkflow.innerHTML = config.workflow
    .map(
      ([title, description]) => `
        <article class="workflow-item">
          <strong>${localize(title)}</strong>
          <p>${localize(description)}</p>
        </article>
      `,
    )
    .join("");
}

function canView(view) {
  return activeRoleConfig().views.includes(view);
}

function setView(view) {
  const target = canView(view) ? view : "dashboard";
  state.currentView = target;
  document.querySelectorAll(".view-panel").forEach((panel) => {
    panel.classList.toggle("is-hidden", panel.dataset.view !== target);
  });
  document.querySelectorAll("[data-view-target]").forEach((item) => {
    item.classList.toggle("active", item.dataset.viewTarget === target);
  });
  const [eyebrow, title] = viewTitles[target] ?? viewTitles.dashboard;
  els.viewEyebrow.textContent = eyebrow;
  els.viewTitle.textContent = title;
}

function applyViewAccess() {
  const allowedViews = activeRoleConfig().views;
  document.querySelectorAll("[data-view-target]").forEach((item) => {
    item.classList.toggle("is-hidden", !allowedViews.includes(item.dataset.viewTarget));
  });
  if (!allowedViews.includes(state.currentView)) {
    setView("dashboard");
  } else {
    setView(state.currentView);
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
  els.operationsSummary.textContent = t("operations.running");
  const roles = await api("/api/v1/admin/roles");
  const canPublish = hasPermission("manage_catalog") || hasPermission("manage_tenants");
  const canOperate = hasPermission("manage_tenants");
  const marketplace = canPublish
    ? await api("/api/v1/admin/marketplace", { headers: authHeaders() })
    : null;
  const operations = canOperate
    ? await api("/api/v1/admin/operations", { headers: authHeaders() })
    : null;
  state.marketplace = marketplace;
  renderRoles(roles.roles);
  if (marketplace) {
    renderMarketplace(marketplace);
  } else {
    els.marketplaceSummary.innerHTML = "";
    els.catalogList.innerHTML = "";
  }
  if (operations) {
    renderOperations(operations);
  } else {
    els.operationsSummary.innerHTML = "";
    els.operationsList.innerHTML = "";
  }
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

function renderOperations(operations) {
  els.operationsSummary.innerHTML = `
    <div>
      <strong>${operations.runtime.gemini}</strong>
      <span>Gemini</span>
    </div>
    <div>
      <strong>${operations.runtime.retrieval}</strong>
      <span>Retrieval</span>
    </div>
    <div>
      <strong>${operations.tenantOperations.users}</strong>
      <span>Users</span>
    </div>
    <div>
      <strong>${operations.qualityGate.optimizedCases}/${operations.qualityGate.totalCases}</strong>
      <span>Quality gate</span>
    </div>
  `;
  els.operationsList.innerHTML = "";
  operations.governance.forEach((item) => {
    const row = document.createElement("article");
    row.className = "catalog-item";
    row.innerHTML = `<strong>${item}</strong>`;
    els.operationsList.appendChild(row);
  });
}

async function runAuthorWorkflow() {
  if (!(hasPermission("upload_owned_books") || hasPermission("manage_tenants"))) {
    applyAccess();
    return;
  }
  els.authorResponse.textContent = t("author.running");
  let data;
  try {
    data = await api("/api/v1/demo/author-workflow", { headers: authHeaders() });
  } catch (error) {
    els.authorResponse.textContent = `${t("login.denied")}: ${error.message}`;
    return;
  }
  els.authorResponse.innerHTML = `
    <strong>${data.manuscript.title} | ${data.manuscript.status}</strong>
    <p>${data.analysisSummary.characters} character agents, ${
      data.analysisSummary.scenes
    } scenes, ${data.analysisSummary.places} places.</p>
    <p>${data.analysisSummary.canonMode}</p>
    <p>${data.analysisSummary.fictionMode}</p>
  `;
  els.authorResponse.insertAdjacentHTML(
    "beforeend",
    data.approvalChecklist
      .map((item) => `<p>${item.item}: ${item.status} | ${item.evidence}</p>`)
      .join(""),
  );
  renderTraces(data.traces);
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
  let data;
  try {
    data = await api("/api/v1/demo/publisher", { headers: authHeaders() });
  } catch (error) {
    els.publisherResponse.textContent = `${t("login.denied")}: ${error.message}`;
    return;
  }
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
document.querySelectorAll("[data-view-target]").forEach((item) => {
  item.addEventListener("click", () => setView(item.dataset.viewTarget));
});
els.languageSelect.addEventListener("change", () => applyLanguage(els.languageSelect.value));
els.runScene.addEventListener("click", runScene);
els.runNarration.addEventListener("click", runNarration);
els.runAuthorWorkflow.addEventListener("click", runAuthorWorkflow);
els.runPublisher.addEventListener("click", runPublisher);
els.refreshAdmin.addEventListener("click", loadAdmin);
els.refreshOperations.addEventListener("click", loadAdmin);
els.runEvaluation.addEventListener("click", runEvaluation);
els.refreshDemo.addEventListener("click", loadBook);

applyLanguage(els.languageSelect.value);
renderShell();
setView("dashboard");

loadBook()
  .then(runEvaluation)
  .catch((error) => {
    els.bookTitle.textContent = "Demo unavailable";
    els.bookSummary.textContent = error.message;
  });
