import time
import click
import pyautogui
import subprocess
from lark import Lark
from Xlib import display, X

from self_driving_desktop import parser as ourlang

d = display.Display()

playlists = {}
wins = {}

def do(t):
    if t.data == "item":
        do(t.children[0])
        return

    if t.data == "play":
        for playname in t.children:
            playlist = playlists[playname]
            do(playlist)

        return

    if t.data == "name_active":
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

    if t.data == "mv":
        cs = []
        for c in t.children:
            cs.append(do(c))

        pyautogui.moveTo(*cs, pyautogui.easeOutQuad)
        return

    if t.data == "click":
        pyautogui.click()
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
        interval=0.1
        if len(t.children) == 2:
            interval = do(t.children[1])

        pyautogui.typewrite(text, interval=interval)
        return

    if t.data == "wspace_up":
        pyautogui.hotkey('ctrl', 'alt', 'up')
        return

    if t.data == "wspace_down":
        pyautogui.hotkey('ctrl', 'alt', 'down')
        return

    raise SyntaxError('Unknown instruction: %s' % t.data)

@click.command()
@click.option('--playlist', default="test.txt", help='Playlist to run.')
def drive(playlist):
    parser = Lark(ourlang.grammar, parser='lalr')

    with open(playlist) as f:
        tree = parser.parse(f.read())
        # print(tree)
        # print("="*16)
        for t in tree.children:
            do(t)
