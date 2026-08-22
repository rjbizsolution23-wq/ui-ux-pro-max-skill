import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPT_PATH = join(__dirname, '..', 'assets', 'scripts', 'search.py');

export async function mcpCommand(): Promise<void> {
  const child = spawn('python3', [SCRIPT_PATH, '--mcp'], {
    stdio: 'inherit',
  });

  child.on('error', (err) => {
    console.error(`Failed to start MCP server: ${err.message}`);
    process.exit(1);
  });

  child.on('close', (code) => {
    process.exit(code || 0);
  });
}
