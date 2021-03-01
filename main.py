import time as t
import random as r
import subprocess


def install(pack):
    subprocess.call(f'pip install {pack}')


try:
    import numpy as np
except:
    install('numpy')
    import numpy as np
try:
    import pygame as pg
except:
    install('pygame')
    import pygame as pg


class filler:
    def __init__(self):
        self.owner = 0
        self.y = 1

    def draw(self):
        pass

    def get(self):
        return 0


class part:
    def __init__(self, x, y, color, owner):
        self.color = color
        x %= 10
        self.x = x
        self.y = y
        self.owner = owner
        self.qu = ''
        global arr
        arr[y, x] = self

    def move(self, mod1, mod2):
        global arr
        arr[self.y, self.x] = filler()
        self.x += mod1
        self.y += mod2
        self.qu += f'arr[{self.y}, {self.x}] = self\n'

    def clear(self):
        exec(self.qu)
        self.qu = ''

    def get(self):
        return self.owner

    def draw(self):
        global res
        pg.draw.rect(scr, self.color, (self.x * res, self.y * res, res, res))

    def check(self):
        global arr
        if not 0 <= self.y < 19:
            return 1
        return arr[self.y + 1, self.x].owner

    def check_free(self, mod1, mod2):
        a = self.x + mod1
        b = self.y + mod2
        if 0 <= b < 20 and 0 <= a < 10:
            global arr
            return arr[b, a].get()
        return 1

    def delete(self):
        global arr
        arr[self.y, self.x] = filler()
        del self


class figure:
    def __init__(self, x, y, mods, color):
        self.x = x
        self.y = y
        self.mods = mods
        self.parts = []
        self.color = color

    def start(self):
        for i in self.mods:
            self.parts.append(part(self.x + i[0], self.y + i[1], self.color, 0))

    def fall(self):
        ans = 0
        for i in self.parts:
            ans += i.check()
        if ans == 0:
            self.y += 1
            for i in self.parts:
                i.move(0, 1)
            for i in self.parts:
                i.clear()
        else:
            self.stop()

    def move(self, mod1, mod2):
        ans = 0
        for i in self.parts:
            ans += i.check_free(mod1, mod2)
        if ans == 0:
            self.x += mod1
            self.y += mod2
            for i in self.parts:
                i.move(mod1, mod2)
            for i in self.parts:
                i.clear()

    def rotate(self, right):
        ans = 0
        global rot, rot1
        if right:
            d = rot
        else:
            d = rot1

        for i in range(4):
            ans += self.parts[i].check_free(*d[self.mods[i]])
        if ans == 0:
            for i in self.parts:
                i.delete()
            for i in range(4):
                self.mods[i] = d[self.mods[i]]
            del self.parts[:]
            for i in range(4):
                self.parts.append(part(self.x + self.mods[i][0], self.y + self.mods[i][1], self.color, 0))

    def stop(self):
        global cur
        generate()
        mn = 19
        for i in self.parts:
            i.owner = 1
            mn = min(i.y, mn)
        if mn <= 2:
            death()
        del self

    def prerender(self):
        global res
        for i in self.mods:
            pg.draw.rect(scr, self.color, (res * (12 + i[0]), (4 + i[1]) * res, res, res))


class f1(figure):
    def __init__(self):
        super().__init__(4, 0, [(-1, 0), (0, 0), (1, 0), (2, 0)], (255, 255, 255))


class f2(figure):
    def __init__(self):
        super().__init__(4, 1, [(0, -1), (0, 0), (0, 1), (1, 1)], (100, 100, 255))


class f3(figure):
    def __init__(self):
        super().__init__(4, 1, [(0, -1), (0, 0), (0, 1), (1, -1)], (255, 100, 100))


class f4(figure):
    def __init__(self):
        super().__init__(4, 1, [(1, 0), (0, 0), (1, 1), (0, 1)], (100, 255, 100))


class f5(figure):
    def __init__(self):
        super().__init__(4, 1, [(0, -1), (0, 0), (1, 0), (1, 1)], (255, 200, 200))


class funny(figure):
    def __init__(self):
        super().__init__(4, 1, [(-1, 0), (0, 0), (1, 0), (0, -1)], (155, 255, 255))


class f6(figure):
    def __init__(self):
        super().__init__(4, 1, [(-1, 0), (0, 0), (1, 0), (0, 1)], (155, 255, 255))


class f7(figure):
    def __init__(self):
        super().__init__(4, 1, [(0, -1), (0, 0), (-1, 0), (-1, 1)], (200, 255, 200))


class sqr:
    def __init__(self, x, y, a, color):
        self.x = x
        self.y = y
        self.a = a
        self.color = color

    def draw(self, mod1, mod2):
        pg.draw.rect(scr, self.color, (self.x * self.a + mod1, self.y * self.a + mod2, self.a, self.a))


class digit:
    def __init__(self, x, y, a, color, mods):
        self.elems = []
        self.x = x
        self.y = y
        self.a = a
        for mod in mods:
            self.elems.append(sqr(*mod, a, color))

    def draw(self):
        for i in self.elems:
            i.draw(self.x + 4 * self.a, self.y)


class _1(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)])


class _2(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2),
                                          (1, 2), (0, 2), (0, 3), (2, 4), (1, 4), (0, 4)])


class _3(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2),
                                          (0, 2), (1, 2), (2, 3), (2, 4), (0, 4), (1, 4), (2, 4)])


class _4(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2),
                                          (2, 2), (1, 2), (2, 3), (2, 4)])


class _5(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2),
                                          (1, 2), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4)])


class _6(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2),
                                          (0, 3), (0, 4), (1, 2), (1, 4), (2, 2), (2, 3), (2, 4)])


class _7(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2),
                                          (1, 3), (1, 4)])


class _8(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                          (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (1, 0), (1, 2), (1, 4)])


class _9(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (0, 1), (0, 2), (0, 4), (2, 0),
                                          (2, 1), (2, 2), (2, 3), (2, 4), (1, 0), (1, 2), (1, 4)])


class _0(digit):
    def __init__(self, x, y, a, color=(255, 255, 255)):
        super().__init__(x, y, a, color, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                          (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (1, 0), (1, 4)])


class number:
    def __init__(self, num, mod1=0, mod2=0):
        global digit_conv, res
        num = str(num)
        self.nums = []
        n = len(num)
        a = int(5 * res / (5 * 6))
        for i in range(len(num)):
            self.nums.append(digit_conv[num[i]](10 * res + 4 * a * i + mod1, res * 7 + mod2, a))


def get():
    global hist
    try:
        a = int(next(hist))
    except Exception as e:
        global cur
        d = [*range(1, 8)]
        d.remove(int(str(type(cur))[-3]))
        a = r.choice(d)
        global add
        add += str(a)
        return a


def generate():
    global cur, last, prer, without_stick
    cur = prer
    cur.start()
    last += 0.1
    if without_stick >= 17:
        prer = f1()
        without_stick = 0
    else:
        d = {1: f1, 2: f2, 3: f3, 4: f4, 5: f5, 6: f6, 7: f7}
        prer = d[get()]()
        if type(prer) == f1:
            without_stick = 0
        else:
            without_stick += 1


def death():
    global cond
    cond = False


rot1 = {(-2, 0): (0, 2), (-1, -1): (-1, 1), (-1, 0): (0, 1),
        (-1, 1): (1, 1), (0, -2): (-2, 0), (0, -1): (-1, 0),
        (0, 0): (0, 0), (0, 1): (1, 0), (0, 2): (2, 0), (1, -1): (-1, -1),
        (1, 0): (0, -1), (1, 1): (1, -1), (2, 0): (0, -2)}

rot = {(0, 2): (-2, 0), (-1, 1): (-1, -1), (0, 1): (-1, 0), (1, 1): (-1, 1),
       (-2, 0): (0, -2), (-1, 0): (0, -1), (0, 0): (0, 0), (1, 0): (0, 1),
       (2, 0): (0, 2), (-1, -1): (1, -1), (0, -1): (1, 0), (1, -1): (1, 1),
       (0, -2): (2, 0)}

digit_conv = {'0': _0, '1': _1, '2': _2, '3': _3, '4': _4, '5': _5,
              '6': _6, '7': _7, '8': _8, '9': _9}

mode = False
script = '1.txt'
if mode:
    with open(script, 'r') as file:
        hist = file.read().__iter__()
else:
    hist = ''.__iter__()
add = ''

res = 30
w, h = 10 * res, 20 * res
scr = pg.display.set_mode((w + 5 * res, h))
timer = pg.time.Clock()
arr = np.array([[filler() for i in range(10)] for i in range(20)])
cond = True
without_stick = 0
prer = r.choice([f1(), f2(), f3(), f4(), f5(), f6(), f7()])
cur = r.choice([f1(), f2(), f3(), f4(), f5(), f6(), f7()])
last = t.time()
generate()
last = t.time()
qu = ''
score = 0
counter = 0
timing = 0.1
converter = {0: 0, 1: 1200, 2: 1800, 3: 2500, 4: 3600}
pressed = {}
print("(you're able to check results in tetris_results.txt)")
username = 'coftochka'  # input("Your nickname: ")
while cond:
    i = 19
    lpf = 0
    numb = number(score)
    ws = number(without_stick, mod2=100)
    while i > 0:
        s = 0
        for j in range(10):
            s += arr[i, j].owner
        if s == 10:
            for j in range(10):
                arr[i, j].delete()
            for A in range(i):
                I = i - A
                for j in range(10):
                    arr[I, j] = arr[I - 1, j]
                    arr[I, j].y += 1
            lpf += 1
            arr[0, :].fill(filler())
        else:
            i -= 1
    if lpf != 0:
        timing = max(timing - 0.005, 0.05)
    score += converter[lpf]
    for event in pg.event.get():
        if event.type == pg.QUIT:
            cond = False
            continue
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_k:
                cur.rotate(True)
            elif event.key == pg.K_l:
                pass
                cur.rotate(False)
            elif event.key == pg.K_a:
                cur.move(-1, 0)
                pressed['a'] = last
            elif event.key == pg.K_d:
                cur.move(1, 0)
                pressed['d'] = last
            elif event.key == pg.K_s:
                cur.fall()
                pressed['s'] = last
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                if 'a' in pressed:
                    del pressed['a']
            elif event.key == pg.K_d:
                if 'd' in pressed:
                    del pressed['d']
            elif event.key == pg.K_s:
                if 's' in pressed:
                    del pressed['s']

    tm = t.time()
    counter += tm - last
    last = t.time()
    if counter > timing:
        cur.fall()
        counter = 0
    for key, val in pressed.items():
        if last - val >= 0.1:
            if key == 'a':
                cur.move(-1, 0)
            elif key == 'd':
                cur.move(1, 0)
            else:
                cur.fall()
            pressed[key] = last
    exec(qu)
    qu = ''
    cl = (70, 70, 70)
    for i in range(11):
        pg.draw.line(scr, cl, (i * res, 0), (i * res, res * 20))
    for j in range(21):
        pg.draw.line(scr, cl, (0, j * res), (10 * res, j * res))
    for elem in numb.nums:
        elem.draw()
    for elem in ws.nums:
        elem.draw()
    for i in range(20):
        for j in range(10):
            arr[i, j].draw()
    prer.prerender()
    pg.draw.line(scr, (200, 225, 255), (w + 2, h), (w + 2, 0), 4)
    pg.display.flip()
    timer.tick(60)
    scr.fill((60, 60, 60))

with open('Tetris results.txt', 'a') as file:
    file.write(f'{username} : {score}\n')
if mode:
    with open(script, 'a') as file:
        file.write(add)
pg.quit()
print(score)