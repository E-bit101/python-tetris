import time
import random
import os

# Colors
class col:
    Black  = '\033[30m'
    Red    = '\033[31m'
    Green  = '\033[32m'
    Yellow = '\033[33m'
    Blue   = '\033[34m'
    Purple = '\033[35m'
    Cyan   = '\033[36m'
    White  = '\033[37m'
    Bright_white = '\033[97m'

    HEADER = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Setup for getting input in real time
if os.name == 'nt':  # Windows
    import msvcrt # Built in on windows

    def get_key(fps):
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b"\xe0":
                return "^" + msvcrt.getch().decode('utf-8', errors='ignore')
            return char.decode('utf-8', errors='ignore')
        return None
else:  # Unix/Linux/macOS
    # Built in imports on Unix based systems
    import termios
    import tty
    import select

    def get_key(fps):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            if select.select([sys.stdin], [], [], 1/fps)[0]:
                ch1 = sys.stdin.read(1)
                if ch1 == '\x1b':
                    if select.select([sys.stdin], [], [], 0.001)[0]:
                        ch2 = sys.stdin.read(1)
                        if select.select([sys.stdin], [], [], 0.001)[0]:
                            ch3 = sys.stdin.read(1)
                            return ch1 + ch2 + ch3
                    return ch1
                return ch1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

# Count unique items in a list
def count_unique(list):
    unique = []
    counter = 0
    for i in list:
        if not i in unique:
            unique.append(i)
            counter += 1
    return counter

# Controls
up = ["w", "H", "\x1b[A"]
down = ["s", "P", "\x1b[B"]
left = ["a", "K", "\x1b[D"]
right = ["d", "M", "\x1b[C"]

# Helper functions for drawing to the screen
def create_screen(width, height, bg_color=col.Blue):
    screen = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(bg_color + "██")
        screen.append(row)
    return screen

def draw_screen(screen):
    out = ""
    for y in range(len(screen)):
        for x in range(len(screen[0])):
            out = out + screen[y][x]
        out = out + "\n"
    return out

def set_pixel(screen, x, y, color):
    screen[round(y)%len(screen)][round(x)%len(screen[0])] = color + "██"
    return screen

def get_pixel(screen, x, y):
    return screen[round(y)%len(screen)][round(x)%len(screen[0])].replace("██", "")

fps = 60

up    = ["w", "^H", "\x1b[A"]
down  = ["s", "^P", "\x1b[B"]
left  = ["a", "^K", "\x1b[D"]
right = ["d", "^M", "\x1b[C"]

tetrominos_0 = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(-1, 0), (0, 0), (1, 0), (1, 1)],
    [(-1, 0), (0, 0), (1, 0), (-1, 1)],
    [(-1, 0), (0, 0), (1, 0), (0, 1)],
    [(0, 0), (1, 0), (-1, 1), (0, 1)],
    [(-1, 0), (0, 0), (0, 1), (1, 1)],
    [(-2, 0), (-1, 0), (0, 0), (1, 0)],
]

tetrominos_90 = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(0, -1), (0, 0), (0, 1), (1, -1)],
    [(0, -1), (0, 0), (0, 1), (1, 1)],
    [(0, -1), (0, 0), (1, 0), (0, 1)],
    [(0, -1), (0, 0), (1, 0), (1, 1)],
    [(1, -1), (0, 0), (1, 0), (0, 1)],
    [(0, -1), (0, 0), (0, 1), (0, 2)],
]

tetrominos_180 = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(-1, -1), (-1, 0), (0, 0), (1, 0)],
    [(-1, 0), (0, 0), (1, 0), (1, -1)],
    [(-1, 0), (0, 0), (1, 0), (0, -1)],
    [(0, 0), (1, 0), (-1, 1), (0, 1)],
    [(-1, 0), (0, 0), (0, 1), (1, 1)],
    [(-2, 1), (-1, 1), (0, 1), (1, 1)],
]

tetrominos_270 = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(-1, 1), (0, -1), (0, 0), (0, 1)],
    [(-1, -1), (0, -1), (0, 0), (0, 1)],
    [(0, -1), (0, 0), (-1, 0), (0, 1)],
    [(0, -1), (0, 0), (1, 0), (1, 1)],
    [(1, -1), (0, 0), (1, 0), (0, 1)],
    [(1, -1), (1, 0), (1, 1), (1, 2)],
]

tetromino_colors = [
    col.Red,
    col.Green,
    col.Blue,
    col.Yellow,
    col.Cyan,
    col.Purple,
    col.White,
]

rotation = 0
position = [8, -2]
old_pos = position
old_tetrominos = tetrominos_0
selected_tetromino = random.randint(0, len(tetrominos_0)-1)
counter = 0
slow = 30
score = 0

screen = create_screen(18, 32, col.Black)

while True:
    key = get_key(fps)
    
    if key in down:
        score += 1

    if key == None and counter >= slow:
        counter = 0
        key = down[0]

    if key in up:
        rotation = (rotation + 90) % 360
    elif key in down:
        position[1] -= 1
        score += 1
    elif key in left:
        position[0] -= 1
    elif key in right:
        position[0] += 1

    if rotation == 0:
        tetrominos = tetrominos_0
    elif rotation == 90:
        tetrominos = tetrominos_90
    elif rotation == 180:
        tetrominos = tetrominos_180
    elif rotation == 270:
        tetrominos = tetrominos_270

    for i in old_tetrominos[selected_tetromino]:
        screen = set_pixel(screen, old_pos[0] + i[0], -old_pos[1] - i[1], col.Black)

    if position != old_pos or tetrominos != old_tetrominos:
        for i in tetrominos[selected_tetromino]:
            if get_pixel(screen, position[0] + i[0], -position[1] - i[1]) != col.Black:
                position = old_pos
                tetrominos = old_tetrominos
                if key in down:
                    for i in tetrominos[selected_tetromino]:
                        screen = set_pixel(screen, position[0] + i[0], -position[1] - i[1], tetromino_colors[selected_tetromino])
                    rotation = 0
                    position = [8, -2]
                    old_pos = position
                    old_tetrominos = tetrominos_0
                    selected_tetromino = random.randint(0, len(tetrominos_0)-1)
                if get_pixel(screen, position[0] + i[0], -position[1] - i[1]) != col.Black:
                    pass
                break

    for i in tetrominos[selected_tetromino]:
        screen = set_pixel(screen, position[0] + i[0], -position[1] - i[1], tetromino_colors[selected_tetromino])
    old_pos = [position[0], position[1]]
    old_tetrominos = tetrominos

    for y in range(len(screen)):
        screen = set_pixel(screen, 0, y, col.Bright_white)
        screen = set_pixel(screen, -1, y, col.Bright_white)

    for x in range(len(screen)):
        screen = set_pixel(screen, x, 0, col.Bright_white)
        screen = set_pixel(screen, x, -1, col.Bright_white)

    for row in range(len(screen[0])-4):
        clear_row = True
        for x in range(len(screen)-2):
            clear_row = clear_row and get_pixel(screen, x+1, -2-row) != col.Black
        if clear_row and position == [8, -2]:
            score += 100
            for y in range(len(screen[0])-3):
                for x in range(len(screen)-2):
                    color = get_pixel(screen, x+1, -3-y-row)
                    screen = set_pixel(screen, x+1, -2-y-row, color)

    if os.name != 'nt':
        os.system('clear')
        print(f"{draw_screen(screen)}\nScore: {score}", end=col.White, flush=True)
    else:
        print(f"\033c{draw_screen(screen)}\nScore: {score}", end=col.White, flush=True)
    
    if os.name == 'nt':
        time.sleep(1/fps)
    counter += 1