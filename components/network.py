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
        self.fidelity = 0.95
        
        
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
        
    def assign_to_net(self, G):
        """
        Atribui as propriedades dos nós e canais à rede.
        """
        for node in G.nodes:
            G.nodes[node]["qubits_available"] = random.randint(4, 10)
        
        # Initialize channels
        channels = {(u, v): {
            # EPRs
            "epr_available": random.randint(1, 2),   
            # fidelity 
            "fidelity_value": self.fidelity,
        } for u, v in G.edges}

        channels.update({(v, u): {
            # EPRs
            "epr_available": random.randint(1, 2),
            # Fidelity 
            "fidelity_value": self.fidelity,
        } for u, v in G.edges})  # Add reverse direction channels
        
        return G, channels
    
    def set_fully_connected_topology(self, num_nodes):
        """
        Cria uma rede com topologia malha (totalmente conectada).

        Args:
            num_nodes (int): Número de nós.
        """
        # Update network topology
        self.topology = "Fully Connected"
        
        # Create a fully connected (complete) network
        G = nx.complete_graph(num_nodes)
        G = nx.convert_node_labels_to_integers(G)
        
        # Assign properties to the nodes and channels
        self.G, self.channels = self.assign_to_net(self, G)
    
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
        
        # Assign properties to the nodes and channels
        self.G, self.channels = self.assign_to_net(G)
        

    def set_ring_topology(self, num_nodes):
        """
        Cria uma rede com topologia de anel.
        
        Args:
            num_nodes (int): Número de nós.
        """
        
        # Create a ring topology network
        G = nx.cycle_graph(num_nodes)
        G = nx.convert_node_labels_to_integers(G)
        
        # Assign properties to the nodes and channels
        self.G, self.channels = self.assign_to_net(G)
        

    def set_star_topology(self, num_nodes):
        """
        Cria uma rede com topologia de estrela.

        Args:
            num_nodes (int): Número de nós.
        """
        
        # Create a star topology network
        G = nx.star_graph(num_nodes - 1)  # num_nodes includes the center node
        G = nx.convert_node_labels_to_integers(G)
        
        # Assign properties to the nodes and channels
        self.G, self.channels = self.assign_to_net(G)
        
    
    def create_line_topology_network(self, num_nodes):
        """
        Cria uma rede com topologia de linha.
        
        Args:
            num_nodes (int): Número de nós.
        """
        # Create a line topology (path graph)
        G = nx.path_graph(num_nodes)
        G = nx.convert_node_labels_to_integers(self.G)

        # Assign random weights and initial memory to nodes
        self.G, self.channels = self.assign_to_net(G)
    
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
        Envia os qubits em uma lista pela rota escolhida. O qubit sofre interferência de acordo com a fidelidade do canal.

        Args:
            route (rota): Rota definida para o envio do qubit.
            qubits (list): Lista com qubits preparados.

        Returns:
            received_qubits (list): Lista com os qubits que chegaram no Bob.
        """
        received_qubits = []
        index_interference_qubit = []
        # Cada qubit irá percorrer a rota, de alice até bob
        for qubit in qubits:
            # O range vai até o penúltimo elemento da rota, pois o último é o nó de Bob
            for indice in range(len(route) - 1):
                # Channels (u, v) -> u é o nó de origem e v é o nó de destino. Aqui, acessamos os nós pelo seu índice na rota.
                # O canal é acessado pelo índice do nó de origem e destino na rota. O canal guarda um dicionario com as propriedades do canal. "fidelity_value" é a fidelidade do canal.
                channel_fidelity = self.channels[(route[indice], route[indice+1])]["fidelity_value"]
                # O qubit sofre interferência com uma probabilidade igual a 1 - fidelidade do canal
                if random.uniform(0, 1) > channel_fidelity:
                    qubit.interference()
                    index_interference_qubit.append(qubits.index(qubit))

            # Adiciona o qubit na lista de qubits recebidos
            received_qubits.append(qubit)

        return received_qubits, index_interference_qubit
    
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
        
        # Cada qubit irá percorrer a rota, de alice até bob
        for epr in eprs:
            # O range vai até o penúltimo elemento da rota, pois o último é o nó de Bob
            for indice in range(len(route) - 1):
                # Channels (u, v) -> u é o nó de origem e v é o nó de destino. Aqui, acessamos os nós pelo seu índice na rota
                channel_fidelity = self.channels[(route[indice], route[indice+1])] 
                # O qubit sofre interferência com uma probabilidade igual a 1 - fidelidade do canal
                if random.uniform(0, 1) > channel_fidelity:
                    qubit = epr.qubit2.interference()
            qubit = epr.qubit2
            
        # Adiciona o qubit na lista de qubits recebidos
        received_qubits.append(qubit)
                
        return received_qubits