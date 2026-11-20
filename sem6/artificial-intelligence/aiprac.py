loc = input("\nenter the current location: ")
status_a = input("\nenter status of room A: ")
status_b = input("\nenter status of room B: ")

environment = {
    'location' : loc,
    'A' : status_a,
    'B' : status_b
}

print(f"\ncurrent loc: {environment['location']} | A: {environment['A']} | B: {environment['B']}")

flag = False
max_steps = 10
steps = 0

while steps < max_steps:
    loc = environment['location']
    status = environment[loc]
    
    if status == 'dirty':
        action = 'clean'
        flag = False
    elif loc == 'A':
        action = 'move right'
        flag = True
    elif loc == 'B':
        action = 'move left'
        flag = True

    if action == 'clean':
        environment[loc] = 'clean'
    elif action == 'move right':
        environment['location'] = 'B'
    elif action == 'move left':
        environment['location'] = 'A'
    
    
    loc = environment['location']
    print(f'\nloc: {loc} | A: {environment["A"]} | B: {environment["B"]}')
    if flag == True and environment[loc] == 'clean':
        break
    
    steps = steps+1
        

