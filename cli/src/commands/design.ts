import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPT_PATH = join(__dirname, '..', 'assets', 'scripts', 'search.py');

interface DesignOptions {
  query: string;
  name?: string;
  format?: string;
  persist?: boolean;
  page?: string;
}

export async function designCommand(options: DesignOptions): Promise<void> {
  const args = [SCRIPT_PATH, options.query, '--design-system'];

  if (options.name) {
    args.push('-p', options.name);
  }
  if (options.format) {
    args.push('-f', options.format);
  }
  if (options.persist) {
    args.push('--persist');
  }
  if (options.page) {
    args.push('--page', options.page);
  }

  const child = spawn('python3', args, {
    stdio: 'inherit',
  });

  child.on('error', (err) => {
    console.error(`Failed to execute design system engine: ${err.message}`);
    process.exit(1);
  });

  child.on('close', (code) => {
    if (code !== 0) {
      process.exit(code || 1);
    }
  });
}
