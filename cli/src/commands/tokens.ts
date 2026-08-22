import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPT_PATH = join(__dirname, '..', 'assets', 'scripts', 'search.py');

interface TokensOptions {
  primary?: string;
  secondary?: string;
  cta?: string;
  format?: string;
  json?: boolean;
}

export async function tokensCommand(options: TokensOptions): Promise<void> {
  const args = [SCRIPT_PATH, '--tokens'];

  if (options.primary) {
    args.push('--primary', options.primary);
  }
  if (options.secondary) {
    args.push('--secondary', options.secondary);
  }
  if (options.cta) {
    args.push('--cta', options.cta);
  }
  if (options.format) {
    args.push('-f', options.format);
  }
  if (options.json) {
    args.push('--json');
  }

  const child = spawn('python3', args, {
    stdio: 'inherit',
  });

  child.on('error', (err) => {
    console.error(`Failed to execute tokens engine: ${err.message}`);
    process.exit(1);
  });

  child.on('close', (code) => {
    if (code !== 0) {
      process.exit(code || 1);
    }
  });
}
