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

   A sample dataset is provided in `plants.csv`.

3. Run the generator with a CSV file:
   ```bash
   python -m plant_layout.main WIDTH HEIGHT plants.csv --cell 0.5 --out output
   ```
   To supply plant data directly as JSON:
   ```bash
   python -m plant_layout.main WIDTH HEIGHT --json '[{"scientific_name": "Quercus", "kr_name": "참나무"}]' --cell 0.5 --out output
   ```
   The script will produce `placement.json` and `layout.png` in the output folder.

## API

A small FastAPI application exposes the layout generator over HTTP.

1. Install the dependencies and start the server:
   ```bash
   pip install -r requirements.txt
   uvicorn api:app --reload
   ```

2. Send a `POST` request to `/run-layout` with JSON containing the target area
   dimensions, an array of plant descriptions and optionally ``return_image``
   to disable the PNG response. Example:

   ```json
   {
     "width": 5,
     "height": 5,
     "plants": [{"scientific_name": "Quercus", "kr_name": "\ucc3d\ub098\ubb34"}],
     "return_image": true
   }
   ```

   On success the response body contains the list of placements and, when
   requested, a base64 encoded PNG image of the layout. If an error occurs, the
   server responds with HTTP 400 and a descriptive message.

## License

MIT
