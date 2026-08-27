#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const userHome = process.env.USERPROFILE || process.env.HOME || '';
if (!userHome) {
  console.error('Error: Could not determine user home directory.');
  process.exit(1);
}

const srcDir = path.join(__dirname, '..', 'skills', 'shopaholic');

const targetRoots = [
  path.join(userHome, '.agents', 'skills'),
  path.join(userHome, '.claude', 'skills'),
  path.join(userHome, '.omp', 'skills'),
  path.join(userHome, '.omp', 'agent', 'skills'),
  path.join(userHome, '.pi', 'skills'),
  path.join(userHome, '.pi', 'agent', 'skills'),
  path.join(userHome, '.codex', 'skills')
];

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

console.log('====================================================');
console.log('🚀 Installing/Updating Shopaholic Skill across agent runtimes...');
console.log('====================================================');

let installedCount = 0;
for (const root of targetRoots) {
  try {
    const targetDir = path.join(root, 'shopaholic');
    copyDir(srcDir, targetDir);
    console.log(`✅ Synced to: ${targetDir}`);
    installedCount++;
  } catch (err) {
    console.warn(`⚠️ Skipped ${root}: ${err.message}`);
  }
}

console.log('====================================================');
console.log(`🎉 Successfully synced to ${installedCount} runtime locations!`);
console.log('💡 You can now use "shopaholic" skill in Pi, OMP, Claude Code, Codex, and OpenClaw.');
console.log('====================================================');
