from components import *

rede = Network()
rede.set_lattice_topology(2, 3)
controlador = Controller()
controlador.set_network(rede)

rede.draw()