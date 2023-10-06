def ffns(nf):
    theory = {}

    for i, q in enumerate("cbt"):
        theory[f"ZM{q}"] = True
        theory[f"k{q}Thr"] = 0.0 if nf >= i + 4 else float("inf")

    return theory
