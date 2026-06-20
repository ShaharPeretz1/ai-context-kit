#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const SPEC_DRIVEN_MARKER = 'spec-driven context';

const CLAUDE_SECTION = `
## Spec-driven context

At session start, read in order: \`specs/product.md\` → \`specs/team.md\` → \`specs/architecture.md\` → \`specs/roadmap.md\` → \`specs/decisions.md\` → relevant \`specs/features/*.md\`. Confirm understanding in 3-4 lines before writing code. Treat \`specs/decisions.md\` as binding — never re-suggest rejected approaches.
`;

const WORKFLOW = `name: Spec close-out prompt

on:
  pull_request:
    types: [closed]
    branches: [main, master]

jobs:
  close-out:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - uses: ShaharPeretz1/ai-context-kit@v1
        with:
          pr-number: \${{ github.event.pull_request.number }}
          pr-title: \${{ github.event.pull_request.title }}
          pr-body: \${{ github.event.pull_request.body }}
`;

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function copyTemplate(src, dest) {
  if (fs.existsSync(dest)) {
    console.log(`  skip  ${dest} (already exists)`);
    return;
  }
  fs.copyFileSync(src, dest);
  console.log(`  create ${dest}`);
}

function init() {
  const pkgRoot = path.join(__dirname, '..');
  const kitSpecs = path.join(pkgRoot, 'kit', 'specs');
  const cwd = process.cwd();

  console.log('\nspec-driven init\n');

  // 1. Create specs/
  const specsDir = path.join(cwd, 'specs');
  ensureDir(path.join(specsDir, 'features'));

  for (const file of ['product.md', 'team.md', 'architecture.md', 'roadmap.md', 'decisions.md', 'repo-map.md']) {
    copyTemplate(path.join(kitSpecs, file), path.join(specsDir, file));
  }
  copyTemplate(
    path.join(kitSpecs, 'features', '_TEMPLATE.md'),
    path.join(specsDir, 'features', '_TEMPLATE.md')
  );

  // 2. Update CLAUDE.md
  const claudePath = path.join(cwd, 'CLAUDE.md');
  if (fs.existsSync(claudePath)) {
    const existing = fs.readFileSync(claudePath, 'utf8');
    if (existing.includes(SPEC_DRIVEN_MARKER)) {
      console.log(`  skip  CLAUDE.md (spec-driven section already present)`);
    } else {
      fs.appendFileSync(claudePath, CLAUDE_SECTION);
      console.log(`  update CLAUDE.md (appended spec-driven section)`);
    }
  } else {
    fs.writeFileSync(claudePath, `# CLAUDE.md\n${CLAUDE_SECTION}`);
    console.log(`  create CLAUDE.md`);
  }

  // 3. Create .github/workflows/spec-update.yml
  const workflowDir = path.join(cwd, '.github', 'workflows');
  ensureDir(workflowDir);
  const workflowPath = path.join(workflowDir, 'spec-update.yml');
  if (fs.existsSync(workflowPath)) {
    console.log(`  skip  .github/workflows/spec-update.yml (already exists)`);
  } else {
    fs.writeFileSync(workflowPath, WORKFLOW);
    console.log(`  create .github/workflows/spec-update.yml`);
  }

  console.log(`
Done. Next steps:
  1. Fill in specs/product.md  — what you're building and why
  2. Fill in specs/team.md     — who owns what
  3. Commit and push           — the close-out Action fires on your next PR merge
`);
}

const cmd = process.argv[2];
if (cmd === 'init') {
  init();
} else {
  console.log('Usage: npx spec-driven init');
  process.exit(1);
}
