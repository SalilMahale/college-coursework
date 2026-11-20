def build_adjacency_matrix(num_nodes, edges):
    # Initialize adjacency matrix with 0 (no edges)
    adj = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    # Fill adjacency matrix: adj[i][j] = 1 if there is an edge from i to j
    for (src, dst) in edges:
        adj[src][dst] = 1
    return adj

def pretty_vec(vec, prec=6):
    return "[" + ", ".join(f"{x:.{prec}f}" for x in vec) + "]"

def page_rank(num_nodes, edges, iterations, damping):
    adj = build_adjacency_matrix(num_nodes, edges)
    
    print("Adjacency Matrix (1 indicates edge from row node to column node):")
    for i in range(num_nodes):
        print(" ".join(str(adj[i][j]) for j in range(num_nodes)))
    print()
    
    # Initialize PageRank values uniformly
    pr = [1 / num_nodes] * num_nodes

    # Build outgoing counts for each node
    out_counts = [sum(row) for row in adj]

    print("After iteration 0:")
    for i, rank in enumerate(pr):
        print(f"Node {i}: {rank:.6f}")
    print()

    for it in range(1, iterations + 1):
        new_pr = [(1 - damping) ] * num_nodes
        for node in range(num_nodes):
            rank_sum = 0
            # Sum over all nodes with edges pointing to 'node'
            for src_node in range(num_nodes):
                if adj[src_node][node] == 1:
                    if out_counts[src_node] > 0:
                        rank_sum += pr[src_node] / out_counts[src_node]
            new_pr[node] += damping * rank_sum

        # Print one line of calculation for this iteration
        print(f"PR^{it} = {(1 - damping):.3f} + {damping:.3f} * (Sum of PRj / OutDegreej)")

        pr = new_pr
        print(f"After iteration {it}:")
        for i, rank in enumerate(pr):
            print(f"Node {i}: {rank:.6f}")
        print()

def main():
    num_nodes = int(input("Enter the number of nodes: "))
    edges = []

    print("For each node, enter the number of outgoing edges and their target nodes (0-indexed).")
    for node in range(num_nodes):
        out_count = int(input(f"Number of outgoing edges from node {node}: "))
        if out_count > 0:
            out_nodes = list(map(int, input(f"Enter the {out_count} outgoing nodes separated by space: ").split()))
            for dst in out_nodes:
                edges.append((node, dst))

    iterations = int(input("Enter the number of iterations: "))
    damping = float(input("Enter the damping factor (e.g., 0.85): "))

    page_rank(num_nodes, edges, iterations, damping)

if __name__ == "__main__":
    main()
