import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPT_PATH = join(__dirname, '..', 'assets', 'scripts', 'search.py');

interface ServeOptions {
  port?: number;
}

export async function serveCommand(options: ServeOptions): Promise<void> {
  const port = options.port || 8080;
  const child = spawn('python3', [SCRIPT_PATH, '--serve', '--port', String(port)], {
    stdio: 'inherit',
  });

  child.on('error', (err) => {
    console.error(`Failed to start Design Studio: ${err.message}`);
    process.exit(1);
  });

  child.on('close', (code) => {
    process.exit(code || 0);
  });
}
