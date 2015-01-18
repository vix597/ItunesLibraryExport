'''
Itunes exported library XML parser
'''

import xml.etree.ElementTree as ET

class ItunesTrack:
    def __init__(
        self,
        name,
        artist,
        album,
        location
    ):
        self.name = name
        self.artist = artist
        self.album = album
        self.location = location

    def __str__(self):
        return ''.join((
            "Name: ",self.name,"\n",
            "Artist: ",self.artist,"\n",
            "Album: ",self.album,"\n",
            "Location: ",self.location,"\n"
        ))

    @classmethod
    def from_element(cls,element):
        name = None
        artist = None
        album = None
        location = None

        for i in range(len(element)):
            child = element[i]
            i += 1
            if child.text == "Name":
                name = element[i].text
            elif child.text == "Artist":
                artist = element[i].text
            elif child.text == "Album":
                album = element[i].text
            elif child.text == "Location":
                location = element[i].text

        return ItunesTrack(
            name,
            artist,
            album,
            location
        )

class ItunesLibraryXmlParser:
    def __init__(self, LibraryXmlFile):
        self.xml_file = LibraryXmlFile
        self.tree = None
        self.root = None
        self.track_count = None
        self.tracks = []

    def parse(self):
        self.tree = ET.parse(self.xml_file)
        self.root = self.tree.getroot()

        '''
        Find the index of the 'Tracks' tag
        '''
        i = 0
        tracks_dict_index = 0
        for child in self.root[0]:
            if child.text == "Tracks":
                tracks_dict_index = i+1 #It'll be the index of the tag after "Tracks"
                break
            i += 1

        for track in self.root[0][tracks_dict_index].findall('dict'):
            self.tracks.append(ItunesTrack.from_element(track))



