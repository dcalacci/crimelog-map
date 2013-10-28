#!/usr/bin/env python
import re, cPickle
class Text:
    def __init__(self, sen=""):
        self.orig_text = sen
        self.text = self.__prep_text(self.orig_text)
        self.entities = self.get_entities()
        self.wordcount = len(self.orig_text)

    def get_entities(self):
        """
        Generates the collections of entities for this sentence.
        populates 'self.original_entities' with the output from
        the stanford ner server. This dictionary is of the form:
        TYPE -> [Listof Entities]
        Also returns a list of all the entities stanford NER recognizes
        in this sentence, as a list of strings.

        @rtype:  list of strings
        @return: A list of entities that exist in this sentence.
        """
        import ner
        tagger = ner.SocketNER(host='localhost', port=8080)
        orig_ents = tagger.get_entities(self.orig_text)

        for key, val in orig_ents.items():
            orig_ents[key] = map(lambda s: self.__prep_text(s), val)
        self.original_entities = orig_ents

        # just a simple list of all the entities
        entities = [v[0] for k, v in orig_ents.items()]
        return entities

    def __parse_entities(self, txt, entities):
        """
        produces a list representation of the given text with each entity
        as its' own list element. Example:
        'i hate northesatern university, but i like john adams'
        ->
        ['i', 'hate', 'northeastern university', 'but', 'i', 'like', 'john adams']
        this will apply this transformation to multiple references to the same 
        entity, as well.

        @type  txt: list of strings
        @param txt: A list representation of the string to examine
        @type  entities: list of strings
        @param entities: A list of entities to check

        @rtype: list of string
        @return: a list representation of a sentence
        """
        # if we're done going through the list of entities,
        # just return the sentence array.
        if not entities:
            return txt.split()
        
        entity = entities[0]
        # if it's not in the list, go to the next entity.
        if txt.find(entity) == -1:
            return self.__parse_entities(txt, entities[1:])

        beg_index = txt.find(entity)
        end_index = txt.find(entity) + len(entity)

        a = txt[:beg_index] # string up to the entity
        b = txt[end_index:] # string after the entity

        a = self.__parse_entities(a, entities)
        a.append(entity) # add the entity inbetween the two parts
        b = self.__parse_entities(b, entities)

        return a + b

    def parse_sentence_with_entities(self, entities):
        "initial call to __parse_entities"
        return self.__parse_entities(self.text, self.entities)


from pattern.web import Crawler
class Polly(Crawler): 
    def add(self, link):
        if not self.links:
            self.links = []
        # regex for crime log pages
        linkregex = re.compile("http://huntnewsnu.com/2013/([0-9]*)/crime-log-([a-z]*)-([0-9]*)-.*-([0-9]*)")
        res = linkregex.search(link)
        if res:
            groups = res.groups()
            link = (link, groups[0], groups[2], groups[3])
            self.links.append(link)
            print "Link Added: ", link

    def visit(self, link, source=None):
        self.links = []
        print 'visited:', repr(link.url), 'from:', link.referrer
        self.add(link.url)

    def fail(self, link):
        print 'failed:', repr(link.url)

crimelogsurl = "http://huntnewsnu.com/category/crime-log/"

p = Polly(links=[crimelogsurl], domains=["huntnewsnu.com"], delay=5)
while not p.done:
    p.crawl(method="DEPTH", cached=False, throttle=5)
cPickle.dump(p.links, open('links.p', 'wb'))


# def get_crimelogs():
#     from pattern.web import Crawler

#     crimelogsurl = "http://huntnewsnu.com/category/crime-log/"

#     crawler = Crawler(links=[crimelogsurl], 
#                       domains=['huntnewsnu.com'], 
#                       delay=10.0, 
#                       parser=HTMLLinkParser().parse)

#     while not crawler.done:
#         crawler.crawl(method=DEPTH)
