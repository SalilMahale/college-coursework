"""
Experiment: Implementation of Code Generation Phase of the Compiler
- Accepts statements in Three Address Code (3AC) form
- Generates target machine code (assembly-like instructions)
- Maintains Register Descriptors and Address Descriptors
- Displays output in tabular form
"""


def code_generation(three_address_code):
    """
    Perform code generation from Three Address Code (3AC).
    Generates assembly instructions with register and address descriptors.
    """
    # Available registers
    available_registers = ["R0", "R1", "R2", "R3"]

    # Register descriptor: maps register -> set of variables it currently holds
    reg_descriptor = {r: set() for r in available_registers}

    # Address descriptor: maps variable -> set of locations where its value lives
    # Locations can be register names or "memory"
    addr_descriptor = {}

    # Parse all 3AC statements
    statements = []
    for line in three_address_code:
        line = line.strip()
        if not line:
            continue
        # Parse: result = operand1 op operand2  OR  result = operand1
        if ":=" in line:
            lhs, rhs = line.split(":=")
        elif "=" in line:
            lhs, rhs = line.split("=", 1)
        else:
            continue
        lhs = lhs.strip()
        rhs = rhs.strip()
        statements.append((lhs, rhs))

    # Determine last use of each variable for freeing registers
    last_use = {}
    for i, (lhs, rhs) in enumerate(statements):
        tokens = rhs.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split()
        for tok in tokens:
            tok = tok.strip()
            if tok and not tok.replace(".", "").isdigit():
                last_use[tok] = i
        last_use[lhs] = i  # lhs is also "used" (defined) at this point

    # Helper: get a register containing the given variable, or None
    def get_reg_for(var):
        for r in available_registers:
            if var in reg_descriptor[r]:
                return r
        return None

    # Helper: get a free register (one that holds nothing)
    def get_free_reg():
        for r in available_registers:
            if len(reg_descriptor[r]) == 0:
                return r
        return None

    # Helper: allocate a register for a variable, spilling if needed
    def get_register(var, stmt_index):
        # 1. If var is already in a register, use that
        r = get_reg_for(var)
        if r is not None:
            return r, []

        # 2. Try to find a free register
        r = get_free_reg()
        if r is not None:
            return r, []

        # 3. Spill: pick register whose content is used farthest in future (or not at all)
        spill_code = []
        best_reg = None
        best_score = -1
        for reg in available_registers:
            for v in reg_descriptor[reg]:
                future = last_use.get(v, -1)
                if future <= stmt_index:
                    best_reg = reg
                    best_score = float("inf")
                    break
                elif future > best_score:
                    best_score = future
                    best_reg = reg
            if best_score == float("inf"):
                break

        if best_reg is None:
            best_reg = available_registers[0]

        # Spill all variables in that register to memory
        for v in list(reg_descriptor[best_reg]):
            if "memory" not in addr_descriptor.get(v, set()):
                spill_code.append(f"MOV {best_reg}, {v}")
                addr_descriptor.setdefault(v, set()).add("memory")
            reg_descriptor[best_reg].discard(v)
            addr_descriptor[v].discard(best_reg)

        return best_reg, spill_code

    # ---- Main code generation loop ----
    results = []  # List of tuples: (statement, code_lines, reg_desc_snapshot, addr_desc_snapshot)

    print("\n" + "=" * 85)
    print("CODE GENERATION PHASE")
    print("=" * 85)
    print(f"\nInput 3AC Statements:")
    for line in three_address_code:
        print(f"  {line.strip()}")
    print()

    is_last_statement = lambda i: i == len(statements) - 1

    for i, (lhs, rhs) in enumerate(statements):
        code_lines = []
        tokens = rhs.strip().split()

        if len(tokens) == 3:
            # Binary operation: operand1 op operand2
            op1, op, op2 = tokens[0].strip(), tokens[1].strip(), tokens[2].strip()

            # Map operator to assembly mnemonic
            op_map = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV"}
            asm_op = op_map.get(op, op)

            # Get register for op1
            reg1, spill1 = get_register(op1, i)
            code_lines.extend(spill1)

            # If op1 is not already in reg1, load it
            if op1 not in reg_descriptor[reg1]:
                code_lines.append(f"MOV {op1}, {reg1}")
                # Update descriptors
                reg_descriptor[reg1] = {op1}
                addr_descriptor.setdefault(op1, set()).add(reg1)

            # Get register for op2 (may be same if op2 == op1)
            reg2 = get_reg_for(op2)
            if reg2 is None:
                # op2 comes from memory; use it directly in instruction
                code_lines.append(f"{asm_op} {op2}, {reg1}")
            else:
                code_lines.append(f"{asm_op} {reg2}, {reg1}")

            # After operation, reg1 now holds lhs (result)
            # Remove old variable from reg1
            for v in list(reg_descriptor[reg1]):
                if v != lhs:
                    addr_descriptor.get(v, set()).discard(reg1)
            reg_descriptor[reg1] = {lhs}
            addr_descriptor[lhs] = {reg1}

            # If op2 was in a register and this is its last use, free it
            if last_use.get(op2, -1) <= i and reg2 is not None and reg2 != reg1:
                reg_descriptor[reg2].discard(op2)

            # If op1's last use is here and it's in another register, free it
            if last_use.get(op1, -1) <= i:
                for r in available_registers:
                    if r != reg1 and op1 in reg_descriptor[r]:
                        reg_descriptor[r].discard(op1)

        elif len(tokens) == 1:
            # Copy statement: lhs = operand
            op1 = tokens[0].strip()
            reg1, spill1 = get_register(op1, i)
            code_lines.extend(spill1)
            if op1 not in reg_descriptor[reg1]:
                code_lines.append(f"MOV {op1}, {reg1}")
                reg_descriptor[reg1] = {op1, lhs}
            else:
                reg_descriptor[reg1].add(lhs)
            addr_descriptor[lhs] = {reg1}
            addr_descriptor.setdefault(op1, set()).add(reg1)

        # If this is the last statement, store result to memory
        if is_last_statement(i):
            result_reg = get_reg_for(lhs)
            if result_reg is not None:
                code_lines.append(f"MOV {result_reg}, {lhs}")
                addr_descriptor[lhs].add("memory")

        # Take snapshots of descriptors for display
        reg_snap = {}
        for r in available_registers:
            if reg_descriptor[r]:
                reg_snap[r] = set(reg_descriptor[r])

        addr_snap = {}
        for v, locs in addr_descriptor.items():
            if locs:
                addr_snap[v] = set(locs)

        original_stmt = f"{lhs} := {rhs}"
        results.append((original_stmt, code_lines, reg_snap, addr_snap))

    # ---- Display results in table format ----
    print("-" * 85)
    print(f"{'Statement':<16} {'Code Generated':<20} {'Register Descriptor':<25} {'Address Descriptor'}")
    print("-" * 85)
    print(f"{'':<16} {'':<20} {'Registers empty':<25} {''}")
    print("-" * 85)

    for stmt, codes, reg_snap, addr_snap in results:
        code_str = "\n".join(codes) if codes else ""
        reg_str = ", ".join(f"{r} contains {','.join(sorted(v))}" for r, v in sorted(reg_snap.items()))
        addr_str = ", ".join(
            f"{v} in {' and '.join(sorted(locs, key=lambda x: (x != 'memory', x)))}"
            for v, locs in sorted(addr_snap.items())
            if any(loc != "memory" or v == list(addr_snap.keys())[-1] for loc in locs)
        )

        # For cleaner display, show only relevant address descriptors
        # (variables that changed or are actively in registers)
        active_vars = set()
        for r, vs in reg_snap.items():
            active_vars.update(vs)
        addr_str_lines = []
        for v in sorted(addr_snap.keys()):
            if v in active_vars or "memory" in addr_snap[v]:
                locs = sorted(addr_snap[v], key=lambda x: (x == "memory", x))
                addr_str_lines.append(f"{v} in {' and '.join(locs)}")

        # Print with multiline support
        code_list = codes if codes else [""]
        reg_str_display = reg_str if reg_str else ""
        addr_str_display = "\n".join(addr_str_lines) if addr_str_lines else ""

        # First line
        print(f"{stmt:<16} {code_list[0]:<20} {reg_str_display:<25} {addr_str_lines[0] if addr_str_lines else ''}")
        # Remaining code lines
        max_lines = max(len(code_list), len(addr_str_lines))
        for j in range(1, max_lines):
            c = code_list[j] if j < len(code_list) else ""
            a = addr_str_lines[j] if j < len(addr_str_lines) else ""
            print(f"{'':<16} {c:<20} {'':<25} {a}")
        print("-" * 85)

    # Collect all generated code
    print("\n\nFinal Generated Assembly Code:")
    print("-" * 40)
    for stmt, codes, _, _ in results:
        print(f"  ; {stmt}")
        for c in codes:
            print(f"    {c}")
    print("-" * 40)


# ---- Main Program ----
if __name__ == "__main__":
    print("=" * 85)
    print("   EXPERIMENT: Implementation of Code Generation Phase of the Compiler")
    print("=" * 85)
    print("\nEnter Three Address Code (3AC) statements.")
    print("Use format:  variable = operand1 op operand2")
    print("Supported operators: +, -, *, /")
    print("Type 'done' when finished.\n")

    print("Example input:")
    print("  t = a - b")
    print("  u = a - c")
    print("  v = t + u")
    print("  d = v + u\n")

    tac_statements = []
    while True:
        stmt = input("Enter 3AC statement (or 'done'): ").strip()
        if stmt.lower() == "done":
            break
        if stmt:
            tac_statements.append(stmt)

    if tac_statements:
        code_generation(tac_statements)
    else:
        print("No statements entered.")
