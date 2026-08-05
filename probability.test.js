import assert from "node:assert/strict";
import test from "node:test";
import {exactDrawProbability, monteCarloProbability, validateModelInput} from "./probability.js";

function permutations(values) {
  if (values.length <= 1) return [values];
  const result = [];
  const used = new Set();
  for (let i=0; i<values.length; i+=1) {
    if (used.has(values[i])) continue;
    used.add(values[i]);
    const rest = values.slice(0,i).concat(values.slice(i+1));
    for (const tail of permutations(rest)) result.push([values[i], ...tail]);
  }
  return result;
}
function brute(deckSize, drawCounts) {
  const cards = [];
  const normals = deckSize - drawCounts.reduce((a,b)=>a+b,0);
  for (let i=0;i<normals;i+=1) cards.push(0);
  drawCounts.forEach((count, idx) => { for(let i=0;i<count;i+=1) cards.push(idx+1); });
  const all = permutations(cards);
  let ok=0;
  for (const deck of all) {
    let available=Math.min(5, deck.length), cursor=0;
    while (available>0 && cursor<deck.length) available=available-1+deck[cursor++];
    if (cursor===deck.length) ok+=1;
  }
  return ok/all.length;
}

test("exact DP matches complete unique-permutation enumeration for decks 0..9", () => {
  for (let n=0;n<=9;n+=1) for (let labs=0;labs<=n;labs+=1) {
    const counts=[0,labs,0,0,0];
    assert.ok(Math.abs(exactDrawProbability(n, counts)-brute(n, counts)) < 1e-12, `${n}/${labs}`);
  }
});
test("validation rejects invalid inputs", () => {
  assert.throws(()=>validateModelInput(10,[0,11,0,0,0]), RangeError);
  assert.throws(()=>validateModelInput(-1,[0,0,0,0,0]), RangeError);
  assert.throws(()=>validateModelInput(10.5,[0,0,0,0,0]), RangeError);
});
test("seeded Monte Carlo covers exact value within its 95% interval", () => {
  const exact=exactDrawProbability(20,[0,8,0,0,0]);
  const mc=monteCarloProbability(20,[0,8,0,0,0],{trials:100000,seed:2306});
  assert.ok(exact >= mc.ci95[0] && exact <= mc.ci95[1], `${exact} not in ${mc.ci95}`);
});
