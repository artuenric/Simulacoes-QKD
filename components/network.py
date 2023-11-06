import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

class Network():
    """
    Um objeto para utilizar como rede.
    """
    def __init__(self) -> None:
        self.G = None
        self.channels = None
        self.topology = None
        self.controller = None
        
    def draw(self):
        # Plot the network
        pos = nx.spring_layout(self.G)  # Compute node positions for visualization

        # Draw nodes with their weights
        nx.draw_networkx_nodes(self.G, pos, node_color='#5DCCF8', node_size=500)
        
        # Draw node indices
        node_indices = {node: node for node in self.G.nodes}
        nx.draw_networkx_labels(self.G, pos, labels=node_indices, font_color='white')
        edge_weights = [self.channels.get((u, v), {}).get("fidelity_value", 0) for u, v in self.G.edges]
        
        # Draw edges with their weights
        edges = nx.draw_networkx_edges(self.G, pos, width=2, edge_color=edge_weights, edge_cmap=plt.cm.viridis)
                
        # Add a color bar to represent the weights
        cbar = plt.colorbar(edges, ax=plt.gca())
        cbar.ax.set_ylabel("Fidelity")
        
        # Display the initial plot
        plt.title("Topology Network")
        #plt.axis("off")
        plt.show()
         
    def set_controller(self, controller):
        """
        Define o controlador da rede.
        """
        self.controller = controller
    
    def set_lattice_topology(self, rows, cols):
        """
        Cria uma rede com topologia de grade.
        
        Args:
            rows (int): Número de linhas.
            cols (int): Número de colunas.
        """

        # Update network topology
        self.topology = "Lattice"
        
        # Create a lattice topology network
        G = nx.generators.lattice.grid_2d_graph(rows, cols)
        G = nx.convert_node_labels_to_integers(G)
        # Assign random weights and initial memory to nodes
        for node in G.nodes:
            G.nodes[node]["qubits_available"] = 50
        # Initialize channels
        channels = {(u, v): {
            #EPRs
            "epr_available": 20 ,
            "fidelity_value": random.uniform(0.90, 1),      
        } for u, v in G.edges}
        channels.update({(v, u): {
        # EPRs
            "epr_available": 20,
            "fidelity_value": random.uniform(0.90, 1),
        } for u, v in G.edges})  # Add reverse direction channels

        # Update network graphics and channels
        self.G = G
        self.channels = channels

    def set_ring_topology(self, num_nodes):
        """
        Cria uma rede com topologia de anel.
        
        Args:
            num_nodes (int): Número de nós.
        """
        
        # Create a ring topology network
        self.G = nx.cycle_graph(num_nodes)
        self.G = nx.convert_node_labels_to_integers(self.G)

        # Assign random weights and initial memory to nodes
        for node in self.G.nodes:
            self.G.nodes[node]["qubits_available"] = random.randint(4, 10)
            self.G.nodes[node]["qubits_reducing_rate"] = random.uniform(0.01, 0.1)
            self.G.nodes[node]["qubits_increasing_rate"] = random.uniform(0.3, 0.5)
            self.G.nodes[node]["qubits_threshold"] = random.randint(2, 4)   

        # Initialize channels
        self.channels = {(u, v): {
            #EPRs
            "epr_available": random.randint(1, 2),   
            "epr_max_capacity": random.uniform(0.5, 0.95),
            #fidelity 
            "fidelity_value": random.uniform(0.85, 1),
            "fidelity_reducing_rate": random.uniform(0.01, 0.1),
            "fidelity_threshold": random.uniform(0.5, 0.8),
            "fidelity_reposition_rate": random.uniform(0.1, 0.2),
        } for u, v in self.G.edges}

        self.channels.update({(v, u): {
        #EPRs
            "epr_available": random.randint(1, 2),   
            "epr_max_capacity": random.uniform(0.5, 0.95),
            #fidelity 
            "fidelity_value": random.uniform(0.85, 1),
            "fidelity_reducing_rate": random.uniform(0.01, 0.1),
            "fidelity_threshold": random.uniform(0.5, 0.8),
            "fidelity_reposition_rate": random.uniform(0.1, 0.2),
        } for u, v in self.G.edges})  # Add reverse direction channels

    def set_star_topology(self, num_nodes):
        """
        Cria uma rede com topologia de estrela.

        Args:
            num_nodes (int): Número de nós.
        """
        
        # Create a star topology network
        self.G = nx.star_graph(num_nodes - 1)  # num_nodes includes the center node
        self.G = nx.convert_node_labels_to_integers(self.G)

        # Assign random weights and initial memory to nodes
        for node in self.G.nodes:
            self.G.nodes[node]["qubits_available"] = random.randint(4, 10)
            self.G.nodes[node]["qubits_reducing_rate"] = random.uniform(0.01, 0.1)
            self.G.nodes[node]["qubits_increasing_rate"] = random.uniform(0.3, 0.5)
            self.G.nodes[node]["qubits_threshold"] = random.randint(2, 4)   

        # Initialize channels
        self.channels = {(u, v): {
            #EPRs
            "epr_available": random.randint(1, 2),   
            "epr_max_capacity": random.uniform(0.5, 0.95),
            #fidelity 
            "fidelity_value": random.uniform(0.85, 1),
            "fidelity_reducing_rate": random.uniform(0.01, 0.1),
            "fidelity_threshold": random.uniform(0.5, 0.8),
            "fidelity_reposition_rate": random.uniform(0.1, 0.2),
        } for u, v in self.G.edges}

        self.channels.update({(v, u): {
        #EPRs
            "epr_available": random.randint(1, 2),   
            "epr_max_capacity": random.uniform(0.5, 0.95),
            #fidelity 
            "fidelity_value": random.uniform(0.85, 1),
            "fidelity_reducing_rate": random.uniform(0.01, 0.1),
            "fidelity_threshold": random.uniform(0.5, 0.8),
            "fidelity_reposition_rate": random.uniform(0.1, 0.2),
        } for u, v in self.G.edges})  # Add reverse direction channels
    
    def create_line_topology_network(self, num_nodes):
        """
        Cria uma rede com topologia de linha.
        
        Args:
            num_nodes (int): Número de nós.
        """
        # Create a line topology (path graph)
        self.G = nx.path_graph(num_nodes)
        self.G = nx.convert_node_labels_to_integers(self.G)

        # Assign random weights and initial memory to nodes
        for node in self.G.nodes:
            self.G.nodes[node]["qubits_available"] = random.randint(4, 10)
            self.G.nodes[node]["qubits_reducing_rate"] = random.uniform(0.01, 0.1)
            self.G.nodes[node]["qubits_increasing_rate"] = random.uniform(0.3, 0.5)
            self.G.nodes[node]["qubits_threshold"] = random.randint(2, 4)

        # Initialize channels
        self.channels = {(u, v): {
            # EPRs
            "epr_available": random.randint(1, 2),   
            "epr_max_capacity": random.uniform(0.5, 0.95),
            # fidelity 
            "fidelity_value": random.uniform(0.85, 1),
            "fidelity_reducing_rate": random.uniform(0.01, 0.1),
            "fidelity_threshold": random.uniform(0.5, 0.8),
            "fidelity_reposition_rate": random.uniform(0.1, 0.2),
        } for u, v in self.G.edges}

        self.channels.update({(v, u): {
            # EPRs
            "epr_available": random.randint(1, 2),   
            "epr_max_capacity": random.uniform(0.5, 0.95),
            # fidelity 
            "fidelity_value": random.uniform(0.85, 1),
            "fidelity_reducing_rate": random.uniform(0.01, 0.1),
            "fidelity_threshold": random.uniform(0.5, 0.8),
            "fidelity_reposition_rate": random.uniform(0.1, 0.2),
        } for u, v in self.G.edges})  # Add reverse direction channels 
    
    def random_alice_bob(self, diff_nodes):
        """
        Escolhe um nó aleatório na rede para Alice e outro para Bob. Útil para protocolos com um remetente e um receptor.

        Args:
            diff_nodes (int): Número entre os nós.

        Returns:
            alice, bob (int) : Número correspondente ao nó do grafo.
        """
        sender = random.choice(list(self.G.nodes))
        receiver = sender + diff_nodes
        if receiver >= self.G.number_of_nodes():
            receiver -= self.G.number_of_nodes()  
        
        # Evitar que os nós sejam os mesmos
        while sender == receiver:
            receiver = random.choice(list(self.G.nodes))
        alice, bob = sender, receiver
        
        return alice, bob
    

    def send_qubits(self, route, qubits):
        """
        Envia os qubits em uma lista pela rota escolhida.

        Args:
            route (rota): Rota definida para o envio do qubit.
            qubits (list): Lista com qubits preparados.

        Returns:
            received_qubits (list): Lista com os qubits que chegaram no Bob.
        """
        
        # Considerar fazer com fidelidades dos canais
        total_fidelity = sum(self.channels[(route[i], route[i + 1])]["fidelity_value"] for i in range(len(route) - 1))
        num_segments = len(route) - 1
        media_fidelity = total_fidelity / num_segments

        received_qubits = []
        
        for i in route[:-1]:
            for indice, qubit in enumerate(qubits):
                # if random.uniform(0, 1) > media_fidelity:
                    #print(f"O {indice}° sofreu interferência")
                    #qubit.interference()
                received_qubits.append(qubit)

        return received_qubits
    
    def send_eprs(self, route, eprs):
        """
        Transmite os EPRs em uma lista pela rota escolhida.

        Args:
            route (rota): Rota definida para o envio do qubit.
            eprs (list): Lista com pares emaranhados preparados.

        Returns:
            received_qubits (list): Lista com os qubits que chegaram no Bob.
        """
        # Considerar fazer com fidelidades dos canais
        total_fidelity = sum(self.channels[(route[i], route[i + 1])]["fidelity_value"] for i in range(len(route) - 1))
        num_segments = len(route) - 1
        media_fidelity = total_fidelity / num_segments

        received_qubits = []
        
        for i in route[:-1]:
            for indice, epr in enumerate(eprs):
                # if random.uniform(0, 1) > media_fidelity:
                    #print(f"O {indice}° sofreu interferência")
                    #epr.interference()
                received_qubits.append(epr.qubit1)
                
        return received_qubits