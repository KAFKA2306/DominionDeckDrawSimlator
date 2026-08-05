export const MODEL = Object.freeze({
  initialHandSize: 5,
  actionLimit: "unlimited",
  reshuffle: false,
  description: "A uniformly random deck order. Processing a card with draw value d consumes one available card and adds d available cards."
});

export function validateModelInput(deckSize, drawCounts, maxDeckSize = 200) {
  if (!Number.isInteger(deckSize) || deckSize < 0 || deckSize > maxDeckSize) {
    throw new RangeError(`deckSize must be an integer from 0 to ${maxDeckSize}`);
  }
  if (!Array.isArray(drawCounts) || drawCounts.length !== 5 ||
      drawCounts.some((v) => !Number.isInteger(v) || v < 0)) {
    throw new RangeError("drawCounts must contain five non-negative integers");
  }
  const specialCards = drawCounts.reduce((a, b) => a + b, 0);
  if (specialCards > deckSize) {
    throw new RangeError("the number of draw cards cannot exceed deckSize");
  }
}

export function exactDrawProbability(deckSize, drawCounts, initialHandSize = MODEL.initialHandSize) {
  validateModelInput(deckSize, drawCounts);
  if (!Number.isInteger(initialHandSize) || initialHandSize < 0) {
    throw new RangeError("initialHandSize must be a non-negative integer");
  }
  if (deckSize === 0 || deckSize <= initialHandSize) return 1;

  const counts = [deckSize - drawCounts.reduce((a, b) => a + b, 0), ...drawCounts];
  const memo = new Map();

  function solve(remaining, available) {
    const total = remaining.reduce((a, b) => a + b, 0);
    if (total === 0) return 1;
    if (available === 0) return 0;
    const key = `${remaining.join(",")}|${available}`;
    if (memo.has(key)) return memo.get(key);

    let probability = 0;
    for (let draw = 0; draw < remaining.length; draw += 1) {
      const count = remaining[draw];
      if (count === 0) continue;
      const next = remaining.slice();
      next[draw] -= 1;
      probability += (count / total) * solve(next, available - 1 + draw);
    }
    memo.set(key, probability);
    return probability;
  }

  return solve(counts, Math.min(initialHandSize, deckSize));
}

export function mulberry32(seed) {
  let state = seed >>> 0;
  return () => {
    state += 0x6D2B79F5;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function monteCarloProbability(deckSize, drawCounts, {trials = 10000, seed = 1} = {}) {
  validateModelInput(deckSize, drawCounts);
  if (!Number.isInteger(trials) || trials <= 0 || trials > 1_000_000) {
    throw new RangeError("trials must be an integer from 1 to 1,000,000");
  }
  const cards = [deckSize - drawCounts.reduce((a,b)=>a+b,0)];
  drawCounts.forEach((count) => cards.push(count));
  const rng = mulberry32(seed);
  let success = 0;
  for (let trial = 0; trial < trials; trial += 1) {
    const deck = [];
    cards.forEach((count, draw) => {
      for (let i=0; i<count; i+=1) deck.push(draw);
    });
    for (let i=deck.length-1; i>0; i-=1) {
      const j = Math.floor(rng() * (i+1));
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }
    let available = Math.min(MODEL.initialHandSize, deck.length);
    let cursor = 0;
    while (available > 0 && cursor < deck.length) {
      available = available - 1 + deck[cursor];
      cursor += 1;
    }
    if (cursor === deck.length) success += 1;
  }
  const estimate = success / trials;
  const standardError = Math.sqrt(estimate * (1-estimate) / trials);
  return {estimate, trials, seed, standardError, ci95: [
    Math.max(0, estimate - 1.96*standardError),
    Math.min(1, estimate + 1.96*standardError)
  ]};
}
