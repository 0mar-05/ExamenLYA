const initialGrid = document.getElementById("initialGrid");
const goalGrid = document.getElementById("goalGrid");
const solveForm = document.getElementById("solveForm");
const resultSection = document.getElementById("result");
const resultMeta = document.getElementById("resultMeta");
const resultFull = document.getElementById("resultFull");
const resultSteps = document.getElementById("resultSteps");

const createSelect = (name) => {
    const select = document.createElement("select");
    select.name = name;
    select.dataset.group = name.includes("initial") ? "initial" : "goal";

    const empty = document.createElement("option");
    empty.value = "";
    empty.textContent = "Seleccionar";
    select.appendChild(empty);

    for (let i = 1; i <= 4; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        select.appendChild(option);
    }

    select.addEventListener("change", updateOptions);
    return select;
};

const buildGrid = (container, prefix) => {
    for (let index = 0; index < 4; index += 1) {
        const select = createSelect(`${prefix}-${index}`);
        container.appendChild(select);
    }
};

const updateOptions = () => {
    ["initial", "goal"].forEach((group) => {
        const selects = Array.from(document.querySelectorAll(`select[data-group='${group}']`));
        const chosen = selects.map((el) => el.value).filter(Boolean);

        selects.forEach((select) => {
            Array.from(select.options).forEach((option) => {
                if (!option.value) {
                    option.disabled = false;
                    return;
                }
                const isSelected = option.value === select.value;
                option.disabled = !isSelected && chosen.includes(option.value);
            });
        });
    });
};

const readState = (prefix) => {
    const selects = Array.from(document.querySelectorAll(`select[name^='${prefix}']`));
    return selects.map((select) => Number(select.value));
};

const isComplete = (state) => state.every((value) => Number.isInteger(value) && value >= 1 && value <= 4);

const showResult = (payload) => {
    resultMeta.textContent = `Inicial: [${payload.initial.join(", ")}] · Objetivo: [${payload.goal.join(", ")}]`;
    resultFull.textContent = payload.results
        .map((algorithmResult) => `${algorithmResult.algorithm}: [ ${algorithmResult.steps.map((step) => `[${step.join(", ")}]`).join(", ")} ]`)
        .join("\n\n");
    resultSteps.innerHTML = "";

    payload.results.forEach((algorithmResult) => {
        const algorithmCard = document.createElement("div");
        algorithmCard.className = "step-card";
        algorithmCard.innerHTML = `
            <strong>${algorithmResult.algorithm} · Pasos: ${algorithmResult.length}</strong>
            <pre>[ ${algorithmResult.steps.map((step) => `[${step.join(", ")}]`).join(", ")} ]</pre>`;
        resultSteps.appendChild(algorithmCard);
    });

    resultSection.classList.remove("hidden");
};

const showError = (message) => {
    resultMeta.textContent = message;
    resultFull.textContent = "";
    resultSteps.innerHTML = "";
    resultSection.classList.remove("hidden");
};

solveForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const initial = readState("initial");
    const goal = readState("goal");

    if (!isComplete(initial) || !isComplete(goal)) {
        showError("Por favor completa los 4 números en ambos estados.");
        return;
    }

    const response = await fetch("/api/solve-all", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ initial, goal }),
    });

    const data = await response.json();
    if (!response.ok) {
        showError(data.error || "Ocurrió un error al procesar la solicitud.");
        return;
    }

    showResult(data);
});

buildGrid(initialGrid, "initial");
buildGrid(goalGrid, "goal");
updateOptions();
