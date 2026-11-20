import re
def parse_tac(filename):
    statements = []
    with open(filename, "r") as f:
        for line in f:
            line = line.split("//")[0].strip()   # remove inline comments
            if line:
                statements.append(line)
    return statements

def constant_folding(statements):
    result = []
    for stmt in statements:
        lhs, _, rhs = stmt.partition("=")
        lhs = lhs.strip()
        rhs = rhs.strip()
        try:
            # Safely evaluate purely numeric expressions
            value = eval(rhs, {"__builtins__": {}})
            if isinstance(value, (int, float)):
                stmt = f"{lhs}={value}"
        except Exception:
            pass
        result.append(stmt)
    return result

def copy_propagation(statements):
    copy_map = {}   # maps variable → its direct alias

    # Build alias map from pure copy assignments  (X = Y, Y is a variable)
    for stmt in statements:
        lhs, _, rhs = stmt.partition("=")
        lhs, rhs = lhs.strip(), rhs.strip()
        if re.fullmatch(r"[A-Za-z_]\w*", rhs):   # rhs is a plain variable
            copy_map[lhs] = rhs

    # Propagate aliases; resolve chains (T3→T1, T1→25 becomes T3→25)
    def resolve(var):
        seen = set()
        while var in copy_map and var not in seen:
            seen.add(var)
            var = copy_map[var]
        return var

    result = []
    for stmt in statements:
        lhs, _, rhs = stmt.partition("=")
        lhs, rhs = lhs.strip(), rhs.strip()

        # Skip pure copy statements (they are now redundant)
        if re.fullmatch(r"[A-Za-z_]\w*", rhs) and lhs in copy_map:
            continue

        # Replace every variable token on the rhs with its resolved alias
        def replace_var(m):
            return resolve(m.group())

        rhs_propagated = re.sub(r"[A-Za-z_]\w*", replace_var, rhs)
        result.append(f"{lhs}={rhs_propagated}")

    return result

def cse(statements):
    expr_map = {}   # rhs expression → first lhs that computed it
    result = []

    for stmt in statements:
        lhs, _, rhs = stmt.partition("=")
        lhs, rhs = lhs.strip(), rhs.strip()

        new_rhs = rhs
        for expr, var in expr_map.items():
            if expr in new_rhs and var != lhs:
                new_rhs = new_rhs.replace(expr, var)

        # Record this expression for future reuse
        if rhs not in expr_map:
            expr_map[rhs] = lhs

        result.append(f"{lhs}={new_rhs}")

    return result

def optimize(filename):
    print("=" * 50)
    print("   CODE OPTIMIZATION USING THREE-ADDRESS CODE")
    print("=" * 50)

    # --- Input ---
    original = parse_tac(filename)
    print("\nInput (Before Optimization):")
    for s in original:
        print(f"  {s}")

    # --- Pass 1: Constant Folding ---
    after_cf = constant_folding(original)

    # --- Pass 2: Copy Propagation ---
    after_cp = copy_propagation(after_cf)

    # --- Pass 3: Common Sub-expression Elimination ---
    after_cse = cse(after_cp)

    # --- Output ---
    print("\nOutput (After Optimization):")
    for s in after_cse:
        print(f"  {s}")

    print("=" * 50)

    return after_cse

if __name__ == "__main__":
    optimize("exp6inp.txt")