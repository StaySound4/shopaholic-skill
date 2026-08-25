#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const userHome = process.env.USERPROFILE || process.env.HOME || '';
if (!userHome) {
  console.error('Error: Could not determine user home directory.');
  process.exit(1);
}

const targetDir = path.join(userHome, '.agents', 'skills', 'shopaholic');
const srcDir = path.join(__dirname, '..', 'skills', 'shopaholic');

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

try {
  copyDir(srcDir, targetDir);
  console.log('====================================================');
  console.log('✅ Shopaholic Skill installed successfully!');
  console.log(`📁 Installed location: ${targetDir}`);
  console.log('💡 You can now use "shopaholic" skill in your AI agent.');
  console.log('====================================================');
} catch (err) {
  console.error('❌ Installation failed:', err.message);
  process.exit(1);
}
