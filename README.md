# Shadow-Aware Plant Layout Generator

This project generates plant layouts on a rectangular area while respecting the
light requirements of each species. Shadows are simulated for several sun
positions to estimate per-cell light levels.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Prepare `plants.csv` with columns:
   `scientific_name,kr_name,life_form,max_height_m,root_depth_cm_range,light_requirement_1_5,lifespan_yr`
   (Korean headers such as `학명,국명,...` are also accepted.)

   A sample dataset is provided in `sample_plants.csv`.

3. Run the generator:
   ```bash
   python -m plant_layout.main plants.csv WIDTH HEIGHT --cell 0.5 --out output
   ```
   The script will produce `placement.json` and `layout.png` in the output folder.

## License

MIT
