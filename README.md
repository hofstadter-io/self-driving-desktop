# self-driving-desktop

Desktop Automation Framework.
Drive your keyboard and mouse with text files.

```
pip3 install self-driving-desktop
```

### Running

Playing a playlist:

```
sdd playlist.txt
```

Recording a playlist:

```
sdd --record recording.txt
```

### Playlists

```
# Import other playlist files
import "test/main.txt";

# Create Coordinates
coords {
  "center": {
    "1080p": [960, 540],
    "720p":  [640, 360]
  }
};

# Create a playlist
playlist "openChrome" {
  # Run programs in the shell
  shell "google-chrome";
  sleep 2.0;

  # Name the new window
  active "hofChrome";
  sleep 0.5;

  # Use hotkeys to arrange
  hotkeys "winleft" "right";
  sleep 1;
};

playlist "closeChrome" {
  # Focus a named window
  focus "hofChrome";
  hotkeys "alt" "f4";
  sleep 1;
};

playlist "readTheDocs" {
  # Go to a webpage
  focus "hofChrome";
  sleep 0.2;

  # Type the URL
  write "https://docs.hofstadter.io\n" 0.05;

  # Goto an imported coordinate
  coord "getting-started" 0.5;
};

# Move the mouse in a square
playlist "repeatTest" {
  mm 100 100 1;
  mm 1000 100 1;
  mm 1000 500 1;
  mm 100 500 1;
};

# Our main playlist
playlist "main" {
  # Goto a named coordinate, also with offset
  coord "center" 1;
  coord "center" 250 -250 1;

  # Operate the browser
  play "openChrome";
  play "readTheDocs";
  play "closeChrome";

  # Play a playlist multiple times
  play "repeatTest" 4;

};

# Set screen size
screen "1080p";

# Set the global delay between steps
delay 0.025;

# Finally, play our main playlist
play "main";

```

### Grammar

#### Top-level:

- file has steps and playlists
- steps are the only thing run
- play runs a playlist

```
# relative imports from file
import "relative/path.txt";

# named coordinates
coords {
  # coord name
  "center": {
    # screen identifier
    "1080p": [960, 540],
    "720p":  [640, 360]
  }
};

# define playlists
playlist "my-playlist" {
  steps...;
};

playlist "main" {
  steps...;
  # run playlists from playlists
  play "my-playlist"
}

# set the screen identifier
screen "1080p";

# run a playlist
play "my-playlist" "main";
```

#### Steps:

- `play "name" "nameB" ... [N];`: run one or more playlists, optionally repeat N times.
- `delay x.y;`: set delay between steps to x.y seconds
- `sleep x.y;`: sleep for x.y seconds
- `screen "screen";`: set the screen resolution identifier
- `shell "quoted strings"+;`: exec a command from the program

windows:

- `active "someName";`: name the active window
- `focus "someName";`: focus a named window

mouse:

- `mouse x y s;`: move the mouse to x,y in s seconds
- `coord "name" s;`: move the mouse to a named coordinate in s seconds
- `coord "name" x y s;`: move to a named coordinate with offset in s seconds
- `click;`: click the left mouse button
- `btnclick [left,middle,right];`
- `btndown [left,middle,right];`
- `btnup [left,middle,right];`
- `drag [left,middle,right] x y s;`: drag the mouse to x,y in s seconds
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

all keys are from [pyautogui](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys)

[Grammer Definition](./self_driving_desktop/grammar.py)

### Recording

You can record your mouse and keyboard
to a playlist file by:

```
sdd record.txt --record
```

_Note, not all keys are working yet._

A keymap to fix some is [here](./self_driving_desktop/keymap.py).

### Development Setup

```
virtualenv --python python3 penv
source penv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
python self_driving_desktop/__main__.py ...
```

Install from local repository:

```
git clone https://github.com/hofstadter-io/self-driving-desktop
pip3 install ./self-driving-desktop/
```

