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

const globalRoots = userHome ? [
  path.join(userHome, '.agents', 'skills'),
  path.join(userHome, '.claude', 'skills'),
  path.join(userHome, '.omp', 'skills'),
  path.join(userHome, '.omp', 'agent', 'skills'),
  path.join(userHome, '.pi', 'skills'),
  path.join(userHome, '.pi', 'agent', 'skills'),
  path.join(userHome, '.codex', 'skills')
] : [];

const repoRoots = [
  path.join(cwd, '.agents', 'skills'),
  path.join(cwd, '.claude', 'skills'),
  path.join(cwd, 'skills')
];

let targetRoots = [];

if (isRepoMode) {
  targetRoots = repoRoots;
  console.log('📦 Installing in Repo/Project-level Mode (Current Workspace)...');
} else if (isGlobalMode) {
  targetRoots = globalRoots;
  console.log('🌐 Installing in User Global Mode (Home Directory)...');
} else if (isAllMode) {
  targetRoots = [...globalRoots, ...repoRoots];
  console.log('🚀 Installing in All Mode (Global & Repo)...');
} else {
  // Default: install to global, and if in a git/agent repo, also sync to repo .agents/skills
  targetRoots = [...globalRoots];
  if (fs.existsSync(path.join(cwd, '.git')) || fs.existsSync(path.join(cwd, '.agents')) || fs.existsSync(path.join(cwd, '.claude'))) {
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
    // Skip if targetDir is the exact same path as srcDir
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
