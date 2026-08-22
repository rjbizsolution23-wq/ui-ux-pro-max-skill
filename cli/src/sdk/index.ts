import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPT_PATH = join(__dirname, '..', '..', 'assets', 'scripts', 'search.py');

export interface PipelineOptions {
  prompt: string;
  projectName?: string;
  stack?: 'html-tailwind' | 'react' | 'nextjs' | 'vue' | 'svelte' | 'swiftui' | 'flutter';
  persist?: boolean;
}

export interface PipelineResult {
  session_id: string;
  project_name: string;
  stack: string;
  artifacts: Record<string, any>;
  telemetry: Array<{
    id: string;
    timestamp: string;
    sender: string;
    recipient: string;
    stage: string;
    type: string;
    confidence: number;
    reasoning: string[];
    payload: any;
  }>;
}

export interface TokenOptions {
  primary?: string;
  secondary?: string;
  cta?: string;
  headingFont?: string;
  bodyFont?: string;
}

/**
 * Execute the August 2026 Multi-Agent Design Pipeline programmatically
 */
export async function runMultiAgentPipeline(options: PipelineOptions): Promise<PipelineResult> {
  return new Promise((resolve, reject) => {
    const args = [SCRIPT_PATH, options.prompt, '--agent', '--json'];
    if (options.projectName) args.push('-p', options.projectName);
    if (options.stack) args.push('--stack', options.stack);
    if (options.persist) args.push('--persist');

    const child = spawn('python3', args);
    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (d) => { stdout += d.toString(); });
    child.stderr.on('data', (d) => { stderr += d.toString(); });

    child.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`Pipeline failed with exit code ${code}: ${stderr}`));
      }
      try {
        const parsed = JSON.parse(stdout);
        resolve(parsed);
      } catch (err: any) {
        reject(new Error(`Failed to parse pipeline output JSON: ${err.message}`));
      }
    });
  });
}

/**
 * Generate W3C DTCG Design Tokens & Tailwind Theme programmatically
 */
export async function generateTokens(options: TokenOptions = {}): Promise<any> {
  return new Promise((resolve, reject) => {
    const args = [SCRIPT_PATH, '--tokens', '--format', 'w3c'];
    if (options.primary) args.push('--primary', options.primary);
    if (options.secondary) args.push('--secondary', options.secondary);
    if (options.cta) args.push('--cta', options.cta);

    const child = spawn('python3', args);
    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (d) => { stdout += d.toString(); });
    child.stderr.on('data', (d) => { stderr += d.toString(); });

    child.on('close', (code) => {
      if (code !== 0) return reject(new Error(stderr));
      try {
        resolve(JSON.parse(stdout));
      } catch (err: any) {
        reject(err);
      }
    });
  });
}

/**
 * Query BM25 Design Intelligence Database programmatically
 */
export async function searchIntelligence(query: string, domain?: string): Promise<any> {
  return new Promise((resolve, reject) => {
    const args = [SCRIPT_PATH, query, '--json'];
    if (domain) args.push('--domain', domain);

    const child = spawn('python3', args);
    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (d) => { stdout += d.toString(); });
    child.stderr.on('data', (d) => { stderr += d.toString(); });

    child.on('close', (code) => {
      if (code !== 0) return reject(new Error(stderr));
      try {
        resolve(JSON.parse(stdout));
      } catch (err: any) {
        reject(err);
      }
    });
  });
}
