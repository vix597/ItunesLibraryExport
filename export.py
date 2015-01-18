from libraryxmlparser import ItunesLibraryXmlParser
import argparse
import sys
import os
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Itunes Library export from XML")
    parser.add_argument("-x","--xml",help="Input xml",type=str)
    parser.add_argument("-o","--out",help="Output root director for music",type=str)
    args = parser.parse_args()

    xml = args.xml
    out = args.out

    if not xml or not out:
        print("Error: Please provide an input XML file to parse and an output root directory for the export")
        exit(1)

    itunes_xml_parser = ItunesLibraryXmlParser(xml)
    itunes_xml_parser.parse()

    tot_tracks = len(itunes_xml_parser.tracks)
    complete = 0

    if not os.path.exists(out):
        os.mkdir(out)

    try:
        for track in itunes_xml_parser.tracks:
            print(complete,"/",tot_tracks," complete...")
            try:
                cur_path = os.path.join(out,track.artist)
                if not os.path.exists(cur_path):
                    os.mkdir(cur_path)
        
                cur_path = os.path.join(cur_path,track.album)
                if not os.path.exists(cur_path):
                    os.mkdir(cur_path)

                check_path = os.path.join(cur_path,os.path.basename(track.location))
                if os.path.isfile(check_path):
                    print("File copied already")
                else:
                    shutil.copy(track.location,cur_path)
            except Exception as e:
                with open("errors.txt",'a') as f:
                    f.write("Exception copying "+track.name+": "+str(e)+"\n")
                print("Current track failed. See errors.txt")
            finally:
                complete += 1
    except KeyboardInterrupt:
        print("cntr-c, exiting...")
        exit(0)

    print("Operation completed successully")
