const state = {
  characters: [],
  catalog: [],
  demoUsers: [],
  language: "en",
  marketplace: null,
  currentBookId: "don-quijote",
  currentBookDetail: null,
  currentSectionIndex: 0,
  currentView: "reader",
  session: null,
  currentCharacterSessionId: "judge-demo-session",
};

const els = {
  accessAccounts: document.querySelector("#accessAccounts"),
  accessScreen: document.querySelector("#accessScreen"),
  appShell: document.querySelector("#appShell"),
  bookTitle: document.querySelector("#bookTitle"),
  bookSummary: document.querySelector("#bookSummary"),
  readerCatalog: document.querySelector("#readerCatalog"),
  readerActiveTitle: document.querySelector("#readerActiveTitle"),
  readerProgressInput: document.querySelector("#readerProgressInput"),
  readerProgressLabel: document.querySelector("#readerProgressLabel"),
  readerExcerpt: document.querySelector("#readerExcerpt"),
  readerBookMeta: document.querySelector("#readerBookMeta"),
  readerPrevSection: document.querySelector("#readerPrevSection"),
  readerNextSection: document.querySelector("#readerNextSection"),
  readerSectionLabel: document.querySelector("#readerSectionLabel"),
  readerNoteInput: document.querySelector("#readerNoteInput"),
  saveReaderNote: document.querySelector("#saveReaderNote"),
  markReaderFavorite: document.querySelector("#markReaderFavorite"),
  readerNoteList: document.querySelector("#readerNoteList"),
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
  characterPsychology: document.querySelector("#characterPsychology"),
  characterMemory: document.querySelector("#characterMemory"),
  characterCitations: document.querySelector("#characterCitations"),
  characterHistory: document.querySelector("#characterHistory"),
  fictionTimeline: document.querySelector("#fictionTimeline"),
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
  cleanupSession: document.querySelector("#cleanupSession"),
  cleanupSessionInput: document.querySelector("#cleanupSessionInput"),
  cleanupResult: document.querySelector("#cleanupResult"),
  uploadTitle: document.querySelector("#uploadTitle"),
  uploadAuthor: document.querySelector("#uploadAuthor"),
  uploadRights: document.querySelector("#uploadRights"),
  uploadFile: document.querySelector("#uploadFile"),
  uploadBook: document.querySelector("#uploadBook"),
  roleList: document.querySelector("#roleList"),
  marketplaceSummary: document.querySelector("#marketplaceSummary"),
  marketplaceExportResult: document.querySelector("#marketplaceExportResult"),
  exportMarketplace: document.querySelector("#exportMarketplace"),
  downloadMarketplaceCsv: document.querySelector("#downloadMarketplaceCsv"),
  adminAccess: document.querySelector("#adminAccess"),
  publisherEngagementBoard: document.querySelector("#publisherEngagementBoard"),
  catalogList: document.querySelector("#catalogList"),
  operationsList: document.querySelector("#operationsList"),
  operationsSummary: document.querySelector("#operationsSummary"),
  runEvaluation: document.querySelector("#runEvaluation"),
  runAuthorWorkflow: document.querySelector("#runAuthorWorkflow"),
  evaluationResults: document.querySelector("#evaluationResults"),
  traceList: document.querySelector("#traceList"),
  refreshDemo: document.querySelector("#refreshDemo"),
  runtimeGemini: document.querySelector("#runtimeGemini"),
  runtimeStorage: document.querySelector("#runtimeStorage"),
  runtimeSeed: document.querySelector("#runtimeSeed"),
  runtimeRetrieval: document.querySelector("#runtimeRetrieval"),
  submissionCriteria: document.querySelector("#submissionCriteria"),
  submissionDeliverables: document.querySelector("#submissionDeliverables"),
  submissionSummary: document.querySelector("#submissionSummary"),
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
    "track.build": "new agent layer",
    "track.optimize": "quality evidence",
    "track.refactor": "Marketplace ready",
    "dashboard.eyebrow": "Role workspace",
    "journey.eyebrow": "Judge journey",
    "journey.title": "From manuscript to living literary world",
    "journey.body":
      "Follow the product path judges should see in the video: upload a book, generate agents, chat in canon, branch into fiction, prove publisher value, and verify the Google Cloud runtime.",
    "journey.start": "Start with upload",
    "journey.chat": "Run character demo",
    "journey.proof": "Inspect Cloud proof",
    "journey.stepUpload": "Upload manuscript",
    "journey.stepUploadBody":
      "Author or publisher brings owned/public-domain IP into the platform.",
    "journey.stepAnalyze": "Generate literary agents",
    "journey.stepAnalyzeBody":
      "Gemini extracts characters, psychology, scenes, canon constraints, and embeddings.",
    "journey.stepReader": "Reader experience",
    "journey.stepReaderBody":
      "Readers talk to characters, ask in English or Spanish, and get grounded answers.",
    "journey.stepFiction": "Fiction branches",
    "journey.stepFictionBody":
      "Alternative storylines are saved separately from canon and can evolve over time.",
    "journey.stepBusiness": "Publisher value",
    "journey.stepBusinessBody":
      "Catalog owners see engagement, quality, title readiness, and admin controls.",
    "journey.stepCloud": "Cloud proof",
    "journey.stepCloudBody":
      "Cloud Run, Gemini, Cloud SQL pgvector, Secret Manager, traces, and A2A card.",
    "proof.build":
      "New agent layer, upload pipeline, character/scene/publisher/admin agents, and A2A-ready contract.",
    "proof.optimize":
      "Before/after evaluation, retrieval grounding, canon guardrails, memory separation, and traces.",
    "proof.refactor":
      "Cloud Run deployment, Gemini via Vertex AI, Cloud SQL pgvector, roles, and Marketplace path.",
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
    "submission.eyebrow": "Submission readiness",
    "submission.title": "Challenge evidence",
    "submission.criteria": "Criteria",
    "submission.deliverables": "Deliverables",
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
    "reader.eyebrow": "Interactive library",
    "reader.title": "Read, listen, and speak with the world inside a book",
    "reader.body":
      "Don Quijote is the public-domain demo title. The same pipeline now supports uploaded manuscripts, generated character psychology, canon chat, fiction branches, scene orchestration, voice handoff, and publisher review.",
    "reader.chat": "Chat with characters",
    "reader.upload": "Upload a book",
    "reader.publisher": "Publisher view",
    "reader.available": "Available in catalog",
    "reader.languages": "English and Spanish",
    "reader.memory": "Memory separated by mode",
    "reader.laneCanon": "Canon conversation",
    "reader.laneCanonBody": "Answers stay grounded in retrieved book sections.",
    "reader.laneFiction": "Fiction branch",
    "reader.laneFictionBody": "Alternative story paths are saved separately from canon.",
    "reader.laneBusiness": "Publisher signal",
    "reader.laneBusinessBody": "Reader interactions become measurable catalog insight.",
    "reader.catalogEyebrow": "Library catalog",
    "reader.catalogTitle": "Choose the book experience",
    "reader.pageEyebrow": "Reading session",
    "reader.progress": "Reading progress",
    "reader.talkNow": "Talk now",
    "reader.demoType": "Public-domain demo",
    "reader.uploadedType": "Uploaded manuscript",
    "reader.openBook": "Open",
    "reader.active": "Active",
    "reader.charactersReady": "characters ready",
    "reader.noUploaded": "Upload a manuscript to add it to this catalog.",
    "reader.scenes": "Key scenes",
    "reader.places": "Places",
    "reader.previous": "Previous",
    "reader.next": "Next",
    "reader.section": "Section",
    "reader.noteLabel": "Reader note",
    "reader.notePlaceholder": "Capture a thought, question, or publisher signal.",
    "reader.saveNote": "Save note",
    "reader.favorite": "Mark favorite",
    "reader.favoriteSaved": "Favorite section saved",
    "reader.noNotes": "No notes for this section yet.",
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
    "marketplace.readerSignals": "Reader signals",
    "marketplace.signalBoard": "Engagement board",
    "marketplace.signalBoardEmpty": "No reader signals yet. Open Reader, save a note or favorite, then refresh.",
    "marketplace.readers": "Readers",
    "marketplace.notes": "Notes",
    "marketplace.favorites": "Favorites",
    "marketplace.progress": "Progress",
    "marketplace.action": "Next action",
    "marketplace.quality": "Quality",
    "marketplace.availability": "Availability",
    "marketplace.sectionSignals": "Section signals",
    "marketplace.noSectionSignals": "No section-level signals yet.",
    "marketplace.lastSignal": "Last signal",
    "marketplace.characterSignals": "Character signals",
    "marketplace.noCharacterSignals": "No character chat signals yet.",
    "marketplace.turns": "Turns",
    "marketplace.sessions": "Sessions",
    "marketplace.preferences": "Prefs",
    "marketplace.export": "Export insights",
    "marketplace.downloadCsv": "Download CSV",
    "marketplace.exportRunning": "Preparing publisher export package.",
    "marketplace.csvRunning": "Preparing CSV download.",
    "marketplace.exportReady": "Export package ready",
    "marketplace.csvReady": "CSV package downloaded",
    "marketplace.exportBlocked": "Publisher Admin or Super Admin export access required.",
    "operations.eyebrow": "Superadmin operations",
    "operations.title": "Platform controls",
    "operations.refresh": "Refresh",
    "operations.running": "Loading platform operations.",
    "operations.cleanup": "Clear session",
    "operations.cleanupLabel": "Demo session",
    "operations.cleanupRunning": "Clearing demo session.",
    "operations.cleanupDone": "Session cleared",
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
    "track.build": "nueva capa de agentes",
    "track.optimize": "evidencia de calidad",
    "track.refactor": "listo para Marketplace",
    "dashboard.eyebrow": "Espacio por rol",
    "journey.eyebrow": "Recorrido para jueces",
    "journey.title": "De manuscrito a mundo literario vivo",
    "journey.body":
      "Sigue la ruta que deben ver los jueces en el video: subir libro, generar agentes, chatear en canon, crear ficcion, probar valor editorial y verificar Google Cloud.",
    "journey.start": "Empezar con upload",
    "journey.chat": "Ejecutar demo de personaje",
    "journey.proof": "Inspeccionar prueba Cloud",
    "journey.stepUpload": "Subir manuscrito",
    "journey.stepUploadBody":
      "Autor o editorial incorpora IP propia o libre de derechos a la plataforma.",
    "journey.stepAnalyze": "Generar agentes literarios",
    "journey.stepAnalyzeBody":
      "Gemini extrae personajes, psicologia, escenas, restricciones canonicas y embeddings.",
    "journey.stepReader": "Experiencia lectora",
    "journey.stepReaderBody":
      "Los lectores hablan con personajes, preguntan en ingles o espanol y reciben respuestas ancladas.",
    "journey.stepFiction": "Ramas de ficcion",
    "journey.stepFictionBody":
      "Las historias alternativas se guardan separadas del canon y pueden evolucionar.",
    "journey.stepBusiness": "Valor editorial",
    "journey.stepBusinessBody":
      "Los duenos del catalogo ven engagement, calidad, estado del titulo y controles admin.",
    "journey.stepCloud": "Prueba Cloud",
    "journey.stepCloudBody":
      "Cloud Run, Gemini, Cloud SQL pgvector, Secret Manager, trazas y agent card A2A.",
    "proof.build":
      "Nueva capa de agentes, pipeline de upload, agentes de personaje/escena/editorial/admin y contrato A2A-ready.",
    "proof.optimize":
      "Evaluacion before/after, grounding, guardrails canonicos, memoria separada y trazas.",
    "proof.refactor":
      "Deploy en Cloud Run, Gemini via Vertex AI, Cloud SQL pgvector, roles y ruta Marketplace.",
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
    "submission.eyebrow": "Preparacion de entrega",
    "submission.title": "Evidencia del challenge",
    "submission.criteria": "Criterios",
    "submission.deliverables": "Entregables",
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
    "reader.eyebrow": "Biblioteca interactiva",
    "reader.title": "Lee, escucha y habla con el mundo dentro de un libro",
    "reader.body":
      "Don Quijote es el titulo demo de dominio publico. El mismo pipeline ya soporta manuscritos subidos, psicologia de personajes, chat canonico, ramas de ficcion, orquestacion de escenas, voz y revision editorial.",
    "reader.chat": "Hablar con personajes",
    "reader.upload": "Subir libro",
    "reader.publisher": "Vista editorial",
    "reader.available": "Disponible en catalogo",
    "reader.languages": "Ingles y espanol",
    "reader.memory": "Memoria separada por modo",
    "reader.laneCanon": "Conversacion canonica",
    "reader.laneCanonBody": "Las respuestas se anclan en secciones recuperadas del libro.",
    "reader.laneFiction": "Rama de ficcion",
    "reader.laneFictionBody": "Las rutas alternativas se guardan separadas del canon.",
    "reader.laneBusiness": "Senal editorial",
    "reader.laneBusinessBody": "Las interacciones se convierten en insight medible de catalogo.",
    "reader.catalogEyebrow": "Catalogo de biblioteca",
    "reader.catalogTitle": "Elige la experiencia del libro",
    "reader.pageEyebrow": "Sesion de lectura",
    "reader.progress": "Progreso de lectura",
    "reader.talkNow": "Hablar ahora",
    "reader.demoType": "Demo de dominio publico",
    "reader.uploadedType": "Manuscrito subido",
    "reader.openBook": "Abrir",
    "reader.active": "Activo",
    "reader.charactersReady": "personajes listos",
    "reader.noUploaded": "Sube un manuscrito para anadirlo a este catalogo.",
    "reader.scenes": "Escenas clave",
    "reader.places": "Lugares",
    "reader.previous": "Anterior",
    "reader.next": "Siguiente",
    "reader.section": "Seccion",
    "reader.noteLabel": "Nota del lector",
    "reader.notePlaceholder": "Guarda una idea, pregunta o senal editorial.",
    "reader.saveNote": "Guardar nota",
    "reader.favorite": "Marcar favorito",
    "reader.favoriteSaved": "Seccion favorita guardada",
    "reader.noNotes": "Todavia no hay notas en esta seccion.",
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
    "marketplace.readerSignals": "Senales de lector",
    "marketplace.signalBoard": "Panel de engagement",
    "marketplace.signalBoardEmpty": "Aun no hay senales de lector. Abre Lector, guarda una nota o favorito y actualiza.",
    "marketplace.readers": "Lectores",
    "marketplace.notes": "Notas",
    "marketplace.favorites": "Favoritos",
    "marketplace.progress": "Progreso",
    "marketplace.action": "Siguiente accion",
    "marketplace.quality": "Calidad",
    "marketplace.availability": "Disponibilidad",
    "marketplace.sectionSignals": "Senales por seccion",
    "marketplace.noSectionSignals": "Aun no hay senales por seccion.",
    "marketplace.lastSignal": "Ultima senal",
    "marketplace.characterSignals": "Senales por personaje",
    "marketplace.noCharacterSignals": "Aun no hay senales de chat por personaje.",
    "marketplace.turns": "Turnos",
    "marketplace.sessions": "Sesiones",
    "marketplace.preferences": "Prefs",
    "marketplace.export": "Exportar insights",
    "marketplace.downloadCsv": "Descargar CSV",
    "marketplace.exportRunning": "Preparando paquete de exportacion editorial.",
    "marketplace.csvRunning": "Preparando descarga CSV.",
    "marketplace.exportReady": "Paquete de exportacion listo",
    "marketplace.csvReady": "CSV descargado",
    "marketplace.exportBlocked": "Se requiere acceso Publisher Admin o Super Admin para exportar.",
    "operations.eyebrow": "Operaciones superadmin",
    "operations.title": "Controles de plataforma",
    "operations.refresh": "Actualizar",
    "operations.running": "Cargando operaciones de plataforma.",
    "operations.cleanup": "Limpiar sesion",
    "operations.cleanupLabel": "Sesion demo",
    "operations.cleanupRunning": "Limpiando sesion demo.",
    "operations.cleanupDone": "Sesion limpiada",
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
  reader: ["Reader", "Interactive book experience"],
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

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function applyLanguage(language) {
  const previousCopy = copy[state.language];
  state.language = language;
  document.documentElement.lang = language;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
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
  renderReaderCatalog();
  if (state.currentBookDetail) {
    const currentIndex = state.currentSectionIndex;
    updateActiveBook(
      state.currentBookDetail.book,
      state.currentBookDetail.analysis,
      [],
      state.currentBookDetail.readingSections,
    );
    goToReaderSection(currentIndex);
  }
}

async function api(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const headers = {
    ...(isFormData ? {} : { "content-type": "application/json" }),
    ...(options.headers ?? {}),
  };
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
  setView("reader");
  await loadReaderCatalog();
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
  loadReaderCatalog();
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
  const canExport = hasPermission("export_catalog_insights") || hasPermission("manage_tenants");
  const canOperate = hasPermission("manage_tenants");
  els.runAuthorWorkflow.disabled = !canAuthor;
  els.runPublisher.disabled = !canPublish;
  els.refreshAdmin.disabled = !canPublish;
  els.exportMarketplace.disabled = !canExport;
  els.downloadMarketplaceCsv.disabled = !canExport;
  els.refreshOperations.disabled = !canOperate;
  els.cleanupSession.disabled = !canOperate;
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
  els.cleanupResult.className = canOperate ? "access-box granted" : "access-box locked";
  if (!canExport) {
    els.marketplaceExportResult.textContent = state.session
      ? t("marketplace.exportBlocked")
      : t("login.required");
    els.marketplaceExportResult.className = "access-box locked";
  }
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

function bookProgressKey(bookId) {
  return `stormsboys-reader-progress:${bookId}`;
}

function currentBookProgress() {
  return Number(localStorage.getItem(bookProgressKey(state.currentBookId)) ?? "0");
}

function saveCurrentBookProgress(value) {
  localStorage.setItem(bookProgressKey(state.currentBookId), String(value));
  renderReaderProgress();
}

function readerNotesKey(bookId, sectionId) {
  return `stormsboys-reader-notes:${bookId}:${sectionId}`;
}

function loadReaderNotes(sectionId) {
  const raw = localStorage.getItem(readerNotesKey(state.currentBookId, sectionId));
  if (!raw) {
    return [];
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    return [];
  }
}

function saveReaderNotes(sectionId, notes) {
  localStorage.setItem(readerNotesKey(state.currentBookId, sectionId), JSON.stringify(notes));
}

function noteFromReaderEvent(event) {
  return {
    kind: event.event_type === "favorite" ? t("reader.favoriteSaved") : t("reader.noteLabel"),
    text: event.note_text || "",
  };
}

function renderReaderProgress() {
  const progress = currentBookProgress();
  els.readerProgressInput.value = String(progress);
  els.readerProgressLabel.textContent = `${progress}%`;
}

function activeReadingSections() {
  return state.currentBookDetail?.readingSections ?? [];
}

function activeReadingSection() {
  const sections = activeReadingSections();
  return sections[state.currentSectionIndex] ?? null;
}

function summarizeBookForReader(analysis, section) {
  const scenes = analysis.scenes ?? [];
  const places = analysis.places ?? [];
  const sceneLines = scenes
    .slice(0, 3)
    .map((scene) => `<li>${escapeHtml(scene.summary ?? scene.name ?? scene.scene_id)}</li>`)
    .join("");
  const placeLine = places
    .slice(0, 4)
    .map((place) => escapeHtml(place))
    .join(", ");
  return `
    ${
      section
        ? `<article class="reader-section-text">
            <p>${escapeHtml(section.text)}</p>
          </article>`
        : ""
    }
    <p>${escapeHtml(analysis.summary)}</p>
    ${
      sceneLines
        ? `<strong>${t("reader.scenes")}</strong><ul>${sceneLines}</ul>`
        : ""
    }
    ${
      placeLine
        ? `<p><strong>${t("reader.places")}:</strong> ${placeLine}</p>`
        : ""
    }
  `;
}

function renderReaderNotes() {
  const section = activeReadingSection();
  if (!section) {
    els.readerNoteList.innerHTML = `<p>${t("reader.noNotes")}</p>`;
    return;
  }
  const notes = loadReaderNotes(section.section_id);
  els.readerNoteList.innerHTML = notes.length
    ? notes
        .map(
          (note) => `
            <article>
              <strong>${escapeHtml(note.kind)}</strong>
              <p>${escapeHtml(note.text)}</p>
            </article>
          `,
        )
        .join("")
    : `<p>${t("reader.noNotes")}</p>`;
}

async function hydrateReaderNotes(section) {
  if (!state.session?.token || !section) {
    return;
  }
  try {
    const params = new URLSearchParams({
      book_id: state.currentBookId,
      section_id: section.section_id,
    });
    const data = await api(`/api/v1/reader/notes?${params.toString()}`, {
      headers: authHeaders(),
    });
    const notes = (data.notes ?? []).map(noteFromReaderEvent);
    if (notes.length) {
      saveReaderNotes(section.section_id, notes);
      renderReaderNotes();
    }
  } catch (error) {
    // Local notes remain available if backend persistence is unavailable.
  }
}

function renderReaderPage() {
  const sections = activeReadingSections();
  const section = activeReadingSection();
  const total = Math.max(sections.length, 1);
  els.readerSectionLabel.textContent = `${t("reader.section")} ${state.currentSectionIndex + 1} / ${total}`;
  els.readerPrevSection.disabled = state.currentSectionIndex <= 0;
  els.readerNextSection.disabled = state.currentSectionIndex >= sections.length - 1;
  els.readerExcerpt.innerHTML = summarizeBookForReader(
    state.currentBookDetail?.analysis ?? { summary: "", scenes: [], places: [] },
    section,
  );
  renderReaderNotes();
  hydrateReaderNotes(section);
}

async function persistReaderProgress(progress, section) {
  if (!state.session?.token || !section) {
    return;
  }
  try {
    await api("/api/v1/reader/progress", {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        book_id: state.currentBookId,
        section_id: section.section_id,
        section_index: state.currentSectionIndex,
        progress_percent: progress,
      }),
    });
  } catch (error) {
    // Progress remains available locally.
  }
}

async function hydrateReaderProgress() {
  if (!state.session?.token) {
    return;
  }
  try {
    const params = new URLSearchParams({ book_id: state.currentBookId });
    const data = await api(`/api/v1/reader/progress?${params.toString()}`, {
      headers: authHeaders(),
    });
    if (!data.progress) {
      return;
    }
    const sections = activeReadingSections();
    state.currentSectionIndex = Math.max(
      0,
      Math.min(data.progress.section_index ?? 0, Math.max(sections.length - 1, 0)),
    );
    localStorage.setItem(
      bookProgressKey(state.currentBookId),
      String(data.progress.progress_percent ?? currentBookProgress()),
    );
    renderReaderProgress();
    renderReaderPage();
  } catch (error) {
    // Local progress remains the fallback.
  }
}

function goToReaderSection(nextIndex) {
  const sections = activeReadingSections();
  state.currentSectionIndex = Math.max(0, Math.min(nextIndex, Math.max(sections.length - 1, 0)));
  const progress = sections.length
    ? Math.round(((state.currentSectionIndex + 1) / sections.length) * 100)
    : currentBookProgress();
  saveCurrentBookProgress(progress);
  persistReaderProgress(progress, activeReadingSection());
  renderReaderPage();
}

async function persistReaderNote(eventType, noteText, section) {
  if (!state.session?.token || !section) {
    return;
  }
  try {
    await api("/api/v1/reader/notes", {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        book_id: state.currentBookId,
        section_id: section.section_id,
        section_index: state.currentSectionIndex,
        event_type: eventType,
        note_text: noteText,
      }),
    });
  } catch (error) {
    // Notes remain available locally.
  }
}

function saveReaderNote(kind, text, eventType = "note") {
  const section = activeReadingSection();
  if (!section) {
    return;
  }
  const trimmed = text.trim();
  if (!trimmed && kind !== t("reader.favoriteSaved")) {
    return;
  }
  const notes = loadReaderNotes(section.section_id);
  notes.unshift({
    kind,
    text: trimmed || section.text.slice(0, 140),
  });
  saveReaderNotes(section.section_id, notes.slice(0, 8));
  els.readerNoteInput.value = "";
  renderReaderNotes();
  persistReaderNote(eventType, trimmed || section.text.slice(0, 140), section);
}

function updateActiveBook(book, analysis, traces = [], readingSections = []) {
  state.currentBookId = book.book_id;
  state.currentBookDetail = { book, analysis, readingSections };
  state.currentSectionIndex = 0;
  state.characters = analysis.characters ?? [];
  els.bookTitle.textContent = book.title ?? analysis.title;
  els.bookSummary.textContent = analysis.summary;
  els.readerActiveTitle.textContent = book.title ?? analysis.title;
  els.characterCount.textContent = state.characters.length;
  els.placeCount.textContent = (analysis.places ?? []).length;
  els.sceneCount.textContent = (analysis.scenes ?? []).length;
  els.readerBookMeta.innerHTML = `
    <span>${escapeHtml(book.rights ?? "rights reviewed")}</span>
    <span>${escapeHtml(book.status ?? "available")}</span>
    <span>${readingSections.length} section(s)</span>
    <span>${state.characters.length} ${t("reader.charactersReady")}</span>
  `;
  renderCharacters(state.characters);
  renderReaderProgress();
  renderReaderPage();
  renderReaderCatalog();
  if (traces.length) {
    renderTraces(traces);
  }
  hydrateReaderProgress();
}

function renderReaderCatalog() {
  els.readerCatalog.innerHTML = "";
  state.catalog.forEach((book) => {
    const item = document.createElement("article");
    const isActive = book.book_id === state.currentBookId;
    item.className = `reader-catalog-item${isActive ? " active" : ""}`;
    item.innerHTML = `
      <div>
        <small>${escapeHtml(book.typeLabel)}</small>
        <strong>${escapeHtml(book.title)}</strong>
        <p>${escapeHtml(book.rights ?? book.status ?? "")}</p>
      </div>
      <button type="button" data-reader-book="${escapeHtml(book.book_id)}">
        ${isActive ? t("reader.active") : t("reader.openBook")}
      </button>
    `;
    els.readerCatalog.appendChild(item);
  });
  if (state.catalog.length === 1) {
    const empty = document.createElement("p");
    empty.className = "reader-empty";
    empty.textContent = t("reader.noUploaded");
    els.readerCatalog.appendChild(empty);
  }
}

async function selectReaderBook(bookId) {
  if (bookId === "don-quijote") {
    const data = await api("/api/v1/demo/book");
    updateActiveBook(
      {
        book_id: data.bookId ?? "don-quijote",
        title: data.title,
        rights: t("reader.demoType"),
        status: "published",
      },
      data.analysis,
      data.traces,
      data.readingSections ?? [],
    );
    return;
  }
  const data = await api(`/api/v1/books/${encodeURIComponent(bookId)}`, {
    headers: authHeaders(),
  });
  updateActiveBook(
    data.book ?? {
      book_id: bookId,
      title: data.analysis.title,
      rights: "rights reviewed",
      status: "available",
    },
    data.analysis,
    [],
    data.readingSections ?? [],
  );
}

async function loadReaderCatalog() {
  const demoItem = {
    book_id: "don-quijote",
    title: "Don Quijote de la Mancha",
    rights: t("reader.demoType"),
    status: "published",
    typeLabel: t("reader.demoType"),
  };
  state.catalog = [demoItem];
  if (state.session?.token) {
    try {
      const catalog = await api("/api/v1/books/catalog", { headers: authHeaders() });
      const uploaded = (catalog.uploadedBooks ?? []).map((book) => ({
        ...book,
        typeLabel: t("reader.uploadedType"),
      }));
      state.catalog = [
        {
          ...catalog.demoBook,
          typeLabel: t("reader.demoType"),
        },
        ...uploaded,
      ];
    } catch (error) {
      state.catalog = [demoItem];
    }
  }
  renderReaderCatalog();
}

async function loadBook() {
  await loadAuth();
  await loadCapabilities();
  await loadSubmission();
  await loadStorage();
  await loadAdmin();
  const data = await api("/api/v1/demo/book");
  await loadReaderCatalog();
  updateActiveBook(
    {
      book_id: data.bookId ?? "don-quijote",
      title: data.title,
      rights: t("reader.demoType"),
      status: "published",
    },
    data.analysis,
    data.traces,
    data.readingSections ?? [],
  );
}

async function loadSubmission() {
  const submission = await api("/api/v1/challenge/submission");
  els.submissionSummary.innerHTML = `
    <div>
      <strong>${submission.status}</strong>
      <span>${submission.track}</span>
    </div>
    <div>
      <strong>${submission.region}</strong>
      <span>${submission.deadline}</span>
    </div>
    <div>
      <strong>${submission.recommendedJudgeAccount.name}</strong>
      <span>${submission.recommendedJudgeAccount.role}</span>
    </div>
    <div>
      <strong>public</strong>
      <span>${submission.publicDemo}</span>
    </div>
  `;
  els.submissionCriteria.innerHTML = "";
  if (submission.trackPortfolio?.length) {
    submission.trackPortfolio.forEach((track) => {
      const item = document.createElement("article");
      item.className = "catalog-item delivery-ready";
      item.innerHTML = `
        <strong>${track.track}</strong>
        <p>${track.evidence}</p>
      `;
      els.submissionCriteria.appendChild(item);
    });
  }
  submission.judgingCriteria.forEach((criterion) => {
    const item = document.createElement("article");
    item.className = "catalog-item";
    item.innerHTML = `
      <strong>${criterion.name} | ${criterion.weight}</strong>
      <p>${criterion.evidence}</p>
    `;
    els.submissionCriteria.appendChild(item);
  });
  els.submissionDeliverables.innerHTML = "";
  submission.deliverables.forEach((deliverable) => {
    const item = document.createElement("article");
    item.className =
      deliverable.status === "ready" ? "catalog-item delivery-ready" : "catalog-item";
    item.innerHTML = `
      <strong>${deliverable.name}</strong>
      <p>${deliverable.status}</p>
    `;
    els.submissionDeliverables.appendChild(item);
  });
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
    els.marketplaceExportResult.textContent = "";
    els.marketplaceExportResult.className = "access-box";
    renderMarketplace(marketplace);
  } else {
    els.marketplaceSummary.innerHTML = "";
    els.marketplaceExportResult.textContent = "";
    if (els.publisherEngagementBoard) {
      els.publisherEngagementBoard.innerHTML = "";
    }
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

function bookSignals(book) {
  return (
    book.reader_signals ?? {
      progress_events: 0,
      notes: 0,
      favorites: 0,
      readers: 0,
    }
  );
}

function totalReaderSignals(signals) {
  return (
    (signals.progress_events ?? 0) +
    (signals.notes ?? 0) +
    (signals.favorites ?? 0) +
    (signals.readers ?? 0)
  );
}

function sectionSignals(book) {
  return book.section_signals ?? [];
}

function characterSignals(book) {
  return book.character_signals ?? [];
}

function renderSectionSignalRows(book) {
  const sections = sectionSignals(book);
  if (!sections.length) {
    return `<p class="board-empty">${t("marketplace.noSectionSignals")}</p>`;
  }
  return `
    <div class="section-signal-list" aria-label="${t("marketplace.sectionSignals")}">
      ${sections
        .map(
          (section) => `
            <div class="section-signal-row">
              <strong>Section ${(section.section_index ?? 0) + 1}</strong>
              <span>${section.readers ?? 0} ${t("marketplace.readers")}</span>
              <span>${section.progress_events ?? 0} ${t("marketplace.progress")}</span>
              <span>${section.notes ?? 0} ${t("marketplace.notes")}</span>
              <span>${section.favorites ?? 0} ${t("marketplace.favorites")}</span>
            </div>
          `,
        )
        .join("")}
    </div>
  `;
}

function renderCharacterSignalRows(book) {
  const characters = characterSignals(book);
  if (!characters.length) {
    return `<p class="board-empty">${t("marketplace.noCharacterSignals")}</p>`;
  }
  return `
    <div class="character-signal-list" aria-label="${t("marketplace.characterSignals")}">
      ${characters
        .map(
          (character) => `
            <div class="character-signal-row">
              <strong>${character.character_id}</strong>
              <span>${character.mode}</span>
              <span>${character.turns ?? 0} ${t("marketplace.turns")}</span>
              <span>${character.sessions ?? 0} ${t("marketplace.sessions")}</span>
              <span>${character.preferences ?? 0} ${t("marketplace.preferences")}</span>
            </div>
          `,
        )
        .join("")}
    </div>
  `;
}

function renderPublisherEngagementBoard(catalog = []) {
  if (!els.publisherEngagementBoard) {
    return;
  }
  const activeBooks = catalog
    .map((book) => ({ book, signals: bookSignals(book) }))
    .sort((left, right) => totalReaderSignals(right.signals) - totalReaderSignals(left.signals));
  els.publisherEngagementBoard.innerHTML = `
    <div class="board-heading">
      <div>
        <p class="eyebrow">${t("marketplace.signalBoard")}</p>
        <strong>${t("marketplace.readerSignals")}</strong>
      </div>
      <span>${activeBooks.length} title(s)</span>
    </div>
  `;
  if (!activeBooks.some((item) => totalReaderSignals(item.signals) > 0)) {
    const empty = document.createElement("p");
    empty.className = "board-empty";
    empty.textContent = t("marketplace.signalBoardEmpty");
    els.publisherEngagementBoard.appendChild(empty);
  }
  activeBooks.forEach(({ book, signals }) => {
    const quality = Math.round((book.quality_score ?? 0) * 100);
    const row = document.createElement("article");
    row.className = "engagement-row";
    row.innerHTML = `
      <div class="engagement-title">
        <strong>${book.title}</strong>
        <span>${book.readiness_level ?? book.availability}</span>
      </div>
      <div class="signal-grid">
        <span><b>${signals.readers ?? 0}</b>${t("marketplace.readers")}</span>
        <span><b>${signals.progress_events ?? 0}</b>${t("marketplace.progress")}</span>
        <span><b>${signals.notes ?? 0}</b>${t("marketplace.notes")}</span>
        <span><b>${signals.favorites ?? 0}</b>${t("marketplace.favorites")}</span>
      </div>
      <div class="engagement-action">
        <span>${t("marketplace.quality")} ${quality}%</span>
        <strong>${book.business_action ?? t("marketplace.action")}</strong>
      </div>
      <details class="section-drilldown" ${sectionSignals(book).length ? "open" : ""}>
        <summary>${t("marketplace.sectionSignals")}</summary>
        ${renderSectionSignalRows(book)}
      </details>
      <details class="section-drilldown" ${characterSignals(book).length ? "open" : ""}>
        <summary>${t("marketplace.characterSignals")}</summary>
        ${renderCharacterSignalRows(book)}
      </details>
    `;
    els.publisherEngagementBoard.appendChild(row);
  });
}

function renderMarketplace(marketplace) {
  const canPublish = hasPermission("manage_catalog") || hasPermission("manage_tenants");
  if (!canPublish) {
    els.marketplaceSummary.innerHTML = "";
    if (els.publisherEngagementBoard) {
      els.publisherEngagementBoard.innerHTML = "";
    }
    els.catalogList.innerHTML = "";
    return;
  }
  const readiness = marketplace.listingReadiness;
  const operations = marketplace.operations;
  const engagementTotals = marketplace.catalog.map(bookSignals).reduce(
    (totals, book) => ({
      readers: totals.readers + (book.readers ?? 0),
      notes: totals.notes + (book.notes ?? 0),
      favorites: totals.favorites + (book.favorites ?? 0),
      progress: totals.progress + (book.progress_events ?? 0),
    }),
    { readers: 0, notes: 0, favorites: 0, progress: 0 },
  );
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
    <div>
      <strong>${engagementTotals.notes + engagementTotals.favorites + engagementTotals.progress}</strong>
      <span>${t("marketplace.readerSignals")} | ${engagementTotals.readers} reader(s)</span>
    </div>
  `;
  renderPublisherEngagementBoard(marketplace.catalog);
  els.catalogList.innerHTML = "";
  marketplace.catalog.forEach((book) => {
    const engagement = bookSignals(book);
    const item = document.createElement("article");
    item.className = "catalog-item";
    item.innerHTML = `
      <div class="catalog-title-row">
        <strong>${book.title}</strong>
        <span>${book.availability}</span>
      </div>
      <p>${book.rights} | ${book.languages.join(", ")}</p>
      <small>${book.characters} characters | ${book.scenes} scenes | ${book.agent_modes.join(
        " / ",
      )} | ${t("marketplace.quality")} ${Math.round(book.quality_score * 100)}%</small>
      <div class="catalog-signals">
        <span>${engagement.progress_events ?? 0} ${t("marketplace.progress")}</span>
        <span>${engagement.notes ?? 0} ${t("marketplace.notes")}</span>
        <span>${engagement.favorites ?? 0} ${t("marketplace.favorites")}</span>
      </div>
      <p class="catalog-action">${book.business_action ?? ""}</p>
    `;
    els.catalogList.appendChild(item);
  });
}

async function exportMarketplaceInsights() {
  if (!(hasPermission("export_catalog_insights") || hasPermission("manage_tenants"))) {
    applyAccess();
    return;
  }
  els.marketplaceExportResult.textContent = t("marketplace.exportRunning");
  els.marketplaceExportResult.className = "access-box";
  let data;
  try {
    data = await api("/api/v1/admin/marketplace/export", { headers: authHeaders() });
  } catch (error) {
    els.marketplaceExportResult.textContent = `${t("login.denied")}: ${error.message}`;
    els.marketplaceExportResult.className = "access-box locked";
    return;
  }
  els.marketplaceExportResult.innerHTML = `
    <strong>${t("marketplace.exportReady")}: ${data.exportType}</strong>
    <p>${data.tenant.name} | ${data.listingReadiness.marketplaceStatus}</p>
    <p>${data.totals.books} title(s) | ${data.totals.readerSignals} reader signal(s) | ${
      data.totals.characterTurns
    } character turn(s)</p>
    <p>${data.generatedAt}</p>
  `;
  els.marketplaceExportResult.className = "access-box granted";
}

async function downloadMarketplaceCsv() {
  if (!(hasPermission("export_catalog_insights") || hasPermission("manage_tenants"))) {
    applyAccess();
    return;
  }
  els.marketplaceExportResult.textContent = t("marketplace.csvRunning");
  els.marketplaceExportResult.className = "access-box";
  let response;
  try {
    response = await fetch("/api/v1/admin/marketplace/export.csv", {
      headers: authHeaders(),
    });
  } catch (error) {
    els.marketplaceExportResult.textContent = `${t("login.denied")}: ${error.message}`;
    els.marketplaceExportResult.className = "access-box locked";
    return;
  }
  if (!response.ok) {
    els.marketplaceExportResult.textContent = `${t("login.denied")}: ${response.status}`;
    els.marketplaceExportResult.className = "access-box locked";
    return;
  }
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "stormsboys-marketplace-insights.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  els.marketplaceExportResult.innerHTML = `
    <strong>${t("marketplace.csvReady")}</strong>
    <p>stormsboys-marketplace-insights.csv</p>
  `;
  els.marketplaceExportResult.className = "access-box granted";
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

async function cleanupDemoSession() {
  if (!hasPermission("manage_tenants")) {
    applyAccess();
    return;
  }
  const sessionId = els.cleanupSessionInput.value.trim();
  if (!sessionId) {
    els.cleanupResult.textContent = "Session id is required.";
    els.cleanupResult.className = "access-box locked";
    return;
  }
  els.cleanupResult.textContent = t("operations.cleanupRunning");
  els.cleanupResult.className = "access-box";
  let data;
  try {
    data = await api(`/api/v1/admin/demo-sessions/${encodeURIComponent(sessionId)}`, {
      method: "DELETE",
      headers: authHeaders(),
    });
  } catch (error) {
    els.cleanupResult.textContent = `${t("login.denied")}: ${error.message}`;
    els.cleanupResult.className = "access-box locked";
    return;
  }
  els.cleanupResult.innerHTML = `
    <strong>${t("operations.cleanupDone")}: ${data.session_id}</strong>
    <p>${data.provider} | ${data.scope}</p>
    <p>${data.deleted.memory_events} memory event(s) | ${
      data.deleted.fiction_branches
    } fiction branch(es)</p>
  `;
  els.cleanupResult.className = "access-box granted";
  await loadCharacterHistory(sessionId);
  await loadFictionTimeline(sessionId);
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
  if (data.uploadedCatalog?.length) {
    els.authorResponse.insertAdjacentHTML(
      "beforeend",
      `<p><strong>Uploaded catalog:</strong> ${data.uploadedCatalog
        .map((book) => `${book.title} (${book.characters} agents)`)
        .join(", ")}</p>`,
    );
  }
  renderTraces(data.traces);
}

async function uploadBook() {
  if (!(hasPermission("upload_owned_books") || hasPermission("manage_tenants"))) {
    applyAccess();
    return;
  }
  const file = els.uploadFile.files?.[0];
  if (!file) {
    els.authorResponse.textContent = "Choose a .txt, .md, or .pdf manuscript first.";
    return;
  }
  const form = new FormData();
  form.append("title", els.uploadTitle.value.trim() || file.name);
  form.append("author", els.uploadAuthor.value.trim() || "Unknown");
  form.append("rights", els.uploadRights.value);
  form.append("language", els.languageSelect.value);
  form.append("file", file);
  els.authorResponse.textContent = "Uploading, chunking, embedding, and generating agents.";
  let data;
  try {
    data = await api("/api/v1/books/upload", {
      method: "POST",
      headers: authHeaders(),
      body: form,
    });
  } catch (error) {
    els.authorResponse.textContent = `Upload failed: ${error.message}`;
    return;
  }
  els.authorResponse.innerHTML = `
    <strong>${data.book.title} | ${data.book.status}</strong>
    <p>${data.provider} | ${data.book.sections} section(s) | ${
      data.book.characters
    } character agent(s)</p>
    <p>${data.pipeline.ingestion} | ${data.pipeline.analysis} | ${data.pipeline.catalog}</p>
    <p>Added to the reader catalog as <strong>${data.book.book_id}</strong>.</p>
  `;
  await loadReaderCatalog();
  updateActiveBook(
    {
      book_id: data.book.book_id,
      title: data.book.title,
      rights: data.book.rights,
      status: data.book.status,
    },
    data.analysis,
    data.traces,
    data.readingSections ?? [],
  );
  await loadAdmin();
}

async function loadCapabilities() {
  const data = await api("/api/v1/challenge/capabilities");
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
  const sessionId = `${state.session?.user?.user_id ?? "anonymous"}-${state.currentBookId}-${
    els.characterSelect.value
  }`;
  state.currentCharacterSessionId = sessionId;
  const data = await api("/api/v1/demo/chat/character", {
    method: "POST",
    body: JSON.stringify({
      book_id: state.currentBookId,
      character_id: els.characterSelect.value,
      mode: els.modeSelect.value,
      language: els.languageSelect.value,
      session_id: sessionId,
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
  renderCharacterEvidence(data);
  await loadCharacterHistory(sessionId);
  await loadFictionTimeline(sessionId);
  renderTraces(data.traces);
}

function renderCharacterEvidence(data) {
  const profile = data.characterProfile;
  const ocean = profile.psychological_profile?.ocean ?? {};
  els.characterPsychology.innerHTML = `
    <p><strong>Speech:</strong> ${profile.speech_style}</p>
    <p><strong>Emotion:</strong> ${profile.emotional_baseline}</p>
    <p><strong>Desire:</strong> ${profile.desires?.[0] ?? "n/a"}</p>
    <p><strong>Fear:</strong> ${profile.fears?.[0] ?? "n/a"}</p>
    <p><strong>OCEAN:</strong> ${Object.entries(ocean)
      .map(([key, value]) => `${key}: ${value}`)
      .join(" | ")}</p>
  `;
  els.characterMemory.innerHTML = `
    <p><strong>${data.memory.turn_count}</strong> remembered turn(s)</p>
    <p>${data.memory.relationship_summary}</p>
    <p><strong>Preferences:</strong> ${
      data.memory.learned_reader_preferences.join(", ") || "none learned yet"
    }</p>
    <p><strong>Canon memory:</strong> ${data.memory.canon_memory.length}</p>
    <p><strong>Fiction memory:</strong> ${data.memory.fiction_memory.length}</p>
  `;
  els.characterCitations.innerHTML =
    data.reply.citations.length > 0
      ? data.reply.citations.map((citation) => `<span>${citation}</span>`).join("")
      : "<p>No citations returned for this turn.</p>";
}

async function loadCharacterHistory(sessionId) {
  const params = new URLSearchParams({
    session_id: sessionId,
    character_id: els.characterSelect.value,
    mode: els.modeSelect.value,
    limit: "5",
  });
  const history = await api(`/api/v1/demo/chat/memory?${params.toString()}`);
  els.characterHistory.innerHTML = `
    <p><strong>${history.provider}</strong></p>
    ${
      history.events.length
        ? history.events
            .map(
              (event) => `
                <div class="memory-event">
                  <strong>${event.question}</strong>
                  <p>${event.memory_line}</p>
                  ${
                    event.reader_preference
                      ? `<span>${event.reader_preference}</span>`
                      : ""
                  }
                </div>
              `,
            )
            .join("")
        : "<p>No memory turns recorded for this mode yet.</p>"
    }
  `;
}

async function loadFictionTimeline(sessionId) {
  state.currentCharacterSessionId = sessionId;
  els.fictionTimeline.dataset.sessionId = sessionId;
  const params = new URLSearchParams({
    session_id: sessionId,
    character_id: els.characterSelect.value,
    limit: "5",
  });
  const timeline = await api(`/api/v1/demo/fiction/branches?${params.toString()}`);
  const branches = timeline.branches ?? [];
  els.fictionTimeline.innerHTML = `
    <p><strong>${escapeHtml(timeline.provider)}</strong></p>
    ${
      branches.length
        ? branches
            .map(
              (branch) => `
                <div class="fiction-branch">
                  <header>
                    <strong>${escapeHtml(branch.branch_id)}</strong>
                  </header>
                  <p>${escapeHtml(branch.seed_prompt)}</p>
                  <span>${escapeHtml(
                    branch.canon_anchor_citations.join(", ") || "no canon anchor",
                  )}</span>
                  <details class="fiction-detail">
                    <summary>Open</summary>
                    <p><strong>Premise:</strong> ${escapeHtml(branch.premise)}</p>
                    <p><strong>Continuation:</strong> ${escapeHtml(branch.continuation)}</p>
                    <p><strong>Canon anchors:</strong> ${escapeHtml(
                      branch.canon_anchor_citations.join(", ") || "no canon anchor",
                    )}</p>
                  </details>
                </div>
              `,
            )
            .join("")
        : "<p>No fiction branches recorded for this character yet.</p>"
    }
  `;
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
document.querySelectorAll("[data-jump-view]").forEach((item) => {
  item.addEventListener("click", () => setView(item.dataset.jumpView));
});
els.languageSelect.addEventListener("change", () => applyLanguage(els.languageSelect.value));
els.runScene.addEventListener("click", runScene);
els.runNarration.addEventListener("click", runNarration);
els.runAuthorWorkflow.addEventListener("click", runAuthorWorkflow);
els.uploadBook.addEventListener("click", uploadBook);
els.runPublisher.addEventListener("click", runPublisher);
els.refreshAdmin.addEventListener("click", loadAdmin);
els.exportMarketplace.addEventListener("click", exportMarketplaceInsights);
els.downloadMarketplaceCsv.addEventListener("click", downloadMarketplaceCsv);
els.refreshOperations.addEventListener("click", loadAdmin);
els.cleanupSession.addEventListener("click", cleanupDemoSession);
els.runEvaluation.addEventListener("click", runEvaluation);
els.refreshDemo.addEventListener("click", loadBook);
els.readerCatalog.addEventListener("click", (event) => {
  const button = event.target.closest("[data-reader-book]");
  if (!button) {
    return;
  }
  selectReaderBook(button.dataset.readerBook);
});
els.readerProgressInput.addEventListener("input", () => {
  saveCurrentBookProgress(els.readerProgressInput.value);
});
els.readerPrevSection.addEventListener("click", () => {
  goToReaderSection(state.currentSectionIndex - 1);
});
els.readerNextSection.addEventListener("click", () => {
  goToReaderSection(state.currentSectionIndex + 1);
});
els.saveReaderNote.addEventListener("click", () => {
  saveReaderNote(t("reader.noteLabel"), els.readerNoteInput.value);
});
els.markReaderFavorite.addEventListener("click", () => {
  saveReaderNote(t("reader.favoriteSaved"), "", "favorite");
});

applyLanguage(els.languageSelect.value);
renderShell();
setView("reader");

loadBook()
  .then(runEvaluation)
  .catch((error) => {
    els.bookTitle.textContent = "Demo unavailable";
    els.bookSummary.textContent = error.message;
  });
