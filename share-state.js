import {validateModelInput} from "./probability.js";

export const MODEL_VERSION = "1";
const DRAW_PARAMETERS = ["draw1", "draw2", "draw3", "draw4", "draw5"];

function readInteger(params, name) {
  const raw = params.get(name);
  if (raw === null || raw.trim() === "") {
    throw new RangeError(`共有URLに${name}がありません`);
  }
  const value = Number(raw);
  if (!Number.isInteger(value)) {
    throw new RangeError(`共有URLの${name}が不正です`);
  }
  return value;
}

export function encodeCalculationState(deckSize, drawCounts) {
  validateModelInput(deckSize, drawCounts);
  const params = new URLSearchParams();
  params.set("model", MODEL_VERSION);
  params.set("deck", String(deckSize));
  DRAW_PARAMETERS.forEach((name, index) => params.set(name, String(drawCounts[index])));
  return params;
}

export function decodeCalculationState(search) {
  const params = search instanceof URLSearchParams ? search : new URLSearchParams(search);
  if (!params.has("model")) return null;
  if (params.get("model") !== MODEL_VERSION) {
    throw new RangeError("共有URLの計算モデルversionに対応していません");
  }

  const deckSize = readInteger(params, "deck");
  const drawCounts = DRAW_PARAMETERS.map((name) => readInteger(params, name));
  validateModelInput(deckSize, drawCounts);
  return {deckSize, drawCounts};
}

export function updateCalculationSearch(search, deckSize, drawCounts) {
  const params = new URLSearchParams(search);
  const state = encodeCalculationState(deckSize, drawCounts);
  for (const [name, value] of state) params.set(name, value);
  return params.toString();
}
