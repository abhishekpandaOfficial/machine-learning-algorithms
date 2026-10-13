import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, "../..");
const sourcePath = resolve(repoRoot, "knowledge-bank/foundations/ml-foundations-001-050.md");
const outputPath = resolve(here, "../src/data/questions.json");
const source = await readFile(sourcePath, "utf8");
const blocks = source.split(/(?=^## ML-[A-Z]+-\\d{3} — )/m).filter((block) => /^## ML-[A-Z]+-\\d{3} — /m.test(block));

function section(block, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
  const match = block.match(new RegExp("^### " + escaped + "\\s*\\n([\\s\\S]*?)(?=^### |^---\\s*$|$)", "m"));
  return match ? match[1].trim() : "";
}
const questions = blocks.map((block) => {
  const titleMatch = block.match(/^## (ML-[A-Z]+-\\d{3}) — (.+)$/m);
  const meta = block.match(/^\\*\\*Difficulty:\\*\\* (.+?) · \\*\\*Type:\\*\\* (.+?) · \\*\\*Tags:\\*\\* (.+)$/m);
  if (!titleMatch || !meta) throw new Error("Question missing ID/title/metadata: " + block.slice(0, 100));
  return {
    id: titleMatch[1],
    title: titleMatch[2].trim(),
    difficulty: meta[1].trim(),
    type: meta[2].trim(),
    tags: meta[3].split(",").map((tag) => tag.trim()).filter(Boolean),
    answer: section(block, "Answer"),
    example: section(block, "Example"),
    pitfall: section(block, "Common pitfall"),
    practice: section(block, "Practice"),
  };
});
const ids = questions.map((q) => q.id);
if (new Set(ids).size !== ids.length) throw new Error("Duplicate question IDs detected.");
for (const q of questions) {
  for (const key of ["answer", "example", "pitfall", "practice"]) {
    if (!q[key]) throw new Error(q.id + " is missing section: " + key);
  }
}
await writeFile(outputPath, JSON.stringify(questions, null, 2) + "\\n");
console.log(`Built ${questions.length} questions into ${outputPath}`);
