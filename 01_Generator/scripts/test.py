import networkx as nx
import matplotlib.pyplot as plt

def create_factor_graph(variables, factors, edges):
    """
    Create a factor graph using networkx.

    Parameters:
    - variables: List of variable node names (e.g., ['X1', 'X2']).
    - factors: List of factor node names (e.g., ['f1', 'f2']).
    - edges: List of tuples defining connections (e.g., [('X1', 'f1'), ('X2', 'f1')]).
    
    Returns:
    - G: A networkx graph representing the factor graph.
    """
    G = nx.Graph()

    # Add variable and factor nodes
    G.add_nodes_from(variables, type='variable')
    G.add_nodes_from(factors, type='factor')

    # Add edges between variables and factors
    G.add_edges_from(edges)

    return G

def visualize_factor_graph(G):
    """
    Visualize a factor graph using matplotlib.

    Parameters:
    - G: A networkx graph representing the factor graph.
    """
    pos = nx.spring_layout(G)

    # Separate variable and factor nodes
    variable_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'variable']
    factor_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'factor']

    # Draw variable nodes in one color and factor nodes in another
    nx.draw_networkx_nodes(G, pos, nodelist=variable_nodes, node_color='lightblue', label='Variables', node_size=800)
    nx.draw_networkx_nodes(G, pos, nodelist=factor_nodes, node_color='lightgreen', label='Factors', node_size=800)
    nx.draw_networkx_edges(G, pos, edge_color='black')
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Add legend
    plt.legend(scatterpoints=1, loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('Factor Graph')
    plt.axis('off')
    plt.show()

# Example Usage
if __name__ == "__main__":
    # Define variables, factors, and edges
    variables = ['X1', 'X2', 'X3']
    factors = ['f1', 'f2']
    edges = [('X1', 'f1'), ('X2', 'f1'), ('X2', 'f2'), ('X3', 'f2')]

    # Create and visualize the factor graph
    G = create_factor_graph(variables, factors, edges)
    visualize_factor_graph(G)

# Explanation:

#     Graph Representation:
#         Variables are represented as one type of node.
#         Factors are represented as another type of node.
#         Edges connect variables to factors.

#     Visualization:
#         Variable nodes are colored (e.g., light blue).
#         Factor nodes are differently colored (e.g., light green).
#         The graph is laid out using a spring layout for aesthetic placement.

#     Example Input:
#         Variables: ['X1', 'X2', 'X3']
#         Factors: ['f1', 'f2']
#         Edges: [('X1', 'f1'), ('X2', 'f1'), ('X2', 'f2'), ('X3', 'f2')]

# Output:

# A graphical representation of the factor graph with variables and factors visually distinct, and their connections clearly depicted.

# Would you like further customization or extensions (e.g., saving the graph, adding weights)?