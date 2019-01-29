import re
from collections import defaultdict
from collections import defaultdict

if_tok = "if"
while_tok = "while"
return_tok = "return"
switch_tok = "switch"
case_tok = "case"
default_tok = "default"
break_tok = "break"
continue_tok = "continue"
int_tok = "int"
void_tok = "void"
keyword = "keyword"
special = "special_character"
scope = 0
dec_flag = 0
id_tok = "ID"
num_tok = "NUM"
idregex = re.compile("^[a-zA-Z][a-zA-Z0-9]*")
numregex = re.compile("[+-]?[0-9]+")


symbol_table = []


def find_st(id_str):
    for i, entry in enumerate(symbol_table):
        for s in reversed(range(scope + 1)):
            if id_str in entry.keys() and entry[id_str]["scope"] == s:
                return i
# TODO error handling here


def is_defined(id_str):
    for i, entry in enumerate(symbol_table):
        if id_str in entry.keys() and entry[id_str]["scope"] == scope:
            return True
    return False


def del_scope():
    global symbol_table
    for i, entry in enumerate(symbol_table):
        for key in entry.keys():
            if entry[key]["scope"] == scope:
                del symbol_table[i]


def scanner(last_token_type):
    global source_text
    source_text = source_text.lstrip()
    if source_text.find(if_tok) == 0:
        source_text = source_text.replace(if_tok, "", 1)
        return if_tok, keyword
    elif source_text.find(while_tok) == 0:
        source_text = source_text.replace(while_tok, "", 1)
        return while_tok, keyword
    elif source_text.find(return_tok) == 0:
        source_text = source_text.replace(return_tok, "", 1)
        return return_tok, keyword
    elif source_text.find(switch_tok) == 0:
        source_text = source_text.replace(switch_tok, "", 1)
        return switch_tok, keyword
    elif source_text.find(case_tok) == 0:
        source_text = source_text.replace(case_tok, "", 1)
        return case_tok, keyword
    elif source_text.find(default_tok) == 0:
        source_text = source_text.replace(default_tok, "", 1)
        return default_tok, keyword
    elif source_text.find(break_tok) == 0:
        source_text = source_text.replace(break_tok, "", 1)
        return break_tok, keyword
    elif source_text.find(continue_tok) == 0:
        source_text = source_text.replace(continue_tok, "", 1)
        return continue_tok, keyword
    elif source_text.find(int_tok) == 0:
        source_text = source_text.replace(int_tok, "", 1)
        return int_tok, keyword
    elif source_text.find("(") == 0:
        source_text = source_text.replace("(", "", 1)
        return "(", special
    elif source_text.find(")") == 0:
        source_text = source_text.replace(")", "", 1)
        return ")", special
    elif source_text.find("[") == 0:
        source_text = source_text.replace("[", "", 1)
        return "[", special
    elif source_text.find("]") == 0:
        source_text = source_text.replace("]", "", 1)
        return "]", special
    elif source_text.find("{") == 0:
        global scope
        source_text = source_text.replace("{", "", 1)
        return "{", special
    elif source_text.find("}") == 0:
        global scope
        del_scope()
        scope -= 1
        source_text = source_text.replace("}", "", 1)
        return "}", special
    elif source_text.find(";") == 0:
        source_text = source_text.replace(";", "", 1)
        return ";", special
    elif source_text.find("<") == 0:
        source_text = source_text.replace("<", "", 1)
        return "<", special
    elif source_text.find("==") == 0:
        source_text = source_text.replace("==", "", 1)
        return "=", special
    elif source_text.find("*") == 0:
        source_text = source_text.replace("*", "", 1)
        return "*", special
    elif source_text.find(",") == 0:
        source_text = source_text.replace(",", "", 1)
        return ",", special
    elif source_text.find("+"):
        if last_token_type == id_tok:
            source_text = source_text.replace("+", "", 1)
            return "+", special
    elif source_text.find("-"):
        if last_token_type == id_tok:
            source_text = source_text.replace("-", "", 1)
            return "-", special
    else:
        id_match = idregex.match(source_text)
        num_match = numregex.match(source_text)

        if id_match.start() == 0:
            id_str = id_match.group()
            if id_str == "main":
                PB[0] = convertToStr("JP", PB_counter)
            if dec_flag and not is_defined(id_str):
                entry = {id_str: {"scope": scope, "type": id_tok}}
                symbol_table.append(entry)
                source_text = source_text.replace(id_str, "", 1)
                return id_tok, len(symbol_table)-1
            else:
                position = find_st(id_str)
                source_text = source_text.replace(id_str, "", 1)
                return id_tok, position

        elif num_match.start() == 0:
            num_str = num_match.group()
            source_text = source_text.replace(num_str, "", 1)
            return num_tok, int(num_str)


ss = []
PB = []
PB_counter = 0
whiles = []
address = 10000


def gettemp():
    global address
    address += 32
    return address - 32


def top(stack):
    return len(stack) - 1


def convertToStr(func, par1='', par2='', par3=''):
    return '(' + func + ', ' + str(par1) + ', ' + str(par2) + ', ' + str(par3) + ')'


def code_generation(action, input):
    global PB_counter
    global address
    global scope
    if action == "#PUSH_SS":
        ss.append(input)
        return
    elif action == "#PUSH_ADDR":
        ss.append(symbol_table[ss[top(ss)]].values()[0]["addr"])
    elif action == "#ASSIGN":
        PB.append(convertToStr("ASSIGN", ss[top(ss)], ss[top(ss)]))
        PB_counter += 1
        ss.pop()
        ss.pop()
        return
    elif action == "#ADDSUB":
        t = gettemp()
        if ss[top(ss) - 1] == "+":
            PB.append(convertToStr("ADD", ss[top(ss)], ss[top(ss) - 1], t))
        elif ss[top(ss) - 1] == "-":
            PB.append(convertToStr("SUB", ss[top(ss)], ss[top(ss) - 1], t))
        PB_counter += 1
        for i in range(3):
            ss.pop()
        ss.append(t)
        return
    elif action == "MULT":
        t = gettemp()
        # symbol_table[ss[top(ss)]]
        PB.append(convertToStr("MULT", ss[top(ss)], ss[top(ss) - 1], t))
        # PB[PB_counter] = (MULT, ss[top(ss)], ss[top(ss) - 1], t)
        PB_counter += 1
        ss.pop()
        ss.pop()
        ss.append(t)
        return
    elif action == "#PUSH_VOID":
        ss.append("void")
    elif action == "#FUN_ADDR":
        fun_id = ss.pop()
        fun_dict = symbol_table[fun_id].values()[0]
        fun_dict['addr'] = PB_counter
        fun_dict['params'] = []
        fun_dict['params_count'] = 0
        fun_dict['ret_addr'] = address
        if ss[top(ss)] == "void":
            fun_dict['is_retrun'] = 0
            ss.pop()
        else:
            fun_dict['is_return'] = 1
        address+= 32
        fun_dict['ret_val'] = address
        address += 32
        PB_counter += 1
        ss.append(fun_id)
        return
    elif action == "#VAR_ADDR":
        var_dict = symbol_table[ss.pop()].values()[0]
        var_dict['addr'] = address
        address += 32
        return
    elif action == "#ARR_ADDR":
        arr_dict = symbol_table[ss.pop()].values()[0]
        arr_dict['addr'] = address
        address += 32
        PB.append('(ASSIGN, #' + str(address) + ',' + str(arr_dict['addr']) + ', )')
        PB_counter += 1
        # for i in range(input):
        return
    elif action == "#INC_SCOPE":
        scope += 1
        return
    elif action == "#PAR_ADDR":
        param_dict = symbol_table[input].values()[0]
        param_dict['addr'] = address
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        fun_dict['params_count'] += 1
        fun_dict['params'].append(address)
        address += 32
        return
    elif action == "#DEC_SCOPE":
        scope -= 1
        return
    elif action == "#ASSIGN_RET":
        fun_dict = symbol_table[ss[top(ss) - 1]].values()[0]
        PB.append('(ASSIGN, #' + str(ss.pop()) + ',' + str(fun_dict['ret_val']) + ', )')
        PB_counter += 1
        return
    elif action == "#JMP_CALLER":
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        PB.append('(JP, ' + '@' + str(fun_dict['ret_addr']) + ', , )')
        PB_counter += 1
        return
    elif action == "#POP_SS":
        ss.pop()
        return
    elif action == "#SAVE":
        ss.append(PB_counter)
        PB_counter += 1
        return
    elif action == "#LABEL":
        ss.append(PB_counter)
        return
    elif action == "#SAVE_CONTINUE":
        whiles.append(([PB_counter], []))
        return
    elif action == "#SAVE_SWITCH":
        whiles.append(([], []))
        return
    elif action == "#END_SWITCH":
        last_switch = whiles[-1][1]
        for i in last_switch:
            PB[i] = convertToStr("JP", PB_counter)
        whiles.pop()
    elif action == "#WHILE":
        PB[ss[top(ss)]] = convertToStr("JPF", ss[top(ss) - 1], PB_counter + 1)
        PB.append(convertToStr("JP", ss[top(ss) - 2]))
        PB_counter += 1
        last_loop_breaks = whiles[-1][1]
        for i in last_loop_breaks:
            PB[i] = convertToStr("JP", PB_counter)
        whiles.pop()
        for i in range(3):
            ss.pop()
        return
    elif action == "#JMP_BEGIN":
        # PB[PB_counter] = (JP, ss.get(ss.top))
        PB.append(convertToStr("JP", whiles[-1][0][-1]))
        PB_counter += 1
        return
    elif action == "#JMP_END":
        whiles[-1][1].append(PB_counter)
        PB_counter += 1
        return
    elif action == "#JPF_SAVE":
        PB[ss[top(ss)]] = convertToStr("JPF", ss[top(ss)-1], PB_counter+1)
        ss.pop()
        ss.pop()
        ss.append(PB_counter)
        PB_counter += 1
        return
    elif action == "#JP":
        PB[ss[top(ss)]] = convertToStr("JP", PB_counter)
        ss.pop()
        return
    elif action == "#JPT_SAVE":
        pass
    elif action == "#COMPARE_CASE":
        t = gettemp()
        PB.append(convertToStr("EQ", int(input), ss[top(ss) - 1], t))
        PB_counter += 1
        ss.append(t)
        return
    elif action == "#JPF":
        PB[ss[top(ss)]] = convertToStr("JPF", ss[top(ss) - 1], PB_counter)
        ss.pop()
        ss.pop()
        return
    elif action == "#PUSH_INPUT":
        ss.append(input)
        return
    elif action == "#RELOP":
        t = gettemp()
        if ss[top(ss) - 1] == "<":
            PB.append(convertToStr("LT", ss[top(ss) - 2], ss[top(ss)], t))
        else:
            PB.append(convertToStr("EQ", ss[top(ss) - 2], ss[top(ss)], t))
        PB_counter += 1
        for i in range(3):
            ss.pop()
        ss.append(t)
        return
    elif action == "#RET_ADDR":
        fun_dict = symbol_table[ss.pop()].values()[0]
        fun_dict['ret_addr'] = PB_counter
        if fun_dict['is_return']:
            ss.append(fun_dict['ret_val'])
        return
    elif action == "#JP_CALL":
        ss.pop()
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        PB.append(convertToStr("JP", fun_dict['addr']))
        PB_counter += 1
        return
    elif action == "#PARAM_CNT":
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        ss.append(fun_dict["params_count"])
        return
    elif action == "#ASS_ARG":
        fun_dict = symbol_table[ss[top(ss) - 2]].values()[0]
        param_num = fun_dict["params_count"] - ss[top(ss) -1]
        PB.append(convertToStr("ASSIGN", ss.pop(), fun_dict["params"][param_num]))
        PB_counter += 1
        ss.append(ss.pop() - 1)
        return
    elif action == "#ARR_READ":
        arr_dict = symbol_table[ss[top(ss) - 1]].values()[0]
        t1 = gettemp()
        PB.append(convertToStr("ADD", arr_dict["addr"], ss.pop(), t1))
        PB_counter += 1
        ss.pop()
        ss.append('@' + str(t1))
        return
    elif action == "#PUSH_NUM":
        t1 = gettemp()
        PB.append(convertToStr("ASSIGN", '#' + str(input), t1))
        PB_counter += 1
        ss.append(t1)
        return


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


def program(type, ebnf):
    state = 0
    while True:
        token, type = scanner(type)
        if state == 0 and token in ebnf.first["dl"]:
            status = dl(type, ebnf)
            state = 1
            continue
        elif state == 1 and token == "EOF":
            # END STATE
            state = 2
            return
        else:
            # ERROR
            pass


def dl(type, ebnf):
    state = 3
    while True:
        token, type = scanner(type)
        if state == 3 and token in ebnf.first["dec"]:
            status = dec(type, ebnf)
            state = 4
            continue
        elif state == 4 and token in ebnf.first["dl"]:
            status = dl(type, ebnf)
            state = 5
            return
            # END STATE
        elif state == 3 and token in ebnf.follow["dl"]:
            #EPSILON EDGE
            # END STATE
            state = 5
            return
        else:
            # ERROR
            pass


def dec(type, ebnf):
    state = 6
    while True:
        token, type = scanner(type)
        if state == 6 and token in ebnf.first["ts"]:
            status = ts(type, ebnf)
            state = 7
            continue
        elif state == 7 and token == "ID":
            code_generation("#PUSH_SS", type)
            state = 8
            continue
        elif state == 8 and token in ebnf.first["dec'"]:
            # END STATE
            status = dec_(type, ebnf)
            state = 9
            return
        else:
            # ERROR
            pass


def dec_(type, ebnf):
    state = 10
    while True:
        token, type = scanner(type)
        if state == 10 and token in ebnf.first["vdec"]:
            # END STATE
            status = vdec(type, token)
            state = 11
            return
        elif state == 10 and token in ebnf.first["fdec"]:
            #END STATE
            code_generation("#FUN_ADDR", type)
            status = fdec(type, token)
            state = 11
            return
        else:
            # ERROR
            pass


def vdec(type, ebnf):
    state = 12
    while True:
        token, type = scanner(type)
        if (state == 12 or state == 16) and token == ";":
            # END STATE
            code_generation("#VAR_ADDR", type)
            state = 13
            return
        elif state == 12 and token == "[":
            state = 14
            continue
        elif state == 14 and token == "NUM":
            code_generation("#ARR_ADDR", type)
            state = 15
            continue
        elif state == 15 and token == "]":
            state = 16
            continue
        else:
            # ERROR
            pass


def ts(type, ebnf):
    state = 17
    while True:
        token, type = scanner(type)
        if state == 17 and (token == "int" or token == "void"):
            # END STATE
            state = 18
            return
        else:
            # ERROR
            pass


def fdec(type, ebnf):
    state = 19
    while True:
        token, type = scanner(type)
        if state == 19 and token == "(":
            code_generation("#INC_SCOPE", type)
            state = 20
            continue
        elif state == 20 and token in ebnf.first["params"]:
            status = params(type, ebnf)
            state = 21
            continue
        elif state == 21 and token == ")":
            state = 22
            continue
        elif state == 22 and token in ebnf.first["cs"]:
            # END STATE
            code_generation("#DEC_SCOPE", type)
            status = cs(type, token)
            code_generation("#JMP_CALLER", type)
            code_generation("#POP_SS", type)
            state = 23
            return
        else:
            # ERROR
            pass


def params(type, ebnf):
    state = 24
    while True:
        token, type = scanner(type)
        if state == 24 and token == "void":
            state = 26
            return
        elif state == 24 and token == "int":
            state = 27
            continue
        elif state == 27 and token == "ID":
            code_generation("#PAR_ADDR", type)
            state = 28
            continue
        elif state == 28 and token in ebnf.first["P'"]:
            status = P_(type, ebnf)
            state = 29
            continue
        elif state == 29 and token in ebnf.first["pl"]:
            # END STATE
            status = pl(type, token)
            state = 26
            return
        else: # ERROR
            pass


def pl(type, ebnf):
    state = 34
    while True:
        token, type = scanner(type)
        if state == 34 and token == ";":
            state = 35
            continue
        elif state == 35 and token in ebnf.first["P"]:
            status = P(type, ebnf)
            state = 36
            continue
        elif state == 36 and token in ebnf.first["pl"]:
            # END STATE
            status = pl(type, ebnf)
            state = 37
            return
        elif state == 34 and token in ebnf.follow["pl"]:
            # END STATE
            # EPSILON EDGE
            state = 37
            return
        else: # ERROR
            pass


def P(type, ebnf):
    state = 38
    while True:
        token, type = scanner(type)
        if state == 38 and token in ebnf.first["ts"]:
            status = ts(type, ebnf)
            state = 39
            continue
        elif state == 39 and token == "ID":
            code_generation("#PAR_ADDR", type)
            state = 40
            continue
        elif state == 40 and token in ebnf.first["P'"]:
            # END STATE
            status = P_(type, ebnf)
            state = 41
            return


def P_(type, ebnf):
    state = 42
    while True:
        token, type = scanner(type)
        if state == 42 and token == "[":
            state = 44
            continue
        elif state == 44 and token == "]":
            # END STATE
            state = 43
            return
        elif state == 42 and token in ebnf.follow["P'"]:
            # END STATE
            # EPSILON EDGE
            state = 43
            return
        else: # ERROR
            pass


def cs(type, ebnf):
    state = 45
    while True:
        token, type = scanner(type)
        if state == 45 and token == "{":
            state = 46
            continue
        elif state == 46 and token in ebnf.first["dl"]:
            status = dl(type, ebnf)
            state = 47
            continue
        elif state == 47 and token in ebnf.first["sl"]:
            status = sl(type, ebnf)
            state = 48
            continue
        elif state == 48 and token == "}":
            # END STATE
            state = 49
            return
        else: # ERROR
            pass


def sl(type, ebnf):
    state = 50
    while True:
        token, type = scanner(type)
        if state == 50 and token in ebnf.first["S"]:
            status = S(type, ebnf)
            state = 51
            continue
        elif state == 51 and token in ebnf.first["sl"]:
            # END STATE
            status = sl(type, ebnf)
            state = 52
            return
        elif state == 50 and token in ebnf.follow["sl"]:
            # END STATE
            # EPSILON EDGE
            state = 52
            return
        else: # ERROR
            pass


def S(type, ebnf):
    state = 53
    while True:
        token, type = scanner(type)
        if state == 53 and token in ebnf.first["es"]:
            # END STATE
            status = es(type, ebnf)
            state = 54
            return
        elif state == 53 and token in ebnf.first["cs"]:
            # END STATE
            status = cs(type, ebnf)
            state = 54
            return
        elif state == 53 and token in ebnf.first["ss"]:
            # END STATE
            status = ss(type, ebnf)
            state = 54
            return
        elif state == 53 and token in ebnf.first["is"]:
            # END STATE
            status = _is(type, ebnf)
            state = 54
            return
        elif state == 53 and token in ebnf.first["rs"]:
            # END STATE
            status = rs(type, ebnf)
            state = 54
            return
        elif state == 53 and token in ebnf.first["sws"]:
            # END STATE
            status = sws(type, ebnf)
            state = 54
            return
        else: #ERROR
            pass


def es(type, ebnf):
    state = 55
    while True:
        token, type = scanner(type)
        if state == 55 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            state = 56
            continue
        elif state == 56 and token == ";":
            # END STATE
            state = 57
            return
        elif state == 55 and token == "continue":
            state = 58
            continue
        elif state == 58 and token == ";":
            # END STATE
            code_generation("#JMP_BEGIN", type)
            state = 57
            return
        elif state == 55 and token == "break":
            state = 59
            continue
        elif state == 59 and token == ";":
            # END STATE
            code_generation("#JMP_END", type)
            state = 57
            return
        elif state == 55 and token == ";":
            # END STATE
            state = 57
            return
        else: # ERROR
            pass


def ss(type, ebnf):
    state = 60
    while True:
        token, type = scanner(type)
        if state == 60 and token == "if":
            state = 61
            continue
        elif state == 61 and token == "(":
            state = 62
            continue
        elif state == 62 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            state = 63
            continue
        elif state == 63 and token == ")":
            state = 64
            continue
        elif state == 64 and token in ebnf.first["S"]:
            code_generation("#SAVE", type)
            status = S(type, ebnf)
            state = 65
            continue
        elif state == 65 and token == "else":
            state = 66
            continue
        elif state == 66 and token in ebnf.first["S"]:
            # END STATE
            code_generation("#JPF_SAVE", type)
            status = S(type, ebnf)
            code_generation("#JP", type)
            state = 67
            return
        else: # ERROR
            pass

def _is(type, ebnf):
    state = 68
    while True:
        token, type = scanner(type)
        if state == 68 and token == "while":
            state = 69
            continue
        elif state == 69 and token == "(":
            state = 70
            continue
        elif state == 70 and token in ebnf.first["E"]:
            code_generation("LABEL", type)
            code_generation("SAVE_CONTINUE", type)
            status = E(type, ebnf)
            state = 71
            continue
        elif state == 71 and token == ")":
            state = 72
            continue
        elif state == 72 and token in ebnf.first["S"]:
            # END STATE
            code_generation("#SAVE", type)
            status = S(type, ebnf)
            code_generation("#WHILE", type)
            state = 73
            return
        else: # ERROR
            pass


def rs(type, ebnf):
    state = 74
    while True:
        token, type = scanner(type)
        if state == 74 and token == "return":
            state = 75
            continue
        elif state == 75 and token in ebnf.first["rs'"]:
            status = rs_(type, ebnf)
            state = 76
            return
        else:
            pass


def rs_(type, ebnf):
    state = 77
    while True:
        token, type = scanner(type)
        if state == 77 and token == ";":
            # END STATE
            code_generation("#JMP_CALLER", type)
            state = 78
            return
        elif state == 77 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            code_generation("#ASSIGN_RET", type)
            code_generation("JMP_CALLER", type)
            state = 79
            continue
        elif state == 79 and token == ";":
            state = 78
            return
        else:
            pass

def sws(type, ebnf):
    state = 80
    while True:
        token, type = scanner(type)
        if state == 80 and token == "switch":
            code_generation("#SAVE_SWITCH", type)
            state = 81
            continue
        elif state == 81 and token == "(":
            state = 82
            continue
        elif state == 82 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            state = 83
            continue
        elif state == 83 and token == ")":
            state = 84
            continue
        elif state == 84 and token == "{":
            state = 85
            continue
        elif state == 85 and token in ebnf.first["cas"]:
            status = cas(type, ebnf)
            state = 86
            continue
        elif state == 86 and token in ebnf.first["ds"]:
            status = ds(type, ebnf)
            state = 87
            continue
        elif state == 87 and token == "}":
            state = 88
            code_generation("#END_SWITCH", type)
            return
        else:
            pass


def cas(type, ebnf):
    state = 89
    while True:
        token, type = scanner(type)
        if state == 89 and token in ebnf.first["ca"]:
            status = ca(type, ebnf)
            state = 90
            continue
        elif state == 90 and token in ebnf.first["cas"]:
            code_generation("#JPF", type)
            status = cas(type, ebnf)
            state = 91
            return
        elif state == 89 and token in ebnf.follow["cas"]:
            # EPSILON
            state = 91
            return
        else:
            pass


def ca(type, ebnf):
    state = 92
    while True:
        token, type = scanner(type)
        if state == 92 and token == "case":
            code_generation("#LABEL", type)
            state = 93
            continue
        elif state == 93 and token == "NUM":
            code_generation("#COMPARE_CASE", type)
            state = 94
            continue
        elif state == 94 and token == ":":
            state = 95
            continue
        elif state == 95 and token in ebnf["sl"]:
            code_generation("SAVE", type)
            status = sl(type, ebnf)
            state = 96
            return
        else:
            pass


def ds(type, ebnf):
    state = 97
    while True:
        token, type = scanner(type)
        if state == 97 and token == "default":
            state = 98
            continue
        elif state == 98 and token == ":":
            state = 99
            continue
        elif state == 99 and token in ebnf.first["sl"]:
            status = sl(type, ebnf)
            state = 100
            return
        elif state == 97 and token in ebnf.follow["ds"]:
            # EPSILON
            state = 100
            return
        else:
            pass


def E(type, ebnf):
    state = 101
    while True:
        token, type = scanner(type)
        if state == 101 and token == "ID":
            code_generation("#PUSH_SS", type)
            state = 102
            continue
        elif state == 102 and token in ebnf.first["E'"]:
            status = E_(type, ebnf)
            state = 103
            return
        elif state == 101 and token == "(":
            state = 104
            continue
        elif state == 104 and token in ebnf.first["E"]:
            state = 105
            continue
        elif state == 105 and token == ")":
            state = 106
            continue
        elif state == 106 and token in ebnf.first["T'"]:
            status = T_(type, ebnf)
            state = 107
            continue
        elif state == 107 and token in ebnf.first["ae'"]:
            status = ae_(type, ebnf)
            state = 108
            continue
        elif state == 108 and token in ebnf.first["se"]:
            status = se(type, ebnf)
            state = 103
            return
        elif state == 101 and token == "NUM":
            code_generation("#PUSH_NUM", type)
            state = 109
            continue
        elif state == 109 and token in ebnf.first["T'"]:
            state = T_(type, ebnf)
            state = 110
            continue
        elif state == 110 and token in ebnf.first["ae'"]:
            status = ae_(type, ebnf)
            state = 111
            continue
        elif state == 111 and token in ebnf.first["se"]:
            status = se(type, ebnf)
            state = 103
            return
        else:
            pass


def E_(type, ebnf):
    state = 112
    while True:
        token, type = scanner(type)
        if state == 112 and token in ebnf.first["var"]:
            status = var(type, ebnf)
            state = 113
            continue
        elif state == 113 and token in ebnf.first["E''"]:
            status = E__(type, ebnf)
            state = 114
            return
        elif state == 112 and token == "call":
            state = 115
            continue
        elif state == 115 and token in ebnf.first["T'"]:
            status = T_(type, ebnf)
            state = 116
            continue
        elif state == 116 and token in ebnf.first["ae'"]:
            status = ae_(type, ebnf)
            state = 117
            continue
        elif state == 117 and token in ebnf.first["se"]:
            status = se(type, ebnf)
            state = 114
            return
        else:
            pass


def E__(type, ebnf):
    state = 118
    while True:
        token, type = scanner(type)
        if state == 118 and token in ebnf.first["T'"]:
            status = T_(type, ebnf)
            state = 119
            continue
        elif state == 119 and token in ebnf.first["ae_"]:
            status = ae_(type, ebnf)
            state = 120
            continue
        elif state == 120 and token in ebnf.first["se"]:
            status = se(type, ebnf)
            state = 121
            return
        elif state == 118 and token == "=":
            state = 122
            continue
        elif state == 122 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            code_generation("#ASSIGN", type)
            state = 121
            return
        else:
            pass


def var(type, ebnf):
    state = 123
    while True:
        token, type = scanner(type)
        if state == 123 and token in ebnf.follow["var"]:
            # EPSILON
            code_generation("#PUSH_ADDR", type)
            state = 124
            return
        elif state == 123 and token == "[":
            state = 125
            continue
        elif state == 125 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            code_generation("#ARR_READ", type)
            state = 126
            continue
        elif state == 126 and token == "]":
            state = 124
            return
        else:
            pass


def se(type, ebnf):
    state = 127
    while True:
        token, type = scanner(type)
        if state == 127 and token == "relop":
            status = relop(type, ebnf)
            state = 128
            continue
        elif state == 128 and token in ebnf.first["ae"]:
            status = ae(type, ebnf)
            code_generation("#RELOP", type)
            state = 129
            return
        elif state == 127 and token in ebnf.follow["se"]:
            #EPSILON
            state = 129
            return
        else:
            pass


def relop(type, ebnf):
    state = 130
    while True:
        token, type = scanner(type)
        if state == 130 and token == "<":
            code_generation("#PUSH_INPUT", type)
            state = 131
            return
        elif state == 130 and token == "==":
            code_generation("#PUSH_INPUT", type)
            state = 131
            return
        else:
            pass


def ae(type, ebnf):
    state = 132
    while True:
        token, type = scanner(type)
        if state == 132 and token in ebnf.first["T"]:
            status = T(type, ebnf)
            state = 133
            continue
        elif state == 133 and token in ebnf.first["ae'"]:
            status = ae_(type, ebnf)
            state = 134
            return
        else:
            pass


def ae_(type, ebnf):
    state = 135
    while True:
        token, type = scanner(type)
        if state == 135 and token in ebnf.first["addop"]:
            status = addop(type, ebnf)
            state = 136
            continue
        elif state == 136 and token in ebnf.first["T"]:
            status = T(type, ebnf)
            state = 137
            continue
        elif state == 137 and token in ebnf.first["ae'"]:
            code_generation("#ADDSUB", type)
            status = ae_(type, ebnf)
            state = 138
            return
        elif state == 135 and token in ebnf.follow["ae'"]:
            state = 138
            return
        else:
            pass


def addop(type, ebnf):
    state = 139
    while True:
        token, type = scanner(type)
        if state == 139 and token == "+":
            code_generation("PUSH_INPUT", type)
            state = 140
            return
        elif state == 139 and token == "-":
            code_generation("PUSH_INPUT", type)
            state = 140
            return
        else:
            pass


def T(type, ebnf):
    state = 141
    while True:
        token, type = scanner(type)
        if state == 141 and token in ebnf.first["F"]:
            status = F(type, ebnf)
            state = 142
            continue
        elif state == 142 and token in ebnf.first["T'"]:
            status = T_(type, ebnf)
            state = 143
            return
        else:
            pass


def T_(type, ebnf):
    state = 144
    while True:
        token, type = scanner(type)
        if state == 144 and token == "*":
            state = 145
            continue
        elif state == 145 and token in ebnf.first["F"]:
            status = F(type, ebnf)
            state = 146
            continue
        elif state == 146 and token in ebnf.first["T'"]:
            code_generation("#MULT", type)
            status = T_(type, ebnf)
            state = 147
            return
        elif state == 144 and token in ebnf.follow["T'"]:
            state = 147
            return
        else:
            pass


def F(type, ebnf):
    state = 148
    while True:
        token, type = scanner(type)
        if state == 148 and token == "(":
            state = 149
            continue
        elif state == 149 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            state = 150
            continue
        elif state == 150 and token == ")":
            state = 151
            return
        elif state == 148 and token == "ID":
            code_generation("#PUSH_SS", type)
            state = 152
            continue
        elif state == 152 and token in ebnf.first["F'"]:
            status = F_(type, ebnf)
            state = 151
            return
        elif state == 148 and token == "NUM":
            state = 151
            return
        else:
            pass


def F_(type, ebnf):
    state = 153
    while True:
        token, type = scanner(type)
        if state == 153 and token in ebnf.first["var"]:
            status = var(type, ebnf)
            state = 154
            return
        elif state == 153 and token in ebnf.first["call"]:
            status = call(type, ebnf)
            state = 154
            return
        else:
            pass


def call(type, ebnf):
    state = 155
    while True:
        token, type = scanner(type)
        if state == 155 and token == "(":
            state = 156
            continue
        elif state == 156 and token in ebnf.first["args"]:
            code_generation("#PARAM_COUNT", type)
            status = ae_(type, ebnf)
            state = 157
            continue
        elif state == 157 and token == ")":
            code_generation("#JP_CALL", type)
            code_generation("#RET_ADDR", type)
            state = 158
            return
        else:
            pass


def args(type, ebnf):
    state = 159
    while True:
        token, type = scanner(type)
        if state == 159 and token in ebnf.first["argl"]:
            status = argl(type, ebnf)
            state = 160
            return
        elif state == 159 and token in ebnf.follow["args"]:
            # EPSILON
            state = 160
            return
        else:
            pass


def argl(type, ebnf):
    state = 161
    while True:
        token, type = scanner(type)
        if state == 161 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            state = 162
            continue
        elif state == 162 and token in ebnf.first["argl'"]:
            code_generation("#ASS_ARG", type)
            status = argl_(type, ebnf)
            state = 163
            return
        else:
            pass


def argl_(type, ebnf):
    state = 164
    while True:
        token, type = scanner(type)
        if state == 164 and token == ",":
            state = 165
            continue
        if state == 165 and token in ebnf.first["E"]:
            status = E(type, ebnf)
            state = 166
            continue
        elif state == 166 and token in ebnf.first["argl'"]:
            code_generation("#ASS_ARG", type)
            status = argl_(type, ebnf)
            state = 167
            return
        elif state == 164 and token in ebnf.follow["argl'"]:
            state = 167
            return
        else:
            pass


# def create_transition_diagram():
#     file_name = "edges.txt"
#     file = open(file_name, "r")
#     edges = file.read().split('\n')
#     file.close()
#     for edge in edges:
#         none_terminal = edge.split(":")[0].replace(" ", "")
#         edge = edge.replace(none_terminal + " :", "")
#         edge_tmp = edge.replace(" ", "").split("--")
#         src_state = int(edge_tmp[0])
#         dest_state = int(edge_tmp[2])
#         edge_label = edge_tmp[1]
#         new_edge = {'NT': none_terminal, 'to': dest_state, 'label': edge_label}
#         # if src_state in TD.keys():
#         #     TD[src_state].append(new_edge)
#         # else:
#         #     TD[src_state] = [new_edge]
#         if none_terminal in TD.keys():
#             TD[none_terminal][src_state] = {'to': dest_state, 'label': edge_label}
#         else:
#             TD[none_terminal] = {'start_state': src_state}

    # for key, values in TD.items():
    #     for value in values:
    #         print(value['NT'], ":", key, value["label"], value["to"])


# def parse_transition_diagram(none_terminal, token, type, last_token_type):
#     edges = TD[none_terminal]
#     end_state = False
#     currentState = TD[none_terminal]["start_state"]
#     error = False
#     while not end_state:
#         token, token_type = scanner(last_token_type)
#         for edge in edges[currentState]:
#             if edge["label"] not in ebnf.nt and token == edge["label"]:
#                 currentState = edge["to"]
#                 break
#             if token in ebnf.first[edge["label"]] and not ebnf.epsilon in ebnf.first[edge["label"]]:
#                 parse_transition_diagram(edge["label"], token, token_type, token_type)
#                 currentState = edge["to"]
#                 break
#             elif ebnf.epsilon in ebnf.first[edge["label"]] and token in ebnf.first[edge["label"]]:
#                 pass
#             else:
#                 # error
#                 pass
#         last_token_type = token_type
#         if not error and currentState not in TD.keys():  # end node
#             pass


if __name__ == "main":
    with open("code.c", "r") as file:
        source_text = file.read()
        source_text += "$"
    grammar_file_name = "grammar.txt"
    gf = open(grammar_file_name).read()
    ebnf = GrammarParser(gf)
    # create_transition_diagram()
    # parse_transition_diagram("program", None, None, None)
    PB.append("")
    PB_counter += 1
    output_dec = {'output': {'addr' : 1, 'scope': 0, 'params':[address], 'params_count': 1, 'ret_addr': address+32,
                             'is_return': 0, }}
    PB.append(convertToStr("PRINT", address))
    PB_counter += 1
    PB.append(convertToStr("JP", '@' + str(address + 32)))
    PB_counter += 1
    address += 64
    program(None, ebnf)
    file = open("output.txt", 'w')
    for i in range(len(PB)):
        file.write(str(i) + "\t" + PB[i])
    file.close()