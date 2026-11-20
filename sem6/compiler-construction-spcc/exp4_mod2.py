import sys
def parse_input_file(filepath):
    productions = []
    prec_table  = {}
    terminals_ordered = []
    terminals_set = set()
    section = None

    with open(filepath, encoding='utf-8') as f:
        lines = [l.strip() for l in f]

    for line in lines:
        if not line:
            continue
        if 'GRAMMAR PRODUCTIONS' in line.upper():
            section = 'grammar'; continue
        if 'PRECEDENCE RELATIONS' in line.upper():
            section = 'prec'; continue

        if section == 'grammar':
            for sep in ['->', 'u2192']:
                if sep in line:
                    lhs, rhs = line.split(sep, 1)
                    productions.append((lhs.strip(), rhs.strip().split()))
                    break
                
        elif section == 'prec':
            parts = line.split()
            if len(parts) < 3:
                continue
            a, rel, b = parts[0], parts[1], parts[2]
            for sym in (a, b):
                if sym not in terminals_set:
                    terminals_set.add(sym)
                    terminals_ordered.append(sym)
            if rel == '<':
                prec_table[(a, b)] = '<'
            elif rel == '>':
                prec_table[(a, b)] = '>'
            elif rel in ('=', '=='):
                prec_table[(a, b)] = '='
            elif rel.lower() == 'accept':
                prec_table[(a, b)] = 'A'
            elif rel == '-':
                prec_table[(a, b)] = 'E'

    return productions, prec_table, terminals_ordered


def get_relation(prec_table, a, b):
    return prec_table.get((a, b), 'E')

def print_precedence_table(prec_table, terminals):
    print("\n--- OUTPUT 1: PRECEDENCE TABLE ---")
    col_w = 6
    header = f"{'':>{col_w}}" + "".join(f"{t:^{col_w}}" for t in terminals)
    print(header)
    print("-" * len(header))
    for row in terminals:
        line = f"{row:>{col_w}}"
        for col in terminals:
            cell = get_relation(prec_table, row, col)
            line += f"{' ' if cell == 'E' else cell:^{col_w}}"
        print(line)
    print("-" * len(header))

def tokenise(input_string, grammar_terminals):
    tokens = []
    i = 0
    s = input_string.strip()
    while i < len(s):
        ch = s[i]
        if ch == ' ':
            i += 1; continue
        if ch.isalpha() or ch == '_':
            j = i + 1
            while j < len(s) and (s[j].isalnum() or s[j] == '_'):
                j += 1
            tokens.append('id')
            i = j
        else:
            tokens.append(ch)
            i += 1
    tokens.append('$')
    return tokens

def get_top_terminal(stack, grammar_terminals):
    for sym in reversed(stack):
        if sym in grammar_terminals or sym == '$':
            return sym
    return '$'


def match_production(handle, productions, non_terminals_set):
    def is_var(sym):
        return sym not in non_terminals_set and (sym.isalpha() or sym == 'id')

    for plhs, prhs in productions:
        if len(prhs) != len(handle):
            continue
        ok = True
        for rsym, hsym in zip(prhs, handle):
            r_nt = rsym in non_terminals_set
            h_nt = hsym in non_terminals_set
            if r_nt and h_nt:
                continue
            if r_nt != h_nt:
                ok = False; break
            if is_var(rsym) and is_var(hsym):
                continue
            if rsym != hsym:
                ok = False; break
        if ok:
            return plhs
    return None

def parse(input_string, prec_table, grammar_terminals, productions):
    print("\n--- OUTPUT 2: STACK IMPLEMENTATION ---")

    tokens = tokenise(input_string, grammar_terminals)
    stack  = ['$']
    ptr    = 0
    non_terminals_set = set(p[0] for p in productions)

    print(f"{'STACK':<25} {'INPUT':<25} {'ACTION'}")
    print("-" * 65)

    def show(action):
        print(f"{' '.join(stack):<25} {' '.join(tokens[ptr:]):<25} {action}")

    while ptr < len(tokens):
        top_term = get_top_terminal(stack, grammar_terminals)
        curr     = tokens[ptr]
        rel      = get_relation(prec_table, top_term, curr)

        if rel == 'A':
            show("ACCEPTED")
            return True

        elif rel in ('<', '='):
            show(f"Shift  ({top_term} {rel} {curr})")
            stack.append(curr)
            ptr += 1

        elif rel == '>':
            show(f"Reduce ({top_term} {rel} {curr})")

            top_idx = next(i for i in range(len(stack)-1, -1, -1)
                           if stack[i] in grammar_terminals)
            left_bound = 1  
            i = top_idx - 1
            while i >= 0:
                if stack[i] in grammar_terminals:
                    right_term = next(
                        (stack[k] for k in range(i+1, top_idx+1)
                         if stack[k] in grammar_terminals),
                        top_term)
                    r = get_relation(prec_table, stack[i], right_term)
                    if r == '<':
                        left_bound = i + 1
                        break
                i -= 1

            handle = stack[left_bound:]
            stack  = stack[:left_bound]

            lhs = match_production(handle, productions, non_terminals_set)
            if lhs is None:
                show(f"REJECTED — invalid handle {handle}")
                return False

            stack.append(lhs)

        else:
            show(f"REJECTED — no relation between '{top_term}' and '{curr}'")
            return False

    show("REJECTED — unexpected end of input")
    return False

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    print(f"[INFO] Reading grammar and precedence table from: {filepath}\n")

    productions, prec_table, terminals = parse_input_file(filepath)

    print("--- GRAMMAR PRODUCTIONS ---")
    for lhs, rhs in productions:
        print(f"  {lhs} -> {' '.join(rhs)}")

    grammar_terminals = set(terminals)
    print_precedence_table(prec_table, terminals)

    print("\n[INFO] Enter expression using variables and operators from the grammar.")
    print("[INFO] Variables (a, b, c, id, x, ...) are automatically mapped to 'id'.\n")

    user_input = input("Enter string to parse: ").strip()
    if not user_input:
        print("No input provided. Exiting.")
        sys.exit()

    print(f"\nParsing: {user_input}")
    parse(user_input, prec_table, grammar_terminals, productions)
