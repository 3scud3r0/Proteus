"""Paired random seeds shared across interventions."""
def design(seeds: list[int],episodes: int) -> list[dict]:
    if episodes<1 or not seeds: raise ValueError("Non-empty seeds and episodes required")
    return [{"seed":seed,"episodes":episodes,"condition":condition} for seed in seeds for condition in ("control","replay")]
