#!/usr/bin/env python
import re
from pattern.web import Crawler


class Polly(Crawler): 
    def add(self, link):
        if not self.links:
            self.links = []
        # regex for crime log pages
        linkregex = re.compile("http://huntnewsnu.com/2013/([0-9]*)/crime-log-([a-z]*-[0-9]*)-([a-z]*-[0-9]*)")
        res = linkregex.search(link)
        if res:
            groups = res.groups()
            link = (link, groups[1], groups[2])
            print link
            self.links.append(link)
            with open("data.txt", 'a') as outfile:
                txt = ', '.join(link)
                outfile.write(txt + "\n")
            print "Link Added: ", link

    def visit(self, link, source=None):
        self.links = []
        print 'visited:', repr(link.url), 'from:', link.referrer
        self.add(link.url)

    def fail(self, link):
        print 'failed:', repr(link.url)

def get_crimelogs():
    crimelogsurl = "http://huntnewsnu.com/category/crime-log/"

    p = Polly(links=[crimelogsurl], domains=["huntnewsnu.com"], delay=5)
    while not p.done:
        p.crawl(method="DEPTH", cached=False, throttle=5)
