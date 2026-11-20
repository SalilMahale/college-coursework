def generate_3ac(expression):
    lhs, rhs = expression.split("=")
    lhs = lhs.strip()
    rhs = rhs.strip()

    operators = ['+', '-', '*', '/']

    tokens = []
    num = ""

    # Tokenize expression
    for ch in rhs:
        if ch in operators:
            tokens.append(num.strip())
            tokens.append(ch)
            num = ""
        else:
            num += ch
    tokens.append(num.strip())

    temp_count = 1
    three_ac = []
    quadruples = []
    triples = []
    temp_map = {}

    # Handle * and /
    i = 0
    while i < len(tokens):
        if tokens[i] in ['*', '/']:
            op = tokens[i]
            arg1 = tokens[i-1]
            arg2 = tokens[i+1]

            temp = f"t{temp_count}"
            temp_count += 1

            three_ac.append(f"{temp} = {arg1} {op} {arg2}")
            quadruples.append((op, arg1, arg2, temp))

            if arg1 in temp_map:
                arg1 = f"({temp_map[arg1]})"
            if arg2 in temp_map:
                arg2 = f"({temp_map[arg2]})"

            triples.append((op, arg1, arg2))
            temp_map[temp] = len(triples) - 1

            tokens[i-1:i+2] = [temp]
            i = 0
        else:
            i += 1

    # Handle + and -
    i = 0
    while i < len(tokens):
        if tokens[i] in ['+', '-']:
            op = tokens[i]
            arg1 = tokens[i-1]
            arg2 = tokens[i+1]

            temp = f"t{temp_count}"
            temp_count += 1

            three_ac.append(f"{temp} = {arg1} {op} {arg2}")
            quadruples.append((op, arg1, arg2, temp))

            if arg1 in temp_map:
                arg1 = f"({temp_map[arg1]})"
            if arg2 in temp_map:
                arg2 = f"({temp_map[arg2]})"

            triples.append((op, arg1, arg2))
            temp_map[temp] = len(triples) - 1

            tokens[i-1:i+2] = [temp]
            i = 0
        else:
            i += 1

    result = tokens[0]

    # Final assignment
    three_ac.append(f"{lhs} = {result}")
    quadruples.append(("=", result, "-", lhs))

    if result in temp_map:
        result = f"({temp_map[result]})"

    # FIXED TRIPLE FORMAT
    triples.append(("=", lhs, result))

    return three_ac, quadruples, triples


# Main program
n = int(input("Enter number of statements: "))

for _ in range(n):
    expr = input("Enter statement: ")

    tac, quad, trip = generate_3ac(expr)

    print("\nThree Address Code:")
    for line in tac:
        print(line)

    print("\nQuadruples:")
    print("Op\tArg1\tArg2\tResult")
    for q in quad:
        print(f"{q[0]}\t{q[1]}\t{q[2]}\t{q[3]}")

    print("\nTriples:")
    print("Index\tOp\tArg1\tArg2")
    for i, t in enumerate(trip):
        print(f"{i}\t{t[0]}\t{t[1]}\t{t[2]}")

    print("\n----------------------\n")