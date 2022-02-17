import json
manifest_urls = []
ids = open('vatican-ids.txt', 'r')
list = ids.readlines()


for elem in list:
    if list.count(elem) > 1:
        print(elem)

# with open('vatican-manifests.txt', 'w') as out:
#     json.dump(manifest_urls, out)
