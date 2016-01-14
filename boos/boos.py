#!/usr/bin/env python3

import requests
from xml.dom import minidom


class Boos:

    def __init__(self, host):
        self.host = host

    def power(self):
        self._send_key('POWER')

    def pause(self):
        self._send_key('PAUSE')

    def play(self):
        self._send_key('PLAY')

    def next(self):
        print(self._send_key('NEXT_TRACK'))

    def prev(self):
        # first time is seek to beginning
        print(self._send_key('PREV_TRACK'))
        # second time is actual previous track...
        print(self._send_key('PREV_TRACK'))

    def mute(self):
        self._send_key('MUTE')

    def aux(self):
        self._send_key('AUX_INPUT')

    def volup(self):
        self.vol(int(self.vol())+5)

    def voldown(self):
        self.vol(int(self.vol())-5)

    def muted(self):
        path = '/volume'
        r = requests.get(self.host+path)
        doc = minidom.parseString(r.text)
        if len(doc.getElementsByTagName("muteenabled"))>0:
            muted = doc.getElementsByTagName("muteenabled")[0].firstChild.data
            if muted == 'true':
                print('True')
                return True
        print('False')
        return False

    def vol(self, volume_0_100=None):
        path = '/volume'
        if volume_0_100 is None:
            r = requests.get(self.host+path)
            #print(r.text)
            doc = minidom.parseString(r.text)
            print(doc.getElementsByTagName("actualvolume")[0].firstChild.data)
            return doc.getElementsByTagName("actualvolume")[0].firstChild.data
        else:
            volume = '<volume>%s</volume>' % volume_0_100
            r = requests.post(self.host+path, volume)

    def preset(self, preset):
        # set preset
        key = 'PRESET_%s' % preset
        self._send_key(key)

    def state(self):
        # ContentItem source="INTERNET_RADIO"
        # <ContentItem source="STANDBY" isPresetable="true"/> == OFF/STANDBY
        # <playStatus>STOP_STATE</playStatus>  == PAUSE
        path = '/now_playing'
        r = requests.get(self.host+path)
        #print(r.text)
        doc = minidom.parseString(r.text)
        source = doc.getElementsByTagName("ContentItem")[0].attributes["source"].value
        if source == "STANDBY":
            print(source)
            return "STANDBY"
        else:
            # check if play status is STOP_STATE, meaning is paused
            play_status = doc.getElementsByTagName("playStatus")[0].firstChild.data
            if play_status == "PAUSE_STATE" or play_status == "STOP_STATE":
                print("PAUSED")
                return "PAUSED"
            else:
                print(source)
                return source

    def _send_key(self, key):
        path = '/key'
        press = '<key state="press" sender="Gabbo">%s</key>' % key
        r = requests.post(self.host+path, press)
        #print(r.text)
        release = '<key state="release" sender="Gabbo">%s</key>' % key
        r = requests.post(self.host+path, release)
        #print(r.text)