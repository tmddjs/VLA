import { Router } from 'express';
import { spawn } from 'child_process';

const router = Router();

const PYTHON = process.env.PYTHON || 'python3';

router.get('/python-version', (_req, res) => {
  const proc = spawn(PYTHON, ['--version']);
  let output = '';
  proc.stdout.on('data', data => (output += data));
  proc.stderr.on('data', data => (output += data));
  proc.on('close', code => {
    res.json({ version: output.trim(), code });
  });
});

export default router;
