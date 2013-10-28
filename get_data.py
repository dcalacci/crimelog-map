#!/usr/bin/env python

def get_urls_from_datafile(filepath):
    "list of [url, start-date, end-date]"
    urls = []
    with open(filepath) as data:
        for line in data:
            line = line.strip().replace(" ", "").split(',')
            urls.append(line)
    return urls

def get_html(datafile, folder):
    "stores the html for all the urls in datafile in folder."
    from pattern.web import download
    urls = get_urls_from_datafile(datafile)
    for url in urls:
        filename = url[1] + ":" + url[2] + ".html"
        with open(folder+filename, 'w') as outfile:
            outfile.write(download(url[0], cached=False))

# def get_text(html):
#     "extracts the text from the crimelog for some html file"
