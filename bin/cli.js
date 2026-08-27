#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const userHome = process.env.USERPROFILE || process.env.HOME || '';
const cwd = process.cwd();
const srcDir = path.join(__dirname, '..', 'skills', 'shopaholic');

const args = process.argv.slice(2);
const isRepoMode = args.includes('--repo') || args.includes('--local') || args.includes('-l');
const isGlobalMode = args.includes('--global') || args.includes('-g');
const isAllMode = args.includes('--all') || args.includes('-a');

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(s, d);
    } else {
      fs.copyFileSync(s, d);
    }
  }
}

const RUNTIME_REL_PATHS = [
  ['.agents', 'skills'],
  ['.claude', 'skills'],
  ['.omp', 'skills'],
  ['.omp', 'agent', 'skills'],
  ['.pi', 'skills'],
  ['.pi', 'agent', 'skills'],
  ['.codex', 'skills']
];

const globalRoots = userHome ? RUNTIME_REL_PATHS.map(p => path.join(userHome, ...p)) : [];

function getAdaptiveRepoRoots() {
  const roots = [];
  // Detect config markers in workspace
  const hasClaude = fs.existsSync(path.join(cwd, '.claude')) || fs.existsSync(path.join(cwd, 'claude.json'));
  const hasOmp = fs.existsSync(path.join(cwd, '.omp')) || fs.existsSync(path.join(cwd, 'omp.json'));
  const hasAgents = fs.existsSync(path.join(cwd, '.agents')) || fs.existsSync(path.join(cwd, '.git')) || fs.existsSync(path.join(cwd, 'package.json'));

  if (hasAgents) roots.push(path.join(cwd, '.agents', 'skills'));
  if (hasClaude) roots.push(path.join(cwd, '.claude', 'skills'));
  if (hasOmp) roots.push(path.join(cwd, '.omp', 'skills'));
  if (fs.existsSync(path.join(cwd, 'skills'))) roots.push(path.join(cwd, 'skills'));

  return roots.length > 0 ? roots : [path.join(cwd, '.agents', 'skills')];
}

let targetRoots = [];

if (isRepoMode) {
  targetRoots = getAdaptiveRepoRoots();
  console.log('📦 Installing in Repo/Project-level Mode (Current Workspace)...');
} else if (isGlobalMode) {
  targetRoots = globalRoots;
  console.log('🌐 Installing in User Global Mode (Home Directory)...');
} else if (isAllMode) {
  targetRoots = [...globalRoots, ...getAdaptiveRepoRoots()];
  console.log('🚀 Installing in All Mode (Global & Repo)...');
} else {
  // Default mode: sync across global runtimes and adaptively include repo if workspace marker present
  targetRoots = [...globalRoots];
  if (fs.existsSync(path.join(cwd, '.git')) || fs.existsSync(path.join(cwd, 'package.json')) || fs.existsSync(path.join(cwd, '.agents'))) {
    targetRoots.push(path.join(cwd, '.agents', 'skills'));
  }
  console.log('🚀 Installing/Updating Shopaholic Skill across agent runtimes & workspace...');
}

console.log('====================================================');

let installedCount = 0;
const visited = new Set();

for (const root of targetRoots) {
  if (visited.has(root)) continue;
  visited.add(root);
  try {
    const targetDir = path.join(root, 'shopaholic');
    if (path.resolve(targetDir) === path.resolve(srcDir)) {
      continue;
    }
    copyDir(srcDir, targetDir);
    console.log(`✅ Synced to: ${targetDir}`);
    installedCount++;
  } catch (err) {
    console.warn(`⚠️ Skipped ${root}: ${err.message}`);
  }
}

console.log('====================================================');
console.log(`🎉 Successfully synced to ${installedCount} target location(s)!`);
console.log('💡 You can now use "shopaholic" skill in Pi, OMP, Claude Code, Codex, and OpenClaw.');
console.log('====================================================');
