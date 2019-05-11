# self-driving-desktop

Desktop Automation Framework.
Drive your keyboard and mouse with text files.

```
pip install self-driving-desktop

sdd playlist.txt [--record]
```

### Playlists

```
playlist openTerm {
  hotkeys "ctrl" "alt" "t";
  sleep 1.0;

  name_active hofTerm;
  sleep 0.5;

  hotkeys "winleft" "left";
  sleep 1;
};

playlist closeTerm {
  focus hofTerm;
  hotkeys "ctrl" "shift" "q";
  sleep 1;
};

playlist closeChrome {
  focus hofChrome;
  hotkeys "alt" "f4";
  sleep 1;
};

playlist openChrome {
  shell "google-chrome";
  sleep 2.0;

  name_active hofChrome;
  sleep 0.5;

  hotkeys "winleft" "right";
  sleep 1;
};

playlist focusTest {
  focus hofTerm;
  sleep 0.2;
  write "date\n" 0.05;

  sleep 2;

  focus hofChrome;
  sleep 0.2;
  write "https://docs.hofstadter.io\n" 0.05;
};

playlist gsDocs {
  mv 100 100 1.5;
  mv 1111 272 1;
  click;
  sleep 2;
};

playlist main {
  wspace_down;
  sleep 0.2;

  play openTerm openChrome;

  play focusTest;
  play gsDocs;

  play closeChrome closeTerm;

  sleep 2;
  wspace_up;
};

play main;
```

### Grammar

#### Top-level:

- file has steps and playlists
- steps are the only thing run
- play runs a playlist

#### Steps:

- `play name nameB ...;`: run one or more playlists
- `delay x.y;`: set delay between steps to x.y seconds
- `sleep x.y;`: sleep for x.y seconds
- `shell "quoted strings"+;`: exec a command from the program

windows:

- `active someName;`: name the active window
- `focus someName;`: focus a named window

mouse:

- `mouse x y s;`: move the mose to x,y in s seconds
- `click;`: click the left mouse button
- `btnclick [left,middle,right];`
- `btndown [left,middle,right];`
- `btnup [left,middle,right];`
- `draw [left,middle,right] x y s;`: move the mose to x,y in s seconds
- `scroll n;`: scroll n lines, negative is up
- `hscroll n;`: horizontal scroll n "clicks", negative is left

keyboard:

- `keypress "key";`
- `keydown "key";`
- `keyup "key";`
- `hotkeys "quoted" "keys" ...;`: press some keys together
- `write "quoted string\n";`: type a string, "\n" is enter

clipboard:

- `copy;`, just `ctrl-c`
- `paste;`, just `ctrl-v`
- `save_clipboard "name";` save the clipboard contents to "name"
- `load_clipboard "name";` load the clipboard contents from "name"
- `copy_clipboard "name";` copy && save the clipboard contents to "name"
- `paste_clipboard "name";` load the clipboard contents from "name" && paste

all keys are from pyautogui

[Grammer Definition](./self_driving_desktop/grammar.py)

### Development Setup

```
virtualenv --python python3 penv
source penv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
python self_driving_desktop/__main__.py ...
```

