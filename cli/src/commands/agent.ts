import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPT_PATH = join(__dirname, '..', 'assets', 'scripts', 'search.py');

interface AgentOptions {
  prompt: string;
  name?: string;
  stack?: string;
  format?: string;
  persist?: boolean;
  json?: boolean;
}

export async function agentCommand(options: AgentOptions): Promise<void> {
  const args = [SCRIPT_PATH, options.prompt, '--agent'];

  if (options.name) {
    args.push('-p', options.name);
  }
  if (options.stack) {
    args.push('--stack', options.stack);
  }
  if (options.format) {
    args.push('-f', options.format);
  }
  if (options.persist) {
    args.push('--persist');
  }
  if (options.json) {
    args.push('--json');
  }

  const child = spawn('python3', args, {
    stdio: 'inherit',
  });

  child.on('error', (err) => {
    console.error(`Failed to execute multi-agent engine: ${err.message}`);
    console.error('Please ensure Python 3 is installed.');
    process.exit(1);
  });

  child.on('close', (code) => {
    if (code !== 0) {
      process.exit(code || 1);
    }
  });
}
