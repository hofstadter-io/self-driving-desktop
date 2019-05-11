import os
import time
from lark import Lark
import pyautogui
import clipboard
import subprocess
from Xlib import display, X

from self_driving_desktop import grammar as G

pyautogui.PAUSE = 0.01

d = display.Display()

parser = None
dirname = None
filename = None
dirstack = []
screen = "1080p"
coords = {}
playlists = {}
wins = {}
clipboards = {}


def run(playlist):
    global parser
    parser = Lark(G.grammar, parser='lalr')
    dirname = os.path.dirname(playlist)

    setFilename(playlist)
    pushDir(dirname)

    with open(playlist) as f:
        tree = parser.parse(f.read())
        # print(tree)
        # print("="*16)
        for t in tree.children:
            do(t)


def setFilename(n):
    global filename
    filename = n


def pushDir(d):
    global dirname
    dirname = d
    dirstack.append(d)


def popDir():
    global dirname
    dirname = dirstack.pop()


def do(t):
    global parser
    global dirname
    global filename
    global screen
    global coords
    global playlists
    global wins
    global clipboards

    if t.data == "item":
        do(t.children[0])
        return

    if t.data == "import":
        fname = do(t.children[0])
        dname = os.path.dirname(fname)
        fullname = os.path.join(dirname, fname)
        fulldir = os.path.join(dirname, dname)

        currfile = filename
        setFilename(fullname)
        pushDir(fulldir)
        try:
            with open(fullname) as f:
                tree = parser.parse(f.read())
                for t in tree.children:
                    do(t)
        except Exception as e:
            print("Error in file:", fullname)
            raise e

        setFilename(currfile)
        popDir()
        return

    if t.data == "coords":
        do(t.children[0])
        return

    if t.data == "coords_body":
        for c in t.children:
            do(c)

        return

    if t.data == "coord_def":
        name = do(t.children[0])

        try:
            coords[name]
        except:
            coords[name] = {}

        for c in t.children[1:]:
            pnt = do(c)
            coords[name][pnt[0]] = pnt[1:]

        return

    if t.data == "coord_body":
        name = do(t.children[0])
        x = do(t.children[1])
        y = do(t.children[2])
        return [name, x, y]

    if t.data == "playlist":
        name, pl = t.children
        playlists[name] = pl
        return

    if t.data == "playlist_body":
        for c in t.children:
            do(c)

        return

    if t.data == "screen":
        name = do(t.children[0])
        screen = name
        return

    if t.data == "repeat":
        count = do(t.children[-1])

        for x in range(1, int(count)):
            for playname in t.children[:-1]:
                playlist = playlists[playname]
                do(playlist)

        return

    if t.data == "play":
        for playname in t.children:
            playlist = playlists[playname]
            do(playlist)

        return

    if t.data == "active":
        name = t.children[0]
        w = d.get_input_focus().focus
        wins[name] = w
        return

    if t.data == "focus":
        name = t.children[0]
        w = wins[name]
        w.set_input_focus(X.RevertToNone, X.CurrentTime)
        w.configure(stack_mode=X.Above)
        d.sync()
        return

    if t.data == "comment":
        return

    if t.data == "string":
        text = t.children[0][1:-1]
        text = text.replace("\\n", "\n")
        return text

    if t.data == "int":
        return int(t.children[0])

    if t.data == "number":
        return float(t.children[0])

    if t.data == "playlist":
        name, pl = t.children
        playlists[name] = pl
        return

    if t.data == "playlist_body":
        for c in t.children:
            do(c)

        return

    if t.data == "step":
        step = t.children[0]
        do(step)
        return

    if t.data == "sleep":
        sec = do(t.children[0])
        time.sleep(sec)
        return

    if t.data == "delay":
        sec = do(t.children[0])
        pyautogui.PAUSE = sec
        return

    if t.data == "drag":
        btn = do(t.children[0])
        cs = []
        for c in t.children[1:]:
            cs.append(do(c))

        # pyautogui.drag(*cs, button=btn)
        # hack, because the cursor keeps moving...?
        pyautogui.mouseDown(button=btn)
        pyautogui.moveTo(cs[0], cs[1])
        pyautogui.mouseUp(button=btn)
        return

    if t.data == "coord":
        name = do(t.children[0])
        t = do(t.children[1])

        pnt = coords[name][screen]
        x, y = pnt[0], pnt[1]

        pyautogui.moveTo(x, y, t, pyautogui.easeOutQuad)
        return

    if t.data == "coord_off":
        name = do(t.children[0])
        x = do(t.children[1])
        y = do(t.children[2])
        t = do(t.children[3])

        pnt = coords[name][screen]
        px, py = pnt[0], pnt[1]

        x = px + x
        y = py + y

        pyautogui.moveTo(x, y, t, pyautogui.easeOutQuad)
        return

    if t.data == "mouse":
        cs = []
        for c in t.children:
            cs.append(do(c))

        pyautogui.moveTo(*cs, pyautogui.easeOutQuad)
        return

    if t.data == "click":
        pyautogui.click()
        return

    if t.data == "btnclick":
        btn = do(t.children[0])
        pyautogui.click(button=btn)
        return

    if t.data == "btndown":
        btn = do(t.children[0])
        pyautogui.mouseDown(button=btn)
        return

    if t.data == "btnup":
        btn = do(t.children[0])
        pyautogui.mouseUp(button=btn)
        return

    if t.data == "scroll":
        lines = do(t.children[0])
        pyautogui.scroll(lines)
        return

    if t.data == "hscroll":
        lines = do(t.children[0])
        pyautogui.hscroll(lines)
        return

    if t.data == "keypress":
        key = do(t.children[0])
        pyautogui.press(key)
        return

    if t.data == "keydown":
        key = do(t.children[0])
        pyautogui.keyDown(key)
        return

    if t.data == "keyup":
        key = do(t.children[0])
        pyautogui.keyUp(key)
        return

    if t.data == "hotkeys":
        cs = []
        for c in t.children:
            cs.append(do(c))

        pyautogui.hotkey(*cs)
        return

    if t.data == "shell":
        cs = []
        for c in t.children:
            cs.append(do(c))

        subprocess.Popen(cs)
        return

    if t.data == "write":
        text = do(t.children[0])
        interval = 0.1
        if len(t.children) == 2:
            interval = do(t.children[1])

        pyautogui.typewrite(text, interval=interval)
        return

    if t.data == "copy":
        pyautogui.hotkey("ctrl", "c")
        return

    if t.data == "paste":
        pyautogui.hotkey("ctrl", "v")
        return

    if t.data == "save_clipboard":
        name = do(t.children[0])
        value = clipboard.paste()
        clipboards[name] = value
        return

    if t.data == "load_clipboard":
        name = do(t.children[0])
        value = clipboards[name]
        clipboard.copy(value)
        return

    if t.data == "copy_clipboard":
        pyautogui.hotkey("ctrl", "c")
        name = do(t.children[0])
        value = clipboard.paste()
        clipboards[name] = value
        return

    if t.data == "paste_clipboard":
        name = do(t.children[0])
        value = clipboards[name]
        clipboard.copy(value)
        pyautogui.hotkey("ctrl", "v")
        return

    raise SyntaxError('In file: %s\n  Unknown instruction: %s' % (filename, t.data))
