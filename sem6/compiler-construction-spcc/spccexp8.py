IS = {
    "ADD": "01",
    "MOVER": "04",
    "MOVEM": "05",
    "READ": "09",
    "PRINT": "10"
}
DL = {
    "DS": "02"
}
AD = {
    "START": "01",
    "END": "02"
}
REG = {
    "AREG": "01",
    "BREG": "02",
    "CREG": "03",
    "DREG": "04"
}
def read_input(file_name):
    with open(file_name, 'r') as f:
        return [line.strip() for line in f if line.strip()]
def assembler_pass(lines):
    lc = 0
    symbol_table = {}
    literal_table = []
    pool_table = [0]
    output_rows = []
    sym_index = 1
    for line in lines:
        parts = line.split()

        if parts[0] == "START":
            lc = int(parts[1])
            ic = f"(AD,{AD['START']}) (C,{lc})"
            output_rows.append((lc, line, ic, "-"))
            continue

        if parts[0] == "END":
            ic = f"(AD,{AD['END']})"
            output_rows.append((lc, line, ic, "-"))
            break

        # Declarative
        if len(parts) == 3 and parts[1] == "DS":
            symbol = parts[0]
            symbol_table[symbol] = lc

            ic = f"(DL,{DL['DS']}) (C,{parts[2]})"
            output_rows.append((lc, line, ic, "-"))

            lc += int(parts[2])
            continue

        opcode = parts[0]

        if opcode in IS:
            if len(parts) == 2:  # READ A / PRINT C
                symbol = parts[1]
                if symbol not in symbol_table:
                    symbol_table[symbol] = lc

                sym_no = list(symbol_table.keys()).index(symbol) + 1
                ic = f"(IS,{IS[opcode]}) (S,{sym_no})"

                mc = f"{lc} {IS[opcode]} 00 {symbol_table[symbol]}"

            elif len(parts) == 3:  # MOVER AREG, A
                reg = parts[1].replace(",", "")
                symbol = parts[2]

                if symbol not in symbol_table:
                    symbol_table[symbol] = lc

                sym_no = list(symbol_table.keys()).index(symbol) + 1
                ic = f"(IS,{IS[opcode]}) ({REG[reg]}) (S,{sym_no})"

                mc = f"{lc} {IS[opcode]} {REG[reg]} {symbol_table[symbol]}"

            output_rows.append((lc, line, ic, mc))
            lc += 1

    return output_rows, symbol_table, literal_table, pool_table
def print_output(rows, symtab, littab, pooltab):
    print("\n=== ASSEMBLER OUTPUT ===\n")
    print(f"{'Assembly Code':<25} {'Intermediate Code':<30} {'Machine Code'}")
    print("-" * 80)
    for lc, asm, ic, mc in rows:
        ic_with_lc = f"{lc} {ic}"
        print(f"{asm:<25} {ic_with_lc:<30} {mc}")

    print("\n=== SYMBOL TABLE ===")
    print("Index\tSymbol\tAddress")
    for i, (sym, addr) in enumerate(symtab.items(), start=1):
        print(f"{i}\t{sym}\t{addr}")
    print("\n=== LITERAL TABLE ===")
    if littab:
        print("Index\tLiteral\tAddress")
        for i, lit in enumerate(littab, start=1):
            print(f"{i}\t{lit[0]}\t{lit[1]}")
    else:
        print("Empty")

    print("\n=== POOL TABLE ===")
    print("Pool Index\tLiteral Index")
    for i, val in enumerate(pooltab):
        print(f"{i}\t\t{val}")
file_name = "input.txt"  # your input file
lines = read_input(file_name)
rows, symtab, littab, pooltab = assembler_pass(lines)
print_output(rows, symtab, littab, pooltab)