grammar = r"""
start: (item ";")+

item: import | coords | playlist | step

import : "import" string

coords : "coords" coords_body
coords_body : "{" coord_def ("," coord_def)* "}"

coord_def: string ":" "{" coord_body ("," coord_body)* "}"
coord_body: string ":" "[" int "," int "]"

playlist : "playlist" string playlist_body
playlist_body : "{" (step ";")* "}"

step : screen
| repeat
| play
| active
| focus
| delay
| sleep
| shell
| drag
| mouse
| coord_off
| coord
| click
| btndown
| btnup
| scroll
| hscroll
| keydown
| keyup
| hotkeys
| write
| copy
| paste
| save_clipboard
| load_clipboard
| copy_clipboard
| paste_clipboard

screen: "screen" string
repeat: "play" string+ int | "play" string+ number
play: "play" string+

active: "active" string
focus: "focus" string

delay: "delay" number
sleep: "sleep" number
shell: ("shell"|"sh") string+

coord_off: ("coord"|"mc") string number number number
coord: ("coord"|"mc") string number
mouse: ("mouse"|"mv"|"mm") number number number
drag: ("drag"|"md") string number number number
click: "click"
btnclick: ("btnclick"|"bc") string
btndown: ("btndown"|"bd") string
btnup: ("btnup"|"bu") string
scroll: "scroll" int
hscroll: "hscroll" int

keypress: ("keypress"|"kp") string
keydown: ("keydown"|"kd") string
keyup: ("keyup"|"ku") string
hotkeys: ("hotkeys"|"hk") string+
write: ("write"|"w"|"type"|"t") string number?

copy: "copy"
paste: "paste"
save_clipboard: ("save_clipboard"|"scb") string
load_clipboard: ("load_clipboard"|"lcb") string
copy_clipboard: ("copy_clipboard"|"ccb") string
paste_clipboard: ("paste_clipboard"|"pcb") string

int: INT
number: SIGNED_NUMBER
string: ESCAPED_STRING

COMMENT: /#[^\n]*/
IDENT: (LETTER|"_") (LETTER|INT|"-"|"_")*
NAME: LETTER (LETTER|INT|"-"|"_")*
WORD: LETTER+

%import common.LETTER
%import common.ESCAPED_STRING
%import common.INT
%import common.SIGNED_NUMBER
%import common.WS

%ignore COMMENT
%ignore WS
"""
