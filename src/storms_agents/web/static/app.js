const state = {
  characters: [],
};

const els = {
  bookTitle: document.querySelector("#bookTitle"),
  bookSummary: document.querySelector("#bookSummary"),
  characterCount: document.querySelector("#characterCount"),
  placeCount: document.querySelector("#placeCount"),
  sceneCount: document.querySelector("#sceneCount"),
  characterSelect: document.querySelector("#characterSelect"),
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
  await loadCapabilities();
  await loadStorage();
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
  els.characterResponse.textContent = "Running retrieval, character response, and consistency check.";
  const data = await api("/api/v1/demo/chat/character", {
    method: "POST",
    body: JSON.stringify({
      character_id: els.characterSelect.value,
      question,
    }),
  });
  els.characterResponse.innerHTML = `
    <strong>${data.reply.character_name}</strong>
    <p>${data.reply.response}</p>
    <p>Consistency: ${data.consistency.passed ? "passed" : "needs review"}</p>
  `;
  renderTraces(data.traces);
}

async function runScene() {
  els.sceneResponse.textContent = "Coordinating scene agents.";
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
  els.narrationResponse.textContent = "Preparing narration handoff.";
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
  els.publisherResponse.textContent = "Generating publisher insights.";
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
  els.evaluationResults.textContent = "Running before and after evaluation.";
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
  els.questionInput.value = "Tell me what happens ten years after the ending.";
  askCharacter(els.questionInput.value);
});
els.runScene.addEventListener("click", runScene);
els.runNarration.addEventListener("click", runNarration);
els.runPublisher.addEventListener("click", runPublisher);
els.runEvaluation.addEventListener("click", runEvaluation);
els.refreshDemo.addEventListener("click", loadBook);

loadBook()
  .then(runEvaluation)
  .catch((error) => {
    els.bookTitle.textContent = "Demo unavailable";
    els.bookSummary.textContent = error.message;
  });
