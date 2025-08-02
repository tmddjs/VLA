import path from 'path';
import { spawn } from 'child_process';
import { PlantInput, selectedPlantsToCsv } from './utils/serialize';

/**
 * Run the Python layout generator after converting selected plants to CSV.
 */
export function runLayout(plants: PlantInput[], width: number, height: number, cell = 0.5): Promise<void> {
  const csvPath = selectedPlantsToCsv(plants);
  const script = path.resolve(__dirname, '../../plant_layout/main.py');
  return new Promise((resolve, reject) => {
    const args = [script, csvPath, width.toString(), height.toString(), '--cell', cell.toString()];
    const proc = spawn('python', args, { stdio: 'inherit' });
    proc.on('close', code => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Layout process exited with code ${code}`));
      }
    });
  });
}
