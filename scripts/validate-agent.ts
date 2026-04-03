#!/usr/bin/env bun
/** Lint agent project vs AGENT_SPEC.md. Usage: bun scripts/validate-agent.ts [path] */
import * as fs from "node:fs";
import * as path from "node:path";

type S = "Pass" | "Warn" | "Fail";
let hasFail = false;
const out = (n: string, s: S, m: string) => {
  if (s === "Fail") hasFail = true;
  console.log(`[${s}] ${n}: ${m}`);
};
const root = path.resolve(process.argv[2] ?? ".");
const PROMPTS = ["system-prompt.md", "SYSTEM_PROMPT.md", "system_prompt.md", "prompts/system.md", "prompts/system-prompt.md"];
const SECRET_RES = [
  /\bsk-[a-zA-Z0-9]{10,}\b/, /\bAKIA[0-9A-Z]{16}\b/, /\bAIza[0-9A-Za-z_-]{20,}\b/,
  /\bghp_[a-zA-Z0-9]{20,}\b/, /\bgho_[a-zA-Z0-9]{20,}\b/, /\bxox[baprs]-[a-zA-Z0-9-]{10,}\b/,
  /\b-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /(?:OPENAI|ANTHROPIC|AWS_SECRET|API_KEY|PASSWORD)\s*=\s*["']?[^\s#'"]{8,}/i,
];

const exists = (p: string) => {
  try {
    fs.accessSync(p);
    return true;
  } catch {
    return false;
  }
};
const read = (p: string) => {
  try {
    return fs.readFileSync(p, "utf8");
  } catch {
    return null;
  }
};
const collectText = (dir: string, acc: string[], depth = 0) => {
  if (depth > 6 || !exists(dir)) return;
  for (const name of fs.readdirSync(dir)) {
    if (name === "node_modules" || name === ".git") continue;
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) collectText(p, acc, depth + 1);
    else if (/\.(md|txt|json|yaml|yml|ts|tsx|js|jsx|py|toml|env)$/i.test(name)) acc.push(p);
  }
};
const countAllFiles = (dir: string): number => {
  if (!exists(dir)) return 0;
  let n = 0;
  const go = (d: string) => {
    for (const x of fs.readdirSync(d)) {
      const p = path.join(d, x);
      fs.statSync(p).isDirectory() ? go(p) : n++;
    }
  };
  go(dir);
  return n;
};

if (!exists(root) || !fs.statSync(root).isDirectory()) {
  console.error(`Not a directory: ${root}`);
  process.exit(2);
}

const readmePath = path.join(root, "README.md");
if (!exists(readmePath)) out("README.md", "Fail", "missing");
else {
  const txt = read(readmePath) ?? "";
  const arch = /^#{1,3}\s+.*architecture/im.test(txt);
  out("README architecture", arch ? "Pass" : "Warn", arch ? "heading found" : "add Architecture section (AGENT_SPEC)");
}

let sysPath: string | null = null;
for (const rel of PROMPTS) {
  const f = path.join(root, rel);
  if (exists(f) && fs.statSync(f).isFile()) {
    sysPath = f;
    break;
  }
}
if (!sysPath) out("System prompt file", "Fail", `need one of: ${PROMPTS.join(", ")}`);
else out("System prompt file", "Pass", path.relative(root, sysPath));

const toolsPath = path.join(root, "tools");
const toolN = exists(toolsPath) && fs.statSync(toolsPath).isDirectory()
  ? fs.readdirSync(toolsPath).filter((x) => !x.startsWith(".")).length
  : 0;
out("Tool definitions", toolN >= 1 ? "Pass" : "Fail", toolN >= 1 ? `${toolN} in tools/` : "need >=1 entry in tools/");

const testN = countAllFiles(path.join(root, "tests"));
out("Tests directory", testN > 0 ? "Pass" : "Fail", testN > 0 ? `${testN} file(s)` : "missing or empty");

const srcPath = path.join(root, "src");
const srcExists = exists(srcPath) && fs.statSync(srcPath).isDirectory();
const srcN = srcExists ? fs.readdirSync(srcPath).filter((x) => !x.startsWith(".")).length : 0;
out("Source directory", srcN > 0 ? "Pass" : "Warn", srcN > 0 ? `${srcN} file(s) in src/` : "missing or empty src/ (AGENT_SPEC canonical structure)");

const deployPath = path.join(root, "deploy");
const deployExists = exists(deployPath) && fs.statSync(deployPath).isDirectory();
out("Deploy directory", deployExists ? "Pass" : "Warn", deployExists ? "present" : "missing deploy/ (AGENT_SPEC canonical structure)");

if (exists(path.join(root, ".env"))) out("Secrets / .env", "Fail", ".env committed; use .env.example");
else {
  const files: string[] = [];
  collectText(root, files);
  let hit: string | null = null;
  outer: for (const f of files) {
    if (path.basename(f) === "package-lock.json") continue;
    const body = read(f);
    if (!body || body.length > 500_000) continue;
    for (const re of SECRET_RES) {
      if (re.test(body)) {
        hit = path.relative(root, f);
        break outer;
      }
    }
  }
  out("Secret patterns", hit ? "Fail" : "Pass", hit ? `match in ${hit}` : "none in scanned text files");
}

const promptText = sysPath ? read(sysPath) ?? "" : "";
const persona = /\b(persona|role|identity)\b/i.test(promptText);
const constraints = /\b(constraint|must not|do not|never|rules?)\b/i.test(promptText);
const toolsSec = /\b(tools?|function calling|mcp|invoke)\b/i.test(promptText);
if (!sysPath) out("Prompt sections", "Fail", "no system prompt");
else {
  const ok = persona && constraints && toolsSec;
  out(
    "Prompt sections",
    ok ? "Pass" : "Warn",
    ok ? "persona, constraints, tool cues" : `persona=${persona} constraints=${constraints} tools=${toolsSec}`,
  );
}

// CLASSic-surfaced checks (Cycle 4)
const costAware = /\b(cost|budget|token|expense|price|spending)\b/i.test(promptText);
out("Cost awareness", costAware ? "Pass" : "Warn", costAware ? "cost/budget language found in prompt" : "no cost/budget awareness in system prompt (CLASSic)");

const outputVal = /\b(verif|validat|check|confirm|assert)\b/i.test(promptText);
out("Output validation", outputVal ? "Pass" : "Warn", outputVal ? "verification language found in prompt" : "no output verification cues in system prompt (CLASSic)");

process.exit(hasFail ? 1 : 0);
