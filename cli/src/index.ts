#!/usr/bin/env node

import { Command } from 'commander';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { initCommand } from './commands/init.js';
import { versionsCommand } from './commands/versions.js';
import { updateCommand } from './commands/update.js';
import { agentCommand } from './commands/agent.js';
import { tokensCommand } from './commands/tokens.js';
import { designCommand } from './commands/design.js';
import { mcpCommand } from './commands/mcp.js';
import { serveCommand } from './commands/serve.js';
import type { AIType } from './types/index.js';
import { AI_TYPES } from './types/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const pkg = JSON.parse(readFileSync(join(__dirname, '../package.json'), 'utf-8'));

const program = new Command();

program
  .name('uipro')
  .description('UI/UX Pro Max - August 2026 Multi-Agent Design System & Intelligence CLI')
  .version(pkg.version);

program
  .command('init')
  .description('Install UI/UX Pro Max skill to current project for any AI assistant')
  .option('-a, --ai <type>', `AI assistant type (${AI_TYPES.join(', ')})`)
  .option('-f, --force', 'Overwrite existing files')
  .option('-o, --offline', 'Skip GitHub download, use bundled assets only')
  .action(async (options) => {
    if (options.ai && !AI_TYPES.includes(options.ai)) {
      console.error(`Invalid AI type: ${options.ai}`);
      console.error(`Valid types: ${AI_TYPES.join(', ')}`);
      process.exit(1);
    }
    await initCommand({
      ai: options.ai as AIType | undefined,
      force: options.force,
      offline: options.offline,
    });
  });

program
  .command('agent')
  .description('Run August 2026 multi-agent design pipeline')
  .argument('<prompt>', 'Design prompt or requirements')
  .option('-p, --name <name>', 'Project name')
  .option('-s, --stack <stack>', 'Target stack (html-tailwind, react, nextjs, vue, svelte, swiftui, flutter)')
  .option('-f, --format <format>', 'Output format (markdown, json)')
  .option('--persist', 'Persist design system and tokens to workspace')
  .option('--json', 'Output raw JSON')
  .action(async (prompt, options) => {
    await agentCommand({
      prompt,
      name: options.name,
      stack: options.stack,
      format: options.format,
      persist: options.persist,
      json: options.json,
    });
  });

program
  .command('design')
  .description('Generate complete design system recommendation')
  .argument('<query>', 'Search query or project description')
  .option('-p, --name <name>', 'Project name')
  .option('-f, --format <format>', 'Output format (ascii, markdown)', 'markdown')
  .option('--persist', 'Save design system to MASTER.md')
  .option('--page <page>', 'Create page-specific override file')
  .action(async (query, options) => {
    await designCommand({
      query,
      name: options.name,
      format: options.format,
      persist: options.persist,
      page: options.page,
    });
  });

program
  .command('tokens')
  .description('Generate W3C DTCG standard design tokens, OKLCH ramps & Tailwind v4 theme')
  .option('--primary <hex>', 'Primary brand hex color', '#6366F1')
  .option('--secondary <hex>', 'Secondary brand hex color', '#06B6D4')
  .option('--cta <hex>', 'CTA accent hex color', '#10B981')
  .option('-f, --format <format>', 'Output format (css, tailwind, ts, w3c, all)', 'all')
  .option('--json', 'Output as JSON')
  .action(async (options) => {
    await tokensCommand({
      primary: options.primary,
      secondary: options.secondary,
      cta: options.cta,
      format: options.format,
      json: options.json,
    });
  });

program
  .command('mcp')
  .description('Start Model Context Protocol (MCP) JSON-RPC server for Cursor / Claude Desktop / Windsurf')
  .action(async () => {
    await mcpCommand();
  });

program
  .command('serve')
  .description('Start live interactive August 2026 Design Studio web workbench & REST API')
  .option('-p, --port <port>', 'Server port', '8080')
  .action(async (options) => {
    await serveCommand({
      port: parseInt(options.port, 10),
    });
  });

program
  .command('versions')
  .description('List available versions')
  .action(versionsCommand);

program
  .command('update')
  .description('Update UI/UX Pro Max to latest version')
  .option('-a, --ai <type>', `AI assistant type (${AI_TYPES.join(', ')})`)
  .action(async (options) => {
    if (options.ai && !AI_TYPES.includes(options.ai)) {
      console.error(`Invalid AI type: ${options.ai}`);
      console.error(`Valid types: ${AI_TYPES.join(', ')}`);
      process.exit(1);
    }
    await updateCommand({
      ai: options.ai as AIType | undefined,
    });
  });

program.parse();
