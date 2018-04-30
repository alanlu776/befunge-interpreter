from random import randint

#basic LIFO stack
#https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
class LIFO:
    list = []
    def push(self, item):
        self.list.append(item)
    def pop(self):
        if len(self) == 0: return 0
        return self.list.pop()
    def peek(self):
        if len(self) == 0: return 0
        return self.list[-1]
    def __len__(self):
        return len(self.list)

class Interpreter:
    dirs = {
        '>' : (1, 0),
        'v' : (0, 1),
        '<' : (-1, 0),
        '^' : (0, -1),
    }

    def __init__(self, text, x=0, y=0):
        self.source = None
        self.inittext(text)
        self.stringmode = False
        self.char = None
        self.x, self.y = x, y
        self.dx, self.dy = 1, 0
        self.stack = LIFO()
        self.debugging = []

    def inittext(self, text):
        #turn the text into a matrix with uniform lengths and widths
        self.source = text.split('\n')
        self.source = [list(e) for e in self.source]
        maxlen = len(max(self.source, key=len))
        for l in self.source:
            l.extend([' ' for h in range(maxlen-len(l))])
        
        self.source = self.source[:-1]
        # ^optional line to remove pycharm's extra line insertion

        # for l in self.source: print(l)

    def update(self): #step once
        self.x += self.dx
        self.y += self.dy

    def confine(self): #confine x and y within bounds
        self.x += len(self.source[0])
        self.x %= len(self.source[0])
        self.y += len(self.source)
        self.y %= len(self.source)

    def interpret(self):
        while True:
            # print(self.source[self.x][self.y])
            self.char = self.source[self.y][self.x]

            self.debugging.append((self.char, self.x, self.y, self.stringmode))

            #stringmode
            if self.char == '"': self.stringmode = not self.stringmode

            #add character if it is stringmode
            elif self.stringmode:
                self.stack.push(ord(self.char))

            elif self.char in self.dirs:
                dir = self.dirs[self.char]
                self.dx = dir[0]; self.dy = dir[1]
            else:
                #add to stack number if it is between 0 and 9
                if 48 <= ord(self.char) <= 57: self.stack.push(int(self.char))

                #operators
                elif self.char == '+': self.stack.push(self.stack.pop() + self.stack.pop())
                elif self.char == '-':
                    a = self.stack.pop(); b = self.stack.pop()
                    self.stack.push(b-a)
                elif self.char == '*': self.stack.push(self.stack.pop() * self.stack.pop())
                elif self.char == '/':
                    a = self.stack.pop(); b = self.stack.pop()
                    self.stack.push(int(b/a))
                elif self.char == '%':
                    a = self.stack.pop(); b = self.stack.pop()
                    self.stack.push(int(b%a))

                # logical
                elif self.char == '!': self.stack.push(1 if self.stack.pop() == 0 else 0)
                elif self.char == '`':
                    a = self.stack.pop(); b = self.stack.pop()
                    self.stack.push(1 if b > a else 0)

                # directions
                elif self.char in '?_|':
                    # direction = None
                    if self.char == '?': direction = '>v<^'[randint(0, 3)]
                    elif self.char == '_': direction = '>' if self.stack.pop() == 0 else '<'
                    elif self.char == '|': direction = 'v' if self.stack.pop() == 0 else '^'
                    dir = self.dirs[direction]
                    self.dx = dir[0]; self.dy = dir[1]

                #stack operators
                elif self.char == ':': self.stack.push(self.stack.peek())
                elif self.char == '\\':
                    a = self.stack.pop(); b = self.stack.pop()
                    self.stack.push(a); self.stack.push(b)
                elif self.char == '$': self.stack.pop()

                #bridge
                elif self.char == '#':
                    self.update()
                    self.confine()

                #self changing
                elif self.char == 'p':
                    y = self.stack.pop(); x = self.stack.pop(); v = self.stack.pop()
                    #confine value
                    while v < 0: v += 255
                    v %= 255
                    if x >= len(self.source[0]) or x < 0 or y >= len(self.source) or y < 0: pass
                    else: self.source[y][x] = chr(v)
                elif self.char == 'g':
                    y = self.stack.pop(); x = self.stack.pop()
                    if x >= len(self.source[0]) or x < 0 or y >= len(self.source) or y < 0: v = ' '
                    else: v = self.source[y][x]
                    self.stack.push(ord(v))

                #input/output
                elif self.char == '.': print(self.stack.pop(), end=' ')
                elif self.char == ',': print(chr(self.stack.pop()), end='')
                elif self.char == '&':
                    val = input()
                    try: self.stack.push(int(val))
                    except: self.stack.push(0)
                elif self.char == '~':
                    val = input()
                    # self.debug()
                    if val == '': self.stack.push(-1)
                    else: self.stack.push(ord(val))
                
                elif self.char == '@': break
#                 elif self.char == ' ': pass
#                 else: print(self.char)
            self.update()
            self.confine()

    def debug(self):
        for i in self.debugging: print(i)

file = open("program.txt", 'r')
text = file.read()
interpreter = Interpreter(text)
interpreter.interpret()
#interpreter.debug()
