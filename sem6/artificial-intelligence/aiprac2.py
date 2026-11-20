graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

start = 'A'        # Where the agent starts
goal  = ['F']      # What the agent is looking for

def bfs():
    queue   = [start]         # Start with the starting node in queue
    visited = []              # Nobody visited yet
    parent  = {start: None}   # 'A' has no parent (it IS the start)
    step    = 1

    print("\n===== BFS =====")

    while queue:              # Keep going as long as queue is not empty

        print("\nStep", step)
        print("Queue  :", queue)
        print("Visited:", visited)

        node = queue.pop(0)   # Remove from FRONT of queue (FIFO)

        if node not in visited:
            visited.append(node)   # Mark this node as visited

            if node in goal:       # Did we find the goal?
                path = []
                temp = node

                while temp is not None:    # Trace back using parent dict
                    path.append(temp)
                    temp = parent[temp]

                print("\nGoal Found:", node)
                print("Path:", *reversed(path))   # Print path start→goal
                return

            for nbr in graph[node]:             # Look at all neighbors
                if nbr not in visited and nbr not in queue:
                    queue.append(nbr)           # Add unvisited to queue
                    parent[nbr] = node          # Remember who added this

        step += 1

    print("Goal Not Found")

def dfs():
    stack   = [start]         # Start with the starting node in stack
    visited = []
    parent  = {start: None}
    step    = 1

    print("\n===== DFS =====")

    while stack:              # Keep going as long as stack is not empty

        print("\nStep", step)
        print("Stack  :", stack)
        print("Visited:", visited)

        node = stack.pop()    # Remove from TOP of stack (LIFO)

        if node not in visited:
            visited.append(node)

            if node in goal:
                path = []
                temp = node

                while temp is not None:
                    path.append(temp)
                    temp = parent[temp]

                print("\nGoal Found:", node)
                print("Path:", *reversed(path))
                return

            for nbr in reversed(graph[node]):   # reversed() to maintain order
                if nbr not in visited and nbr not in stack:
                    stack.append(nbr)
                    parent[nbr] = node

        step += 1

    print("Goal Not Found")

bfs()
dfs()