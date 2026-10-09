"""No implicit external network access."""
def retrieve(url: str):
    raise PermissionError("Network disabled in prototype; no trusted browser isolation configured")
