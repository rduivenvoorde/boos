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
        return (self._send_key('NEXT_TRACK'))

    def prev(self):
        # first time is seek to beginning
        self._send_key('PREV_TRACK')
        # second time is actual previous track...
        return (self._send_key('PREV_TRACK'))

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
                return True
        return False

    def vol(self, volume_0_100=None):
        path = '/volume'
        if volume_0_100 is None:
            r = requests.get(self.host+path)
            #print(r.text)
            doc = minidom.parseString(r.text)
            return doc.getElementsByTagName("actualvolume")[0].firstChild.data
        else:
            volume = '<volume>%s</volume>' % volume_0_100
            r = requests.post(self.host+path, volume)

    def preset(self, preset):
        # set preset
        key = 'PRESET_%s' % preset
        self._send_key(key)

    def presets(self):
        r = requests.get(self.host + '/presets')
        doc = minidom.parseString(r.text)
        items = {}
        for preset in doc.getElementsByTagName('presets')[0].childNodes:
            items[preset.getAttributeNode('id').value] = preset.getElementsByTagName('itemName')[0].childNodes[0].data
        return items

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
            return "STANDBY"
        else:
            # check if play status is STOP_STATE, meaning is paused
            if len(doc.getElementsByTagName("playStatus")) > 0:
                play_status = doc.getElementsByTagName("playStatus")[0].firstChild.data
                if play_status == "PAUSE_STATE" or play_status == "STOP_STATE":
                    return "PAUSED"
                else:
                    return source
            else:
                return source

    def now_playing(self):
        path = '/now_playing'
        r = requests.get(self.host+path)
        #print(r.text)
        doc = minidom.parseString(r.text)
        if doc.getElementsByTagName('artist')[0].childNodes and doc.getElementsByTagName('track')[0].childNodes:
            # spotify etc
            artist = doc.getElementsByTagName('artist')[0].childNodes[0].data
            track = doc.getElementsByTagName('track')[0].childNodes[0].data
            return "{artist} - {track}".format(artist=artist, track=track)
        elif doc.getElementsByTagName('stationName')[0].childNodes:
            station_name = doc.getElementsByTagName('stationName')[0].childNodes[0].data
            return "{}".format(station_name)
        else:
            return ''

    def _send_key(self, key):
        path = '/key'
        press = '<key state="press" sender="Gabbo">%s</key>' % key
        r = requests.post(self.host+path, press)
        #print(r.text)
        release = '<key state="release" sender="Gabbo">%s</key>' % key
        r = requests.post(self.host+path, release)
        #print(r.text)

    def name(self):
        info = self._info()
        return info.getElementsByTagName("name")[0].childNodes[0].data

    def _info(self):
        r = requests.get(self.host + '/info')
        #print(r.text)
        doc = minidom.parseString(r.text)
        return doc
