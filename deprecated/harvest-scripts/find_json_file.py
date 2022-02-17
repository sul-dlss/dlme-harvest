#!/usr/bin/python
import glob, json, io, os, requests, urllib

def main():
    directory = "/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/walters-art-museum-clean/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)
    for file in glob.glob("/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/walters-art-museum/data/*.json"):
        with open(file) as f:
            data = json.load(f)
            if data['ObjectNumber'] == 'W.590':
                print(file)

if __name__ == "__main__":
    main()
