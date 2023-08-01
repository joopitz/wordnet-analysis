from typing import Optional, List
from urllib.parse import unquote
from nltk.corpus import wordnet as wn
import requests
from rdflib import Graph, Literal, URIRef


class CommonHelper:

    @classmethod    
    def get_attribute_in_rdf_graph(cls, graph: Graph, attribute: URIRef, lang: str = None) -> Optional[Literal]:        
        
        if lang:
            for _, predicate, obj in graph:
                if predicate == attribute and isinstance(obj, Literal) and obj.language == lang:
                    return obj
                
            for _, predicate, obj in graph:
                    if predicate == attribute:
                        return obj        
        return None
            
    @classmethod
    def get_rdf_graph(cls, url: str, accept_headers: List[str]) -> Optional[Graph]:        
        headers = {'Accept': ', '.join(accept_headers)}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content_type = response.headers.get('content-type').split(';')[0]
            if content_type in accept_headers:
                rdf_data = response.text
                try:
                    graph = Graph().parse(data=rdf_data, format=content_type)
                    return graph
                except Exception as e:
                    raise requests.RequestException(f"Failed to parse RDF data: {e}")

        return None

    @classmethod
    def getCountryCode(cls, lang):
        choices = {'fra': 'fr', 'spa': 'es', 'ita': 'it', 'nld': 'nl', 'por' : 'pt', 'ger': 'de', 'eng': 'en', 'fas': 'fa', 'jpn': 'ja', 'pol': 'pl', 'tha': 'th'}
        return choices.get(lang, 'en')

    @classmethod
    def getWordnetLanguageCode(cls, lang):
        choices = {'fr': 'fra', 'es': 'spa', 'it': 'ita', 'nl': 'nld', 'pt' : 'por', 'de': 'ger', 'en': 'eng'}
        return choices.get(lang, 'eng')    

    @classmethod
    def getWordnetLangDescription(cls, lang):
        choices = {'fra': 'french', 'spa': 'spanish', 'ita': 'italian', 'nld': 'dutch', 'por' : 'portuguese', 'ger': 'german', 'eng': 'english'}
        return choices.get(lang, 'english')
    
    @classmethod
    def getSpacyModelName(cls, lang):
        choices = {'de': 'de_core_news_lg'}
        return choices.get(lang, 'en_core_web_sm')

    @classmethod
    def getSpacyToWordnetPosMapping(cls, pos):
        choices = {'VERB': wn.VERB, 'NOUN': wn.NOUN,
                   'ADV': wn.ADV, 'ADJ': wn.ADJ}
        return choices.get(pos, 'x')

    @classmethod
    def getWordnetPosMapping(cls, pos):
        if pos.startswith('NN'):
            return wn.NOUN
        elif pos.startswith('VB'):
            return wn.VERB
        elif pos.startswith('JJ'):
            return wn.ADJ
        elif pos.startswith('RB'):
            return wn.ADV
        else:
            return 'x'

    @classmethod
    def sanatizeWord(cls, woi):
        result = unquote(woi)
        startsWithList = ["...", "'", '"', "n'", "l'", ",", ".", "!", "?", "¿", ";", "_", "-",
                          "`", "~", "<", ">", "%", "$", "#", "*", "(", ")", "+", "|", "@", "&", "^", "«", "»"]
        endsWithList = ["...", "'", '"', "'s", ",", ".", "!", "?", "¿", ";", "_", "-", "`",
                        "~", "<", ">", "%", "$", "#", "*", "(", ")", "+", "|", "@", "&", "^", "«", "»"]
        for s in startsWithList:
            if result.startswith(s):
                result = result[len(s):]
        for e in endsWithList:
            if result.endswith(e):
                result = result[:(len(e)*-1)]

        return result
