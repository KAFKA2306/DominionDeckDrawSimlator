import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import test from "node:test";

const html = await readFile(new URL("./index.html", import.meta.url), "utf8");
const readme = await readFile(new URL("./README.md", import.meta.url), "utf8");

test("public calculator exposes share and sponsor entry points", () => {
  assert.match(html, /id="copyShare"/);
  assert.match(html, /共有URLをコピー/);
  assert.match(html, /\.\/share-state\.js/);
  assert.match(html, /issues\/new\?title=スポンサー・共同企画の相談/);
  assert.match(html, /公開Issueのため/);
});

test("README starts with the canonical production URL", () => {
  assert.equal(readme.split(/\r?\n/, 1)[0], "https://kafka2306.github.io/DominionDeckDrawSimlator/");
});
