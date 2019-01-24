import sys
from collections import defaultdict

TD = {}


def create_transition_diagram():
    file_name = "edges.txt"
    file = open(file_name, "r")
    edges = file.read().split('\n')
    file.close()
    for edge in edges:
        none_terminal = edge.split(":")[0].replace(" ", "")
        edge = edge.replace(none_terminal + " :", "")
        edge_tmp = edge.replace(" ", "").split("--")
        src_state = int(edge_tmp[0])
        dest_state = int(edge_tmp[2])
        edge_label = edge_tmp[1]
        new_edge = {'NT': none_terminal, 'to': dest_state, 'label': edge_label}
        if src_state in TD.keys():
            TD[src_state].append(new_edge)
        else:
            TD[src_state] = [new_edge]

    # for key, values in TD.items():
    #     for value in values:
    #         print(value['NT'], ":", key, value["label"], value["to"])


if __name__ == "main":
    create_transition_diagram()
    last_token_type = None
    # type, new_token = scanner(last_token_type)
