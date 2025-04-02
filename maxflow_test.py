from collections import deque, defaultdict
import networkx as nx
import pandas as pd

class Graph:
    """Represents a directed graph with capacities and residuals."""

    def __init__(self, dataframe):
        self.graph = nx.MultiDiGraph()
        self._build_graph(dataframe)

    def _build_graph(self, dataframe):
        """Build the graph from a DataFrame."""
        for row in dataframe.itertuples():
            u = row.source
            v = row.destination
            cap = row.capacity

            # Add the edge with capacity and residual
            self.graph.add_edge(u, v, weight=cap, residual=cap, identifier=row.Index)
            self.graph.add_edge(v, u, weight=0, residual=0)

    def get_networkx_graph(self):
        """Return the underlying NetworkX graph."""
        return self.graph

class FordFulkerson:
    """Implements the Ford-Fulkerson algorithm to find max flow."""

    def __init__(self, graph):
        self.graph = graph
        self.paths = defaultdict(list)

    def bfs(self, source, sink, parent):
        """Breadth-First Search to find an augmenting path."""
        queue = deque([source])
        visited = set([source])
        parent.clear()

        while queue:
            current = queue.popleft()

            for neighbour, edges in self.graph[current].items():
                for edge_data in edges.values():  # Modified to access all multi-edges
                    residual = edge_data['residual']

                    if neighbour not in visited and residual > 0:
                        parent[neighbour] = (current, edge_data)  # Store edge data for backtracking

                        if neighbour == sink:
                            path = []
                            node = sink
                            while node in parent:
                                path.append(node)
                                node, _ = parent[node]
                            path.append(source)
                            path.reverse()

                            self.paths[sink].append((path, None))
                            return True

                        visited.add(neighbour)
                        queue.append(neighbour)

        return False

    def compute_max_flow(self, source, sink):
        """Calculate the maximum flow from source to sink."""
        max_flow = 0
        parent = {}

        while self.bfs(source, sink, parent):
            current = sink
            path_flow = float('Inf')

            # Find the maximum flow through the path found
            while current != source:
                prev, edge_data = parent[current]
                residual = edge_data['residual']
                path_flow = min(path_flow, residual)
                current = prev

            # Update the last path's flow
            self.paths[sink][-1] = (self.paths[sink][-1][0], path_flow)

            # Update residual capacities of the edges and reverse edges
            current = sink
            while current != source:
                prev, edge_data = parent[current]

                # MARK: Modified to access the specific edge by key
                for edge_key, edge_attr in self.graph[prev][current].items():
                    if edge_attr == edge_data:
                        self.graph[prev][current][edge_key]['residual'] -= path_flow

                # Update reverse edges
                for edge_key, edge_attr in self.graph[current][prev].items():
                    if edge_attr['weight'] == 0:  # Reverse edge check
                        self.graph[current][prev][edge_key]['residual'] += path_flow

                current = prev

            max_flow += path_flow

        return max_flow

class CsvHandler:
    """Handles interactions with CSV files for this script."""

    def __init__(self):
        self.dataframe = pd.DataFrame()

    def read_data(self, path):
        """Reads data from a CSV file and stores it in a DataFrame."""
        self.dataframe = pd.read_csv(path)
        return self.dataframe

    def export_flows(self, graph, dataframe):
        """Updates the DataFrame with flow values from the computed graph."""
        flow_dict = {}

        for _, _, _, data in graph.edges(data=True, keys=True):
            if 'identifier' in data:
                identifier = data['identifier']
                capacity = data['weight']  # Original capacity
                residual = data['residual']  # Remaining capacity after max flow computation

                flow_sent = capacity - residual

                flow_dict[identifier] = flow_sent

        dataframe['flow'] = dataframe.index.map(flow_dict).fillna(0).astype(int)

        return dataframe

if __name__ == "__main__":
    # Load network data
    csv_object = CsvHandler()
    network_df = csv_object.read_data("b_testing/data.csv")

    # Initialize graph and algorithm
    graph_obj = Graph(network_df)
    ntwrk = graph_obj.get_networkx_graph()
    ford_fulkerson = FordFulkerson(ntwrk)

    # Compute max flow
    src, snk = "S", "T"
    flow_max = ford_fulkerson.compute_max_flow(src, snk)

    # Output results
    new_network_df = csv_object.export_flows(ntwrk, network_df)
    new_network_df.to_csv("b_testing/data_with_flows.csv", index=False)

    print(f"Max Flow: {flow_max}\n")
    if snk in ford_fulkerson.paths:
        print(f"All augmenting paths to {snk} and their flows:")
        for _path, flow in ford_fulkerson.paths[snk]:
            print(f"Path: {_path}, Flow: {flow}")
    else:
        print(f"No paths to sink {snk}.")
