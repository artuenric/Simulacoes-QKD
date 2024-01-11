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
        self.nqubits = 100
        self.neprs = 3
            
    def newDraw(self):
        pos = nx.spring_layout(self.G)
        node_colors = [self.G.nodes[n]['color'] for n in self.G.nodes]
        nx.draw(self.G, pos, node_color=node_colors, with_labels=True, font_weight='bold')
        plt.show()
        
    def draw(self):
        # Plotar a rede
        pos = nx.spring_layout(self.G)  # Calcular posições dos nós para visualização

        # Desenhar nós com seus pesos
        nx.draw_networkx_nodes(self.G, pos, node_color='#5DCCF8', node_size=500)

        # Desenhar índices dos nós
        node_indices = {node: node for node in self.G.nodes}
        nx.draw_networkx_labels(self.G, pos, labels=node_indices, font_color='white')

        # Peso das arestas
        edge_weights = [self.channels.get((u, v), {}).get("fidelity_value", 0) for u, v in self.G.edges]
        
        # Desenhar arestas com seus pesos
        edges = nx.draw_networkx_edges(self.G, pos, width=2, edge_color=edge_weights, edge_cmap=plt.cm.viridis)

        # Adicionar uma barra de cores para representar os pesos
        cbar = plt.colorbar(edges, ax=plt.gca())
        cbar.ax.set_ylabel("Fidelidade")
                
        # Exibir o gráfico inicial
        plt.title("Topology Network")
        # plt.axis("off")
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

    def set_topology(self, topology, *args):
        if topology == "Fully Connected":
            self.set_fully_connected_topology(*args)
        elif topology == "Lattice": 
            self.set_lattice_topology(*args)
        elif topology == "Ring":
            self.set_ring_topology(*args)   
        elif topology == "Star":
            self.set_star_topology(*args)
        elif topology == "Line":
            self.set_line_topology_network(*args)
        elif topology == "USA":
            self.set_USA_topology()
        elif topology == "China":
            self.set_china_topology()
        elif topology == "Vienna":
            self.set_vienna_topology()
        else:
            raise Exception("Topology not found.")    

    ### Topologias genéricas ###
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
        self.G, self.channels = self.assign_to_net(G)
    
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
        # Update network topology
        self.topology = "Ring"
        
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
        # Update network topology
        self.topology = "Star"
        
        # Create a star topology network
        G = nx.star_graph(num_nodes - 1)  # num_nodes includes the center node
        G = nx.convert_node_labels_to_integers(G)
        
        # Assign properties to the nodes and channels
        self.G, self.channels = self.assign_to_net(G)
        
        
    def set_line_topology_network(self, num_nodes):
        """
        Cria uma rede com topologia de linha.
        
        Args:
            num_nodes (int): Número de nós.
        """
        # Update network topology
        self.topology = "Line"
        
        # Create a line topology (path graph)
        G = nx.path_graph(num_nodes)
        G = nx.convert_node_labels_to_integers(self.G)

        # Assign random weights and initial memory to nodes
        self.G, self.channels = self.assign_to_net(G)
    
    ### Topologias especiais ###
    def set_USA_topology(self):
        """
        Cria uma rede com topologia dos EUA.
        """
        # Update network topology
        self.topology = "USA"
        G = nx.Graph()

        # Define the edges of the graph
        edges = [
            (1, 2), (1, 6), (2, 3), (2, 6), (3, 4), (3, 7), (4, 5), (4, 7), (4, 8), 
            (5, 8), (6, 7), (6, 9), (6, 11), (7, 8), (7, 9), (9, 10), (9, 12), (10, 13), 
            (10, 14), (11, 15), (12, 13), (12, 16), (13, 14), (13, 17), (14, 18), (15, 16), 
            (15, 19), (16, 17), (16, 21), (17, 18), (17, 22), (18, 23), (18, 24), (19, 20), 
            (20, 21), (21, 22), (22, 23), (23, 24)
        ]

        # Add the edges to the graph
        G.add_edges_from(edges)
        G = nx.convert_node_labels_to_integers(G)
        
        self.G, self.channels = self.assign_to_net(G)
        
    def set_china_topology(self):
        """
        Cria uma topologia específica da China.
        """
        G = nx.Graph()

        # Adiciona nós
        for i in range(1, 41):
            G.add_node(i, color='red' if i <= 13 else 'green')

        # Adiciona nós TR
        for i in range(1, 4):
            G.add_node(f'TR-{i}', color='blue')

        # Adiciona nós OS
        for i in range(1, 4):
            G.add_node(f'OS-{i}', color='purple')

        # Conecta nós em estrelas
        for i in range(1, 6):
            G.add_edge(f'OS-1', i)

        for i in range(6, 8):
            G.add_edge(f'OS-2', i)

        for i in range(8, 14):
            G.add_edge(f'OS-3', i)

        for i in range(14, 27):
            G.add_edge(f'TR-1', i)

        for i in range(27, 33):
            G.add_edge(f'TR-2', i)

        for i in range(33, 41):
            G.add_edge(f'TR-3', i)

        # Adiciona conexões diretas
        G.add_edge('OS-1', 'TR-2')
        G.add_edge('OS-2', 'TR-2')
        G.add_edge('OS-3', 'TR-3')
        G.add_edge('TR-3', 'TR-2')
        G.add_edge('TR-2', 'TR-1')
        G.add_edge('TR-3', 'TR-1')
        
        self.G, self.channels = self.assign_to_net(G)
        
    def set_vienna_topology(self):
        """
        Cria uma topologia específica para Viena sem a necessidade de estar dentro de uma classe.
        """
        G = nx.Graph()

        # Adiciona nós com seus respectivos tipos e cores
        nodes_info = {
            0 : {'type': 'city', 'color': 'blue'},
            1 : {'type': 'hub', 'color': 'blue'},
            2 : {'type': 'hub', 'color': 'blue'},
            3 : {'type': 'hub', 'color': 'blue'},
            4 : {'type': 'hub', 'color': 'red'},
            5 : {'type': 'hub', 'color': 'blue'},
            6 :{'type': 'hub', 'color': 'red'},
        }
        for node, info in nodes_info.items():
            G.add_node(node, color=info['color'])

        # Adiciona as arestas sólidas
        edges = [
            (0 , 1 ),
            (1 ,3 ),
            (1 ,2 ),
            (1 ,5 ),
            (2 ,3 ),
            (2 ,5 ),
            (5 ,3 ),
            (4 ,3 ),
            (5 ,6 ),
        ]
        
        # Adiciona as arestas tracejadas
        G.add_edges_from(edges)
        self.G, self.channels = self.assign_to_net(G)

        
    def random_alice_bob(self):
        """
        Escolhe um nó aleatório na rede para Alice e outro para Bob. Útil para protocolos com um remetente e um receptor.

        Returns:
            alice, bob (int) : Número correspondente ao nó do grafo.
        """
        
        sender = random.choice(list(self.G.nodes))
        receiver = random.choice(list(self.G.nodes))
        
        # Garante que nem sender, nem receiver sejam String (Nós que agem apenas como switch ou repetidores)
        while isinstance(sender, str):
            sender = random.choice(list(self.G.nodes))
        while isinstance(receiver, str):
            receiver = random.choice(list(self.G.nodes))
        
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
        index_interference_qubit = set()

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
                    index_interference_qubit.add(qubits.index(qubit))

            # Adiciona o qubit na lista de qubits recebidos
            received_qubits.append(qubit)

        return received_qubits, index_interference_qubit
    
    def send_eprs(self, route, eprs):
        """
        Envia os EPRs em uma lista pela rota escolhida. O qubit sofre interferência de acordo com a fidelidade do canal.

        Args:
            route (rota): Rota definida para o envio do qubit.
            eprs (list): Lista com pares emaranhados preparados.

        Returns:
            received_qubits (list): Lista com os qubits que chegaram no Bob.
        """
        received_qubits = []
        index_interference_qubit = set()
        
        # Cada qubit irá percorrer a rota, de alice até bob
        for epr in eprs:
            # O range vai até o penúltimo elemento da rota, pois o último é o nó de Bob
            for indice in range(len(route) - 1):
                # Channels (u, v) -> u é o nó de origem e v é o nó de destino. Aqui, acessamos os nós pelo seu índice na rota
                channel_fidelity = self.channels[(route[indice], route[indice+1])]["fidelity_value"]
                # O qubit sofre interferência com uma probabilidade igual a 1 - fidelidade do canal
                if random.uniform(0, 1) > channel_fidelity:
                    qubit = epr.qubit2.interference()
                    index_interference_qubit.add(eprs.index(epr))
                    
            qubit = epr.qubit2
            # Adiciona o qubit na lista de qubits recebidos
            received_qubits.append(qubit)
                          
        return received_qubits, index_interference_qubit