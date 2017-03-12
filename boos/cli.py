#!/usr/bin/env python3

import plac
from boos import Boos


@plac.annotations(
        command=("Commando", 'positional', None, str,
                 ['name', 'power', 'set', 'vol', 'mute', 'aux', 'next', 'prev', 'state', 'pause', 'play', 'volup', 'voldown',
                  'muted']),
        argument=("Optional command argument", 'positional', None, int, None, "n"))
def main(command='state', argument=-1):
    host = 'http://boos.fritz.box:8090'
    boos = Boos(host)
    if command == 'vol':
        # volume
        if argument < 0:
            if boos.muted():
                print('{} - (MUTED)'.format(boos.vol()))
            else:
                print(boos.vol())
        else:
            boos.vol(argument)
    elif command == 'power':
        boos.power()
    elif command == 'next':
        boos.next()
    elif command == 'prev':
        boos.prev()
    elif command == 'mute':
        # first print new state (that is why if muted we print Unmuted)
        if boos.muted():
            print('Unmuted')
        else:
            print('Muted')
        boos.mute()
    elif command == 'aux':
        boos.aux()
    elif command == 'name':
        print(boos.name())
    elif command == 'state':
        print(boos.state())
        print(boos.now_playing())
    elif command == 'pause':
        boos.pause()
    elif command == 'play':
        boos.play()
    elif command == 'volup':
        boos.volup()
        print(boos.vol())
    elif command == 'voldown':
        boos.voldown()
        print(boos.vol())
    elif command == 'muted':
        print(boos.muted())
    elif command == 'set':
        if argument > 0:
            boos.preset(argument)
        else:
            for n in range(1, 7):
                print('{}: {}'.format(n, boos.presets()[str(n)]))
    else:
        print("NOT IMPLEMENTED")


if __name__ == '__main__':
    import plac

    plac.call(main)
