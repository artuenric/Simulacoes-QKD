import random

def generate_qkd_request(rede, num_requests, avaliable_apps=["BB84", "E91", "B92"], diff_nodes=5, case=0):
    """
    Gera uma lista de requisições aleatórias de QKD.

    Args:
        num_requests (int): Número de requisições.
        diff_nodes (int): Número entre os nós. Defaults to 5.
        case (int): Case parameter to specify the class distribution.
                    0: Random distribution (default)
                    1: Fixed distribution (20% A, 20% B, 20% C, 20% D, 20% E)
                    2: Custom distribution
                    3: Custom distribution
                    4: Custom distribution

    Returns:
        requests (list): Lista com requisições.
    """
    requests = []

    classes = ["Class A", "Class B", "Class C", "Class D", "Class E"]

    if case == 0:
        class_distribution = [1/5] * 5
    elif case == 1:
        class_distribution = [0.2] * 5
    elif case == 2:
        class_distribution = [0.1, 0.1, 0.3, 0.25, 0.25]
    elif case == 3:
        class_distribution = [0.25, 0.25, 0.2, 0.1, 0.1]
    elif case == 4:
        class_distribution = [0.3, 0.3, 0.1, 0.15, 0.15]
    else:
        raise ValueError("Invalid case parameter")

    for i in range(num_requests):
        alice, bob = rede.random_alice_bob(diff_nodes)
        priority = random.randint(1, 5)
        app = random.choice(avaliable_apps)
        req_class = random.choices(classes, class_distribution)[0]
        requests.append((alice, bob, app, priority, req_class))

    return requests