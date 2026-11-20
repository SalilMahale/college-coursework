instructions = [
    'f=c+d',
    'e=a-f',
    'g=b*e'
]

result_map = {}
triples = []
quads = []

for i,expr in enumerate(instructions):
    result,rhs = expr.split('=')
    
    for oper in ['*','/','+','-']:
        if oper in rhs:
            arg1,arg2 = rhs.split(oper)
            break
    
    quads.append((oper,arg1,arg2,result))
    
    a1 = f'({result_map[arg1]})' if arg1 in result_map else arg1
    a2 = f'({result_map[arg2]})' if arg2 in result_map else arg2

    triples.append((oper,a1,a2))

print(f'\nquadruples:')
print(f'{'operator':<12}{'arg1':<8}{'arg2':<8}{'result'}')
for oper,arg1,arg2,result in quads:
    print(f'{oper:<12}{arg1:<8}{arg2:<8}{result}')
print()

