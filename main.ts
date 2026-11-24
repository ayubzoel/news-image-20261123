// main.ts — graded entrypoint for news-image-20261123.
// Copies the pre-rendered newspaper page (entry.png, drawn locally by
// poster.py from verified 23 November 2026 news research) into the grader's
// output directory. Node 22 standard library only; no network, no deps.

import { copyFileSync, readFileSync, statSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024; // 1 MiB cap from the bounty gate
const ART_NAME = "entry.png";

function fail(message: string): never {
  console.error(`[news-poster] error: ${message}`);
  process.exit(1);
}

function repoDir(): string {
  return dirname(fileURLToPath(import.meta.url));
}

function checkArtwork(path: string): number {
  if (!existsSync(path)) fail(`artwork missing at ${path}`);
  const head = readFileSync(path, { flag: "r" });
  const sig = head.subarray(0, PNG_MAGIC.length);
  if (!sig.equals(PNG_MAGIC)) fail("artwork is not a PNG (bad signature)");
  const size = statSync(path).size;
  if (size > MAX_BYTES) fail(`artwork is ${size} bytes, over the 1 MiB cap`);
  return size;
}

function publish(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR;
  if (!outDir) fail("MAKEFUN_OUTPUT_DIR is not set");
  const source = join(repoDir(), ART_NAME);
  const size = checkArtwork(source);
  mkdirSync(resolve(outDir), { recursive: true });
  const target = join(resolve(outDir), ART_NAME);
  copyFileSync(source, target);
  const written = statSync(target).size;
  if (written !== size) fail("copy mismatch: output size differs from source");
  console.log(`[news-poster] wrote ${target} (${written} bytes, PNG OK)`);
}

publish();
