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
        scope += 1
        source_text = source_text.replace("{", "", 1)
        return "{", special
    elif source_text.find("}") == 0:
        global scope
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
