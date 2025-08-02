import fs from 'fs';
import { tmpdir } from 'os';
import path from 'path';

export interface PlantInput {
  [key: string]: string | number | boolean | null | undefined;
}

function escapeCsvValue(value: unknown): string {
  if (value === null || value === undefined) return '';
  const str = String(value);
  if (/[",\n]/.test(str)) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

/**
 * Convert selected plants list to a CSV file.
 * Returns path to temporary file written in UTF-8 encoding.
 */
export function selectedPlantsToCsv(plants: PlantInput[]): string {
  const filePath = path.join(tmpdir(), `selected-plants-${Date.now()}.csv`);
  if (plants.length === 0) {
    fs.writeFileSync(filePath, '', { encoding: 'utf8' });
    return filePath;
  }
  const headers = Object.keys(plants[0]);
  const rows = plants.map(p => headers.map(h => escapeCsvValue(p[h])).join(','));
  const csv = [headers.join(','), ...rows].join('\n');
  fs.writeFileSync(filePath, csv, { encoding: 'utf8' });
  return filePath;
}
