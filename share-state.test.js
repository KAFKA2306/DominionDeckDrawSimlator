import assert from "node:assert/strict";
import test from "node:test";
import {
  MODEL_VERSION,
  decodeCalculationState,
  encodeCalculationState,
  updateCalculationSearch,
} from "./share-state.js";

test("calculation state round-trips through query parameters", () => {
  const encoded = encodeCalculationState(20, [0, 8, 0, 0, 0]);
  assert.equal(encoded.get("model"), MODEL_VERSION);
  assert.deepEqual(decodeCalculationState(encoded), {
    deckSize: 20,
    drawCounts: [0, 8, 0, 0, 0],
  });
});

test("shared state rejects unknown versions and invalid inputs", () => {
  assert.throws(
    () => decodeCalculationState("model=2&deck=20&draw1=0&draw2=8&draw3=0&draw4=0&draw5=0"),
    RangeError,
  );
  assert.throws(
    () => decodeCalculationState("model=1&deck=20&draw1=0&draw2=21&draw3=0&draw4=0&draw5=0"),
    RangeError,
  );
});

test("updating calculation state preserves unrelated query parameters", () => {
  const updated = new URLSearchParams(
    updateCalculationSearch("utm_source=creator", 18, [0, 6, 0, 0, 0]),
  );
  assert.equal(updated.get("utm_source"), "creator");
  assert.equal(updated.get("model"), MODEL_VERSION);
  assert.equal(updated.get("deck"), "18");
  assert.equal(updated.get("draw2"), "6");
});
