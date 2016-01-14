#!/usr/bin/env python3

import plac
from boos import Boos


@plac.annotations(
        command=("Commando", 'positional', None, str,
                 ['power', 'set', 'vol', 'mute', 'aux', 'next', 'prev', 'state', 'pause', 'play', 'volup', 'voldown',
                  'muted']),
        argument=("Optional command argument", 'positional', None, int, None, "n"))
def main(command='state', argument=-1):
    host = 'http://boos.fritz.box:8090'
    boos = Boos(host)
    if command == 'vol':
        # volume
        if argument < 0:
            boos.vol()
        else:
            boos.vol(argument)
    elif command == 'power':
        boos.power()
    elif command == 'next':
        boos.next()
    elif command == 'prev':
        boos.prev()
    elif command == 'mute':
        boos.mute()
    elif command == 'aux':
        boos.aux()
    elif command == 'state':
        boos.state()
    elif command == 'pause':
        boos.pause()
    elif command == 'play':
        boos.play()
    elif command == 'volup':
        boos.volup()
    elif command == 'voldown':
        boos.voldown()
    elif command == 'muted':
        boos.muted()
    elif command == 'set' and argument > 0:
        boos.preset(argument)
    else:
        print("NOT IMPLEMENTED")


if __name__ == '__main__':
    import plac

    plac.call(main)
