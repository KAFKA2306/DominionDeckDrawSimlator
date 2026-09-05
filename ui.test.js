import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import test from "node:test";

const html = await readFile(new URL("./index.html", import.meta.url), "utf8");
const readme = await readFile(new URL("./README.md", import.meta.url), "utf8");

test("public calculator exposes share and sponsor entry points", () => {
  assert.match(html, /id="copyShare"/);
  assert.match(html, /この条件のURLをコピー/);
  assert.match(html, /\.\/share-state\.js/);
  assert.match(html, /issues\/new\?title=スポンサー・共同企画の相談/);
  assert.match(html, /公開Issueのため/);
});

test("README starts with the canonical production URL", () => {
  assert.equal(readme.split(/\r?\n/, 1)[0], "https://kafka2306.github.io/DominionDeckDrawSimlator/");
});

test("primary decision path shows result before the secondary table", () => {
  assert.ok(html.indexOf('class="panel result-panel"') < html.indexOf('class="secondary"'));
  assert.match(html, /id="probability"/);
  assert.match(html, /id="sensitivity"/);
  assert.match(html, /研究所±1枚/);
});

test("sensitivity comparison reuses the exact probability model", () => {
  assert.match(html, /function renderSensitivity\(deck,drawCounts,current\)/);
  assert.match(html, /minus=exactDrawProbability\(deck,next\)/);
  assert.match(html, /plus=exactDrawProbability\(deck,next\)/);
  assert.match(html, /drawCounts\[1\]/);
  assert.match(html, /delta\.toFixed\(3\) pt/);
});

test("design authority foundation values are reused without a second token file", () => {
  for (const value of ["#F7F5EF","#FFFFFF","#17233F","#667085","#D9D6CE","#2563EB","#B91C1C"]) {
    assert.match(html, new RegExp(value, "i"));
  }
  assert.match(html, /--touch-target:44px/);
  assert.match(html, /:focus-visible/);
});

test("invalid calculation fails visibly", () => {
  assert.match(html, /showError\(result,e\)/);
  assert.match(html, /probability\.textContent="—"/);
  assert.match(html, /\.error\{color:var\(--danger\)!important\}/);
});
