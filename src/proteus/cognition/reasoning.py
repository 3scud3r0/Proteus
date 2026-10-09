"""Auditable simple rule inference."""
def infer(rules: dict[str,list[str]],known: set[str]) -> set[str]:
    output=set(known)
    changed=True
    while changed:
        changed=False
        for conclusion,premises in rules.items():
            if conclusion not in output and all(p in output for p in premises):
                output.add(conclusion); changed=True
    return output
