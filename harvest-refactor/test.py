import io, os, urllib.request

resumptionToken = 13897

while resumptionToken < 34812:
    try:
        url = "https://api.qdl.qa/oaipmh?verb=ListRecords&resumptionToken={}mods".format(resumptionToken)
        record = urllib.request.urlopen(url).read()
        filename = 'output/qnl/data/qnl-{}.xml'.format(resumptionToken + 1)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with io.open(filename, 'w') as f:
            f.write(record)
        resumptionToken += 1
    except:
        print("Error on {}".format(url))
        pass
