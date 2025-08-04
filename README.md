# Shadow-Aware Plant Layout Generator

This project generates plant layouts on a rectangular area while respecting the
light requirements of each species. Shadows are simulated for several sun
positions to estimate per-cell light levels.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Ensure the `NanumGothic` font is available. On Ubuntu:
   ```bash
   sudo apt-get install fonts-nanum
   ```

2. Prepare `plants.csv` with columns:
   `scientific_name,kr_name,life_form,max_height_m,root_depth_cm_range,light_requirement_1_5,lifespan_yr`
   (Korean headers such as `학명,국명,...` are also accepted.)

   A sample dataset is provided in `sample_plants.csv`.

3. Run the generator with a CSV file:
   ```bash
   python -m plant_layout.main WIDTH HEIGHT plants.csv --cell 0.5 --out output
   ```
   To supply plant data directly as JSON:
   ```bash
   python -m plant_layout.main WIDTH HEIGHT --json '[{"scientific_name": "Quercus", "kr_name": "참나무"}]' --cell 0.5 --out output
   ```
   The script will produce `placement.json` and `layout.png` in the output folder.

## Environment Variables

The server uses the `PYTHON` environment variable to determine which Python
interpreter to run. Set it to the path of your preferred Python executable. If
unset, it defaults to `python3`.

```bash
export PYTHON=/usr/bin/python3.11
```

## Building a Standalone Binary

To bundle a Python script into a single executable with [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller
pyinstaller --onefile test.py
./dist/test
```

## License

MIT
