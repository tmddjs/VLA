export interface PlantInput {
  scientific_name: string;
  kr_name: string;
  life_form: string;
  max_height_m: number;
  root_depth_cm_range: [number, number];
  light_requirement_1_5: number;
  lifespan_yr: number;
}
