# Python 2/3 compatibility.
from __future__ import print_function

import sys
import os
from datetime import datetime


# Change path so we find Xlib
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq

local_dpy = display.Display()
record_dpy = display.Display()

outfile=None
lasttime=None

key_map = {
    "Up": "up",
    "Down": "down",
    "Left": "left",
    "Right": "right",
    "Super_L": "winleft",
    "Control_L": "ctrlleft",
    "Alt_L": "altleft"
}

def lookup_keysym(keysym):
    for name in dir(XK):
        if name[:3] == "XK_" and getattr(XK, name) == keysym:
            return name[3:]
    return "[%d]" % keysym

def record_callback(reply):
    global lasttime

    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        print("* received swapped protocol data, cowardly ignored")
        return
    if not len(reply.data) or reply.data[0] < 2:
        # not an event
        return

    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
        currtime = datetime.now()
        tdiff = currtime - lasttime
        tmicro = tdiff.microseconds / 1000000.0

        if event.type in [X.KeyPress, X.KeyRelease]:
            pr = event.type == X.KeyPress and "Press" or "Release"
            kd = pr == "Press" and "d" or "u"

            outfile.write("  sleep %f;\n" % tmicro)

            keysym = local_dpy.keycode_to_keysym(event.detail, 0)
            if not keysym:
                lasttime = currtime
                key = None
                try:
                    key = key_map[event.detail]
                except:
                    key = event.detail

                outfile.write("  k%s \"%s\";  # KeyCode\n" % (kd, key))
                print("KeyCode%s" % pr, event.detail)
            else:
                lasttime = currtime
                key1 = lookup_keysym(keysym)
                key = None
                try:
                    key = key_map[key1]
                except:
                    key = key1

                outfile.write("  k%s \"%s\";  # KeyStr\n" % (kd, key))
                print("KeyStr%s" % pr, key)

            if event.type == X.KeyPress and keysym == XK.XK_Escape:
                local_dpy.record_disable_context(ctx)
                local_dpy.flush()
                return

        # STAY HERE
        elif event.type == X.ButtonPress:
            lasttime = currtime
            print("ButtonPress", event.detail)
            btn = ""
            if event.detail == 1:
                btn = "left"
            elif event.detail == 2:
                btn = "middle"
            elif event.detail == 3:
                btn = "right"

            outfile.write("  sleep %f;\n" % tmicro)
            outfile.write("  bu \"%s\";\n" % btn)
        elif event.type == X.ButtonRelease:
            lasttime = currtime
            print("ButtonRelease", event.detail)
            btn = ""
            if event.detail == 1:
                btn = "left"
            elif event.detail == 2:
                btn = "middle"
            elif event.detail == 3:
                btn = "right"

            outfile.write("  sleep %f;\n" % tmicro)
            outfile.write("  bd \"%s\";\n" % btn)

        elif event.type == X.MotionNotify:
            lasttime = currtime
            print("MotionNotify", event.root_x, event.root_y)
            outfile.write("  mm %d %d %f;\n" % (event.root_x, event.root_y, tmicro))


# Check if the extension is present
if not record_dpy.has_extension("RECORD"):
    print("RECORD extension not found")
    sys.exit(1)
    r = record_dpy.record_get_version(0, 0)
    print("RECORD extension version %d.%d" % (r.major_version, r.minor_version))

# Create a recording context; we only want key and mouse events
ctx = record_dpy.record_create_context(
    0,
    [record.AllClients],
    [{
        'core_requests': (0, 0),
        'core_replies': (0, 0),
        'ext_requests': (0, 0, 0, 0),
        'ext_replies': (0, 0, 0, 0),
        'delivered_events': (0, 0),
        'device_events': (X.KeyPress, X.MotionNotify),
        'errors': (0, 0),
        'client_started': False,
        'client_died': False,
    }])


def do(playlist):
    global outfile
    global lasttime

    try:
        outfile = open(playlist, 'w+')

        outfile.write("playlist recording {\n")

        lasttime = datetime.now()

        # Enable the context; this only returns after a call to record_disable_context,
        # while calling the callback function in the meantime
        record_dpy.record_enable_context(ctx, record_callback)

        # Finally free the context
        record_dpy.record_free_context(ctx)

    except Exception as e:
        print("Error")
        print(type(e))
        print(e)

    finally:

        outfile.write("};\n\n")
        outfile.write("delay 0.025;\n\n")
        outfile.write("play recording;\n\n")
        outfile.close()

