# self-driving-desktop

Desktop Automation framework

_tested on linux/gnome3_


```
python main.py --playlist path/to/file.txt
```

### Development Setup

```
virtualenv --python python3 penv
source penv/bin/activate
pip install -r requirements.txt
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

### Grammer

Top-level:

- file has steps and playlists
- steps are the only thing run
- play runs a playlist

Steps:

- `play name+;`: run one or more playlists
- `sleep x.y;`: sleep for x.y seconds
- `mv x y s;`: move the mose to x,y in s seconds
- `click;`: click the left mouse button
- `wspace_down;`: move one workspace down
- `wspace_up;`: move one workspace up
- `hotkeys "quoted" "keys" ...;`: press some keys together
- `write "quoted string\n";`: type a string, "\n" is enter
- `shell "quoted strings"+;`: exec a command from the program
- `name_active someName;`: name the active window
- `focus someName;`: focus a named window


```
start: item+

item: step ";" | playlist ";"

playlist : "playlist" WORD playlist_body
playlist_body : "{" (step ";")* "}"

step : play
  | sleep
  | mv
  | wspace_down
  | wspace_up
  | hotkeys
  | write
  | shell
  | name_active
  | focus

play: "play" WORD+

name_active: "name_active" WORD
focus: "focus" WORD

sleep: "sleep" number
mv: "mv" number number number

wspace_down: "wspace_down"
wspace_up: "wspace_up"

hotkeys: "hotkeys" string+
write: "write" string number?
shell: "shell" string+


number: SIGNED_NUMBER
string: ESCAPED_STRING

COMMENT: /#[^\n]*/
WORD: LETTER+

%import common.LETTER
%import common.ESCAPED_STRING
%import common.INT
%import common.SIGNED_NUMBER
%import common.WS

%ignore COMMENT
%ignore WS
```

