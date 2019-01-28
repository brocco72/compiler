class Stack:
    def __init__(self):
        self.items = []
        self.top = -1

    def push(self, item):
        self.items.append(item)
        self.top += 1

    def pop(self, n=1):
        self.top -= n
        if n == 1:
            return self.items.pop()
        else:
            ret = []
            for i in range(n):
                ret.append(self.items.pop())
            return ret


    def get(self, index):
        return ss.items[index]
    def size(self):
        return len(self.items)


ss = Stack()
add_flag = 0
PB_SIZE = 10
PB = [] * PB_SIZE
PB_counter = 0
whiles = []

def gettemp():
    pass


def findaddr(input):
    pass


def code_generation(action, input):
    global PB_counter
    if action == "#PUSH_SS":
        p = findaddr(input)
        if not p:  # if input is not in SYMBOL TABLE, insert and allocate space
            pass
        ss.push(p)
        return

    elif action == "#ADDSUB":
        t = gettemp()
        if ss.get(ss.top - 1) == "+":
            PB[PB_counter] = (ADD, ss.get(ss.top), ss.get(ss.top - 1), t)
        elif ss.get(ss.top - 1) == "-":
            PB[PB_counter] = (SUB, ss.get(ss.top), ss.get(ss.top - 1), t)
        PB_counter += 1
        ss.pop(3)
        ss.push(t)
        return
    elif action == "MULT":
        t = gettemp()
        PB[PB_counter] = (MULT, ss.get(ss.top), ss.get(ss.top - 1), t)
        PB_counter += 1
        ss.pop(2)
        ss.push(t)
        return
    elif action == "#FUN_ADDR":
        pass
    elif action == "#VAR_ADDR":
        pass
    elif action == "#ARR_ADDR":
        pass
    elif action == "#INC_SCOPE":
        pass
    elif action == "#PAR_ADDR":
        pass
    elif action == "#FUNC_SYMBTBL":
        pass
    elif action == "#DEC_SCOPE":
        pass
    elif action == "#PUSH_RETVAL":
        pass
    elif action == "#JMP_CALLER":
        pass
    elif action == "#SAVE":
        ss.push(PB_counter)
        PB_counter += 1
        return
    elif action == "#LABEL":
        ss.push(PB_counter)
        return
    elif action == "#SAVE_CONTINUE":
        whiles.append(([PB_counter], []))
        return
    elif action == "#WHILE":
        PB[ss.get(ss.top)] = (JPF, ss.get(ss.top - 1), PB_counter + 1, )
        PB[PB_counter] = (JP, ss.get(ss.top - 2), ,)
        PB_counter += 1
        last_loop_breaks = whiles[-1][1]
        for i in last_loop_breaks:
            PB[i] = (JP, PB_counter, ,)
        whiles.pop()
        ss.pop(3)
        return
    elif action == "#JMP_BEGIN":
        # PB[PB_counter] = (JP, ss.get(ss.top))
        PB[PB_counter] = (JP, whiles[-1][0][-1])
        PB_counter += 1
        return
    elif action == "#JMP_END":
        whiles[-1][1].append(PB_counter)
        PB_counter += 1
        return
    elif action == "#JPF_SAVE":
        PB[ss.get(ss.top)] = (JPF, ss.get(ss.top-1), PB_counter+1)
        ss.pop(2)
        ss.push(PB_counter)
        PB_counter += 1
        return
    elif action == "#JP":
        PB[ss.get(ss.top)] = (JP, PB_counter, ,)
        ss.pop()
        return
    elif action == "#JPT_SAVE":
        pass
    elif action == "#COMPARE_CASE":
        t = gettemp()
        PB[PB_counter] = (EQ, int(input), ss.get(ss.top - 1), t)
        PB_counter += 1
        ss.push(t)
        return
    elif action == "#JPF":
        PB[ss.get(ss.top)] = JPF(ss.get(ss.top - 1), PB_counter, ,)
        ss.pop(2)
        return
    elif action == "#PUSH_INPUT":
        ss.push(input)
        return
    elif action == "#RELOP":
        t = gettemp()
        if ss.get(ss.top - 1) == "<":
            PB[PB_counter] = (LT, ss.get(ss.top - 2), ss.get(ss.top), t)
        elif ss.get(ss.top - 1) == "==":
            PB[PB_counter] = (EQ, ss.get(ss.top - 2), ss.get(ss.top), t)
        PB_counter += 1
        ss.pop(3)
        ss.push(t)
        return
    elif action == "#RET_ADDR":
        pass
    elif action == "#JP_CALL":
        pass
    elif action == "#ASS_ARG":
        pass
