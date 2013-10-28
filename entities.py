#!/usr/bin/env python

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
