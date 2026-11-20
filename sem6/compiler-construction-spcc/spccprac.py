# Simple Three-Address Code generator

expr = "a = b * c + d"   # you can change this expression

lhs, rhs = expr.split("=")
lhs = lhs.strip()
rhs = rhs.strip()

tokens = rhs.split()     # naive tokenizer
temp_count = 1
three_address = []

i = 0
while i < len(tokens):
    if tokens[i] in ["*", "/", "+", "-"]:
        # operator found, combine previous and next
        t = f"t{temp_count}"
        stmt = f"{t} = {tokens[i-1]} {tokens[i]} {tokens[i+1]}"
        three_address.append(stmt)

        # replace the three tokens with the temp
        tokens[i-1:i+2] = [t]
        temp_count += 1
        i = 0  # restart scan
    else:
        i += 1

# final assignment
three_address.append(f"{lhs} = {tokens[0]}")

# print result
for line in three_address:
    print(line)
