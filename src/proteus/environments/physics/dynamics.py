"""Elementary Euler integration for bounded toy experiments."""
def integrate(x: float, v: float, acceleration: float, dt: float = 0.01) -> tuple[float,float]:
    if dt <= 0:
        raise ValueError("dt must be positive")
    v_next = v + acceleration*dt
    return x + v_next*dt, v_next
