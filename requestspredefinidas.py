# Este documento contém listas de requisições pré-definidas para testes.
from QKDnet import Request
import random

case = 8
n_requests = 10
apps = ["BB84", "E91", "B92"]
apps_distribution = [0.33, 0.33, 0.33]
n_nodes = 12
range_max_time = (10, 20)


def write_requests_to_file(file_name, requests_list):
    with open(file_name, 'w') as file:
        for request in requests_list:
            file.write(f"{request.num_id},{request.category},{request.app},{request.priority},{request.max_time},{request.alice},{request.bob}\n")

def read_requests_from_file(file_name):
    requests_list = []
    with open(file_name, 'r') as file:
        for line in file:
            data = line.strip().split(',')
            num_id = int(data[0])
            category = data[1]
            app = data[2]
            priority = int(data[3])
            max_time = int(data[4])
            alice = int(data[5])
            bob = int(data[6])
            request = Request(num_id, category, app, priority, max_time, alice, bob)
            requests_list.append(request)
    return requests_list

def generate_requests(case, n_requests, apps, apps_distribution, n_nodes, range_max_time):
    """
    Gera uma lista de requisições aleatórias de QKD.

    Args:
        num_requests (int): Número de requisições.
        diff_nodes (int): Número entre os nós. Defauts to 5.
        apps (list): Lista de apps disponíveis.
        
    Returns:
        requests (list): Lista com requisições.
    """
    categories = ["Category A", "Category B", "Category C", "Category D", "Category E"]
    requests = []
    
    if case == 1:
        category_distribution = [0.3, 0.3, 0.2, 0.15, 0.05]
    elif case == 2:
        category_distribution = [0.25, 0.25, 0.2, 0.15, 0.15]
    elif case == 3:
        category_distribution = [0.2] * 5
    elif case == 4:
        category_distribution = [0.15, 0.15, 0.2, 0.25, 0.25]       
    elif case == 5:
        category_distribution = [1, 0, 0, 0, 0]
    elif case == 6:
        category_distribution = [0, 1, 0, 0, 0]
    elif case == 7:
        category_distribution = [0, 0, 1, 0, 0]
    elif case == 8:
        category_distribution = [0, 0, 0, 1, 0]
    elif case == 9:
        category_distribution = [0, 0, 0, 0, 1]
    else:
        raise ValueError("Invalid case parameter")
    
    # Gera as requisições
    for i in range(n_requests):
        classe = random.choices(categories, category_distribution)[0]
        app = random.choices(apps, apps_distribution)[0]
        priority = random.randint(1, 5)
        alice, bob = random.randint(0, n_nodes-1), random.randint(0, n_nodes-1)
        r = Request(i, classe, app, priority, random.randint(range_max_time[0], range_max_time[1]), alice, bob)
        requests.append(r)
        
    return requests

# Escrever requests no arquivo
#requests_aleatorias = generate_requests(case, n_requests, apps, apps_distribution, n_nodes, range_max_time)
#write_requests_to_file("requests.txt", requests_aleatorias)

# Ler requests do arquivo e imprimir
#requests_lidas = read_requests_from_file("requests.txt")
# for request in requests_lidas:
    #print(request)
