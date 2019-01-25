import sys
from collections import defaultdict

# TD = {}
TD = {}

class GrammarParser:
    epsilon = 'EPSILON'

    def __init__(self, grammar):
        self.nt = set()
        self.productions = defaultdict(list)

        self.non_entry_nt = set()

        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.predict = defaultdict(set)

        self.symbols = set()
        self.eps = defaultdict(lambda: False)
        self.nt_order = []

        grammar = grammar.replace("→", "->")
        grammar = grammar.replace("ε", self.epsilon)
        grammar = grammar.replace("epsilon", self.epsilon)

        for production in filter(lambda x: "->" in x, grammar.split("\n")):
            nt, rhs = production.split("->")
            nt = nt.strip()
            if nt not in self.nt_order:
                self.nt_order.append(nt)

            self.nt.add(nt)
            self.symbols.add(nt)
            for s_prod in rhs.split("|"):
                cur_prod = []
                for symbol in s_prod.split():
                    symbol = symbol.strip()
                    self.non_entry_nt.add(symbol)
                    cur_prod.append(symbol)

                    if symbol == self.epsilon:
                        self.eps[nt] = True
                        self.symbols.add(symbol)
                        self.first[nt].add(self.epsilon)
                    else:
                        self.symbols.add(symbol)
                self.productions[nt].append(cur_prod)

        self.terminals = self.symbols - self.nt

        self.start_symbols = self.nt - self.non_entry_nt

        for terminal in self.terminals:
            self.first[terminal].add(terminal)

        # Calculate the first set
        changed = True
        while changed:
            changed = False
            for nt in self.nt:
                for prod in self.productions[nt]:
                    found = False
                    for symbol in prod:
                        if len(self.first[symbol] - self.first[nt]) > 0:
                            changed = True
                            self.first[nt] |= (
                                self.first[symbol] - set(self.epsilon))
                        if self.epsilon not in self.first[symbol]:
                            break
                    else:
                        if self.epsilon not in self.first[nt]:
                            self.first[nt].add(self.epsilon)
                            changed = True

        # Calculate the follow set
        # The start_symbols represent the non terminals that don't appear in
        # rhs
        if not self.start_symbols:
            self.start_symbols.add(self.nt_order[0])

        for nt in self.start_symbols:
            # EOL can follow those symbols
            self.follow[nt].add("$")

        changed = True
        while changed:
            changed = False

            for nt in self.nt:
                for prod in self.productions[nt]:

                    for symbol1, symbol2 in zip(prod, prod[1:]):
                        # The first symbol must be non-terminal
                        if symbol1 in self.nt:
                            first_sym2 = self.first[
                                symbol2] - set([self.epsilon])
                            if len(first_sym2 - self.follow[symbol1]) > 0:
                                changed = True
                                self.follow[symbol1] |= first_sym2

                    last_item = prod[-1]
                    if last_item in self.nt and len(self.follow[nt] - self.follow[last_item]) > 0:
                        changed = True
                        self.follow[last_item] |= self.follow[nt]

                    if len(prod) > 1:
                        last = prod[-1]
                        if self.epsilon in self.first[last]:
                            second_last = prod[-2]
                            if len(self.follow[nt] - self.follow[second_last]) > 0:
                                changed = True
                                self.follow[second_last] |= self.follow[nt]
        # Calculate the predict set
        for nt in self.nt:
            for prod in self.productions[nt]:
                # We use tuple of nt and the production as a tuple(immutable)
                # as the key
                key = (nt, tuple(prod))
                self.predict[key] |= self.first[prod[0]]
                is_eps = all(
                    [self.eps[x] if x in self.nt else False for x in prod])
                # print(nt," ", prod, end="")
                if is_eps or (len(prod) == 1 and prod[0] == self.epsilon):
                    self.predict[key] |= self.follow[nt]
                # No epsilon in predict set
                self.predict[key].discard(self.epsilon)

    def is_eps(self, symbol):
        if symbol not in self.nt:
            return False
        return self.eps[symbol]

    def _print_set(self, pset):
        # This is just some dirty hack to print the non terminals before terminals and in the same
        # order that they appeared. Also, don't print set of epsilon
        for symbol, f_set in filter(lambda x: x[0] != self.epsilon, sorted(pset.items(),
                                                                           key=lambda x: self.nt_order.index(x[0]) if
                                                                           x[0] in self.nt_order else len(self.nt_order) + 1)):
            print("{}\t,\t{}".format(symbol, ', '.join(
                sorted(filter(lambda x: x in self.symbols, f_set)))))

    def print_first_set(self):
        self._print_set(self.first)

    def print_follow_set(self):
        self._print_set(self.follow)

    def print_predict_set(self):
        for nt in sorted(self.nt, key=lambda x: self.nt_order.index(x)):
            for prod in self.productions[nt]:
                print("{} -> {}\t: {} ".format(nt, " ".join(prod),
                                               ",".join(self.predict[(nt, tuple(prod))])))

    def print_eps(self):
        eps_list = [symbol for symbol, iseps in self.eps.items() if iseps]
        print("Epsilon Productions : ", ",".join(eps_list))


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
        # if src_state in TD.keys():
        #     TD[src_state].append(new_edge)
        # else:
        #     TD[src_state] = [new_edge]
        if none_terminal in TD_modified.keys():
            TD[none_terminal][src_state] = {'to': dest_state, 'label': edge_label}
        else:
            TD[none_terminal] = {'start_state': src_state}

    # for key, values in TD.items():
    #     for value in values:
    #         print(value['NT'], ":", key, value["label"], value["to"])


def parse_transition_diagram(none_terminal, token, type, last_token_type):
    edges = TD[none_terminal]
    end_state = False
    currentState = TD[none_terminal]["start_state"]
    while not end_state:
        token, token_type = scanner(last_token_type)
        for edge in edges[currentState]:
            if edge["label"] not in ebnf.nt and token == edge["label"]:
                currentState = edge["to"]
                break
            if token in ebnf.first[edge["label"]] and not ebnf.epsilon in ebnf.first[edge["label"]]:
                parse_transition_diagram(edge["label"], token, token_type, token_type)
                currentState = edge["to"]
                break
            elif ebnf.epsilon in ebnf.first[edge["label"]] and token in ebnf.first[edge["label"]]:
                pass
            else:
                # error
                pass
        last_token_type = token_type
        if not error and currentState not in TD.keys():  # end node
            pass

if __name__ == "main":
    grammar_file_name = "grammar.txt"
    gf = open(grammar_file_name).read()
    ebnf = GrammarParser(gf)
    print("\nFirst set\n")
    ebnf.print_first_set()

    print("\n Follow set\n")
    ebnf.print_follow_set()

    create_transition_diagram()

    parse_transition_diagram("program", None, None, None)
    # last_token_type = None
    # currentState = 0
    # finished = False
    # error = False

    # while not finished:
    #     token, token_type = scanner(last_token_type)
    #     for edge in TD[currentState]:
    #         if token in ebnf.first[edge["label"]] and not ebnf.epsilon in ebnf.first[edge["label"]]:
    #             currentState = edge['to']
    #             break
    #         elif ebnf.epsilon in ebnf.first[edge["label"]] and token in ebnf.first[edge["label"]]:
    #             pass
    #         else:
    #             # error
    #             pass
    #
    #     if not error and currentState not in TD.keys(): # end node