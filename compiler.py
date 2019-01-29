import re

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

with open("code.c", "r") as file:
    source_text = file.read()

source_text += "$"

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


def findaddr(input):
    pass


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
    elif action == "#ADDSUB":
        t = gettemp()
        if ss[top(ss) - 1] == "+":
            PB.append(convertToStr("ADD", symbol_table[ss[top(ss)]].values()[0], symbol_table[ss[top(ss) - 1]].values()[0], t))
        elif ss[top(ss) - 1] == "-":
            PB.append(convertToStr("SUB", symbol_table[ss[top(ss)]].values()[0], symbol_table[ss[top(ss) - 1]].values()[0], t))
        PB_counter += 1
        for i in range(3):
            ss.pop()
        ss.append(t)
        return
    elif action == "MULT":
        t = gettemp()
        # symbol_table[ss[top(ss)]]
        PB.append(convertToStr("MULT", symbol_table[ss[top(ss)]].values()[0], symbol_table[ss[top(ss) - 1]].values()[0], t))
        # PB[PB_counter] = (MULT, ss[top(ss)], ss[top(ss) - 1], t)
        PB_counter += 1
        ss.pop()
        ss.pop()
        ss.append(t)
        return
    elif action == "#FUN_ADDR":
        fun_id = ss.pop()
        fun_dict = symbol_table[fun_id].values()[0]
        fun_dict['addr'] = PB_counter
        fun_dict['params'] = []
        fun_dict['params_count'] = 0
        fun_dict['ret_addr'] = address
        ss.append(fun_dict['ret_addr'])
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
        address += 32 * input
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
        PB.append('(JP, ' + str(fun_dict['ret_addr']) + ', , )')
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
        elif ss[top(ss) - 1] == "==":
            PB.append(convertToStr("EQ", ss[top(ss) - 2], ss[top(ss)], t))
        PB_counter += 1
        for i in range(3):
            ss.pop()
        ss.append(t)
        return
    elif action == "#RET_ADDR":
        fun_dict = symbol_table[ss.pop()].values()[0]
        fun_dict['ret_addr'] = PB_counter
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
        t2 = gettemp()
        PB.append(convertToStr("ASSIGN", str('@') + str(t1), t2))
        PB_counter += 1
        ss.pop()
        ss.append(t2)
        return
    elif action == "#PUSH_NUM":
        t1 = gettemp()
        PB.append(convertToStr("ASSIGN", '#' + str(input), t1))
        PB_counter += 1
        ss.append(t1)
        return