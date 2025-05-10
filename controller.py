# controller.py — Assignment 4
# SHA-256 Watermark for Uniqueness

import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import random

# === Uniqueness watermark ===
student_id = "890607568"
salt = "NeoDDaBRgX5a9"
watermark = hashlib.sha256((student_id + salt).encode()).hexdigest()
print(f"Watermark: {watermark}")

# === Initialize Network ===
network = nx.Graph()
active_flows = []
link_utilization = {}

# === Default Topology ===
def build_topology():
    network.add_weighted_edges_from([
        ("A", "B", 1),
        ("B", "C", 1),
        ("C", "D", 1),
        ("A", "D", 2),
        ("C", "E", 1)
    ])

# === Path and Flow Logic ===
def get_shortest_path(src, dst):
    try:
        return nx.shortest_path(network, source=src, target=dst, weight='weight')
    except nx.NetworkXNoPath:
        return None

def get_all_paths(src, dst):
    try:
        return list(nx.all_shortest_paths(network, source=src, target=dst, weight='weight'))
    except nx.NetworkXNoPath:
        return []

def generate_flow_table(node):
    table = {}
    for dst in network.nodes:
        if dst != node:
            paths = get_all_paths(node, dst)
            if paths:
                next_hops = {path[1] for path in paths}
                table[dst] = list(next_hops)
    return table

# === Inject Flow ===
def inject_flow(src, dst, priority="NORMAL"):
    paths = get_all_paths(src, dst)
    if not paths:
        print("No path found.")
        return
    chosen_path = random.choice(paths)
    active_flows.append({"src": src, "dst": dst, "path": chosen_path, "priority": priority})
    for i in range(len(chosen_path) - 1):
        link = (chosen_path[i], chosen_path[i + 1])
        link_utilization[link] = link_utilization.get(link, 0) + 1
    print(f"Injected {priority} flow: {' → '.join(chosen_path)}")

# === Simulate Link Failure ===
def simulate_failure(u, v):
    if network.has_edge(u, v):
        network.remove_edge(u, v)
        print(f"Simulated failure on link: {u}–{v}")
    else:
        print("Link does not exist.")

# === Visualization ===
def draw_network():
    pos = nx.spring_layout(network)
    nx.draw(network, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    labels = nx.get_edge_attributes(network, 'weight')
    nx.draw_networkx_edge_labels(network, pos, edge_labels=labels)

    for flow in active_flows:
        path = flow["path"]
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(network, pos, edgelist=edges, edge_color='red', width=2)

    for link, count in link_utilization.items():
        print(f"Utilization {link[0]}–{link[1]}: {count}")

    plt.show()

# === CLI Interface ===
def cli():
    while True:
        print("\nCommands: show, flow <src> <dst> [priority], fail <u> <v>, table <node>, add <node>, link <n1> <n2> <weight>, exit")
        cmd = input(">>> ").strip().split()

        if not cmd:
            continue
        if cmd[0] == "show":
            draw_network()
        elif cmd[0] == "flow" and (len(cmd) == 3 or len(cmd) == 4):
            priority = cmd[3].upper() if len(cmd) == 4 else "NORMAL"
            inject_flow(cmd[1], cmd[2], priority)
        elif cmd[0] == "fail" and len(cmd) == 3:
            simulate_failure(cmd[1], cmd[2])
        elif cmd[0] == "table" and len(cmd) == 2:
            table = generate_flow_table(cmd[1])
            for dst, hops in table.items():
                print(f"To {dst} → Next hops: {', '.join(hops)}")
        elif cmd[0] == "add" and len(cmd) == 2:
            network.add_node(cmd[1])
            print(f"Added node {cmd[1]}")
        elif cmd[0] == "link" and len(cmd) == 4:
            try:
                weight = int(cmd[3])
                network.add_edge(cmd[1], cmd[2], weight=weight)
                print(f"Added link {cmd[1]}–{cmd[2]} with weight {weight}")
            except ValueError:
                print("Weight must be an integer.")
        elif cmd[0] == "exit":
            break
        else:
            print("Invalid command. Try again.")

# === Main Program ===
if __name__ == "__main__":
    build_topology()
    print("SDN Controller is running.")
    cli()
