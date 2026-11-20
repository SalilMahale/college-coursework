def astar(start,goal):
    open_list = [(start,0)]
    visited = []
    while open_list:
        open_list.sort(key=lambda x: x[1] + h(x[0],goal))
        state,g= open_list.pop(0)
        if tuple(tuple(r) for r in state) in visited:
            continue
        visited.append(tuple(tuple(r) for r in state))
        for row in state:
            print(row)
        print()
        if state == goal:
            print(f'\ngoal found!')
            return
        for new_state in get_step(state):
            open_list.append((new_state,g+1))

def get_step(state):
    x,y = get_blank(state)
    directions = [(-1,0,'up'),(1,0,'down'),(0,-1,'left'),(0,1,'right')]
    result = []
    for dx,dy,name in directions:
        nx,ny = x+dx,y+dy
        if 0<=nx<3 and 0<=ny<3:
            new_state = [row[:] for row in state]
            new_state[x][y],new_state[nx][ny] = new_state[nx][ny],new_state[x][y]
            result.append((new_state))
    return result

def get_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i,j

def h(state,goal):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count = count+1
    return count

start = [[1,2,3],[4,0,5],[7,8,6]]
goal  = [[1,2,3],[4,5,6],[7,8,0]]
astar(start,goal)