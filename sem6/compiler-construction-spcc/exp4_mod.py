import sys
import re

# ─────────────────────────────────────────────
# 1.  Read grammar & precedence table from file
# ─────────────────────────────────────────────

def parse_input_file(filepath):
    """
    Parses a file with two sections:
      --- GRAMMAR PRODUCTIONS ---
      E -> E + T
      ...

      --- PRECEDENCE RELATIONS ---
      + < *
      + > +
      * > *
      id > $
      $ Accept $        ← accept condition
      id - id           ← '-' means error / no relation
      ...

    Returns:
      productions  : list of (lhs, [rhs_symbols])
      prec_table   : dict  { (a, b): '<' | '>' | '=' | 'A' | 'E' }
      terminals    : ordered list of terminals found in the relation section
    """
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

        # ── Section headers ──
        if 'GRAMMAR PRODUCTIONS' in line.upper():
            section = 'grammar'
            continue
        if 'PRECEDENCE RELATIONS' in line.upper():
            section = 'prec'
            continue

        # ── Grammar section ──
        if section == 'grammar':
            for sep in ['->', '→']:
                if sep in line:
                    lhs, rhs = line.split(sep, 1)
                    productions.append((lhs.strip(), rhs.strip().split()))
                    break

        # ── Precedence relations section ──
        elif section == 'prec':
            parts = line.split()
            if len(parts) < 3:
                continue

            a, rel, b = parts[0], parts[1], parts[2]

            # Normalise 'id' → 'id' (keep as-is); collect terminals
            for sym in (a, b):
                if sym not in terminals_set:
                    terminals_set.add(sym)
                    terminals_ordered.append(sym)

            # Map relation string
            if rel == '<':
                prec_table[(a, b)] = '<'
            elif rel == '>':
                prec_table[(a, b)] = '>'
            elif rel in ('=', '=='):
                prec_table[(a, b)] = '='
            elif rel.lower() == 'accept':
                prec_table[(a, b)] = 'A'   # e.g. "$ Accept $"
            elif rel == '-':
                prec_table[(a, b)] = 'E'   # explicit error / no relation
            # anything else: ignore

    return productions, prec_table, terminals_ordered


def get_relation(prec_table, a, b):
    """Look up relation from the parsed table; return 'E' if not found."""
    return prec_table.get((a, b), 'E')


# ─────────────────────────────────────────────
# 2.  Print the precedence table
# ─────────────────────────────────────────────

def print_precedence_table(prec_table, terminals):
    print("\n--- OUTPUT 1: PRECEDENCE TABLE (Read from file) ---")

    col_w = 6
    # Header
    header = f"{'':>{col_w}}" + "".join(f"{t:^{col_w}}" for t in terminals)
    print(header)
    print("-" * len(header))

    for row in terminals:
        line = f"{row:>{col_w}}"
        for col in terminals:
            cell = get_relation(prec_table, row, col)
            if cell == 'E':
                cell = ' '
            line += f"{cell:^{col_w}}"
        print(line)
    print("-" * len(header))


# ─────────────────────────────────────────────
# 3.  Tokeniser
# ─────────────────────────────────────────────

def tokenise(input_string, grammar_terminals):
    """
    Converts a raw expression string into a list of tokens that match
    the terminal symbols used in the grammar / precedence table.

    Strategy:
      - If the precedence table uses 'id', map every identifier/variable to 'id'.
      - Otherwise keep single-char terminals as-is.
    """
    use_id = 'id' in grammar_terminals

    tokens = []
    i = 0
    s = input_string.strip()
    while i < len(s):
        ch = s[i]
        if ch == ' ':
            i += 1
            continue
        # Multi-char identifier?
        if ch.isalpha() or ch == '_':
            j = i + 1
            while j < len(s) and (s[j].isalnum() or s[j] == '_'):
                j += 1
            word = s[i:j]
            tokens.append('id' if use_id else word)
            i = j
        else:
            tokens.append(ch)
            i += 1

    tokens.append('$')
    return tokens


# ─────────────────────────────────────────────
# 4.  Operator Precedence Parser
# ─────────────────────────────────────────────

def get_top_terminal(stack, grammar_terminals):
    """Return the rightmost terminal on the stack."""
    for sym in reversed(stack):
        if sym in grammar_terminals or sym == '$':
            return sym
    return '$'


def parse(input_string, prec_table, grammar_terminals, productions):
    print("\n--- OUTPUT 2: STACK IMPLEMENTATION ---")

    tokens = tokenise(input_string, grammar_terminals)
    stack  = ['$']
    ptr    = 0

    print(f"{'STACK':<25} {'INPUT':<25} {'ACTION'}")
    print("-" * 65)

    def show(action):
        stk_str = ' '.join(stack)
        inp_str = ' '.join(tokens[ptr:])
        print(f"{stk_str:<25} {inp_str:<25} {action}")

    while ptr < len(tokens):
        top_term = get_top_terminal(stack, grammar_terminals)
        curr     = tokens[ptr]
        rel      = get_relation(prec_table, top_term, curr)

        if rel == 'A':          # ── ACCEPT ──
            show("ACCEPTED")
            return True

        elif rel == '<' or rel == '=':    # ── SHIFT ──
            show(f"Shift  ({top_term} {rel} {curr})")
            stack.append(curr)
            ptr += 1

        elif rel == '>':        # ── REDUCE ──
            show(f"Reduce ({top_term} {rel} {curr})")
            # Pop the handle: everything down to (and including) the symbol
            # whose relation with the symbol before it is '<'
            handle = []
            while True:
                top = stack.pop()
                handle.insert(0, top)
                new_top = get_top_terminal(stack, grammar_terminals)
                prev_rel = get_relation(prec_table, new_top,
                                        next((s for s in handle
                                              if s in grammar_terminals), top))
                if prev_rel == '<':
                    break
                if new_top == '$' and len(stack) == 1:
                    break

            # Find matching production (match terminal skeleton)
            handle_terms = [s for s in handle if s in grammar_terminals]
            lhs = None
            for plhs, prhs in productions:
                prhs_terms = [s for s in prhs
                              if s in grammar_terminals]
                if prhs_terms == handle_terms:
                    lhs = plhs
                    break

            if lhs is None:
                # Fallback: just push a generic non-terminal E
                lhs = productions[0][0] if productions else 'E'

            stack.append(lhs)

        else:                   # ── ERROR ──
            show(f"REJECTED — no relation between '{top_term}' and '{curr}'")
            return False

    show("REJECTED — unexpected end of input")
    return False


# ─────────────────────────────────────────────
# 5.  Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Determine input file
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"   # default

    print(f"[INFO] Reading grammar and precedence table from: {filepath}\n")

    productions, prec_table, terminals = parse_input_file(filepath)

    # Show loaded grammar
    print("--- GRAMMAR PRODUCTIONS ---")
    for lhs, rhs in productions:
        print(f"  {lhs} -> {' '.join(rhs)}")

    # Build set of terminals (for stack lookups)
    grammar_terminals = set(terminals)

    # Output 1: Precedence table
    print_precedence_table(prec_table, terminals)

    # Output 2: Parse an input string
    print("\n[INFO] Enter expression using variables and operators from the grammar.")
    print("[INFO] Variables (a, b, c, id, x, …) are automatically mapped to 'id'.\n")

    user_input = input("Enter string to parse: ").strip()

    if not user_input:
        print("No input provided. Exiting.")
        sys.exit()

    print(f"\nParsing: {user_input}")
    parse(user_input, prec_table, grammar_terminals, productions)
