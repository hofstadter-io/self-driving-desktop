grammar = r"""
start: (item ";")+

item: playlist | step

playlist : "playlist" WORD playlist_body
playlist_body : "{" (step ";")* "}"

step : play
| active
| focus
| delay
| sleep
| shell
| drag
| mouse
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

play: "play" WORD+

active: "active" WORD
focus: "focus" WORD

delay: "delay" number
sleep: "sleep" number
shell: ("shell"|"sh") string+

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
WORD: LETTER+

%import common.LETTER
%import common.ESCAPED_STRING
%import common.INT
%import common.SIGNED_NUMBER
%import common.WS

%ignore COMMENT
%ignore WS
"""
