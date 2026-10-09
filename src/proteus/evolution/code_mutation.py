"""Safe configuration mutation; self-modifying source code is NOT supported."""
def vary(config: dict,parameter: str,values: list) -> list[dict]:
    if parameter not in {"alpha","gamma","replay_per_step","epsilon_start"}:
        raise PermissionError("Parameter is outside bounded experimental scope")
    return [{**config,parameter:value} for value in values]
