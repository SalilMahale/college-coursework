def reflex_agent(location, status):
    if status == 'Dirty':
        return 'Suck'
    elif location == 'Left':
        return 'Move Right'
    elif location == 'Right':
        return 'Move Left'

def run_simulation():
    
    loc = input("Enter initial location of Vacuum (Left/Right): ").strip().capitalize()
    status_left = input("Is the Left room Dirty or Clean? ").strip().capitalize()
    status_right = input("Is the Right room Dirty or Clean? ").strip().capitalize()

    rooms = {'Left': status_left, 'Right': status_right}
    current_loc = loc

    print("\nStarting cleaning process")

    while True:
        current_status = rooms[current_loc]
        print(f"\nLocation: {current_loc} | Status: {current_status}")

        # Check if world is completely clean
        if rooms['Left'] == 'Clean' and rooms['Right'] == 'Clean':
            print("Both rooms are Clean. Goal reached! Exiting...")
            break

        # Agent decides action
        action = reflex_agent(current_loc, current_status)
        print(f"Agent Action: {action}")

        # Execute action
        if action == 'Suck':
            rooms[current_loc] = 'Clean'
            print(f"Result: {current_loc} is now Clean.")
        elif action == 'Move Right':
            current_loc = 'Right'
        elif action == 'Move Left':
            current_loc = 'Left'

if __name__ == "__main__":
    run_simulation()