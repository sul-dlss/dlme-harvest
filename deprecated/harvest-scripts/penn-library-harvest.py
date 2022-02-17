import urllib.request, os, io

ids = [189, 196, 235, 286, 293, 294, 295, 296, 299, 311, 312, 322, 37, 38, 387,
       388, 398, 399, 40, 400, 403, 404, 405, 407, 408, 409, 410, 412, 414, 417,
       425, 426, 427, 434, 435, 436, 441, 444, 447, 45, 455, 456, 459, 460, 464,
       467, 469, 486, 489, 49, 495]

for id in ids:
    url = "http://openn.library.upenn.edu/Data/0001/ljs{}/data/ljs{}_TEI.xml".format(id, id)
    print("Fetching {}".format(url))
    document = urllib.request.urlopen(url).read()

    filename = 'penn-output/schoenberg/data/schoenberg-{}.xml'.format(id)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as out_file:
        out_file.write(document.decode("utf-8"))
