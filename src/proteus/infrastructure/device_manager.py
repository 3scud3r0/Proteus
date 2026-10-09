"""CPU-first device discovery without mandatory third-party packages."""
def inspect() -> dict:
    try:
        import torch
        cuda=bool(torch.cuda.is_available())
        return {"cpu":True,"cuda":cuda,"vram_gb":round(torch.cuda.get_device_properties(0).total_memory/(1024**3),2) if cuda else None}
    except ImportError:
        return {"cpu":True,"cuda":False,"vram_gb":None}
