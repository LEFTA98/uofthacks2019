from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import json
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../auth.json"

client = language.LanguageServiceClient()

dict_auth = json.load(open("../dict_auth.json"))


def getLemma(word):
    if word is None:
        return None
    document = types.Document(
        content=word,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_syntax(document=document)

    return annotations.tokens[0].lemma


def analyze(sentence, allowed_actions=None):
    sentence = sentence.lower()

    document = types.Document(
        content=sentence,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_syntax(document=document)

    main_action = None

    tokens = annotations.tokens

    for token in tokens:

        if getLabel(token.dependency_edge) == "ROOT":
            main_action = token
            break

    if main_action is None:
        return Command(None)
    root = findTokenOfLabel(tokens, "ROOT")
    if root is not None:
        root = root.lemma
    pobj = findTokenOfLabel(tokens, "POBJ")
    if pobj is not None:
        pobj = pobj.lemma
    dobj = findTokenOfLabel(tokens, "DOBJ")
    if dobj is not None:
        dobj = dobj.lemma

    for allowed_root in allowed_actions:
        if getLemma(allowed_root) in getSynonyms(root):
            for allowed_pobj in allowed_actions[allowed_root]:
                if allowed_pobj is None or getLemma(allowed_pobj) in getSynonyms(pobj):
                    for allowed_dobj in allowed_actions[allowed_root][allowed_pobj]:
                        if getLemma(allowed_dobj) in getSynonyms(dobj):
                            return Command(allowed_root, allowed_pobj, allowed_dobj)
    return None


def getLabel(dependency_edge):
    split_tokens = str(dependency_edge).split()
    return split_tokens[split_tokens.index("label:")+1]


def findTokenOfLabel(tokens, label):
    for token in tokens:
        if getLabel(token.dependency_edge) == label:
            return token
    return None


def getSynonyms(word):
    results = json.loads(requests.request(method="GET",
                                          url="https://od-api.oxforddictionaries.com/api/v1/entries/en/{}/synonyms".format(
                                              word),
                                          headers=dict_auth).content)["results"][0]["lexicalEntries"][0]["entries"][0]["senses"]

    synonyms = sum([result["synonyms"] for result in results], [])

    synonyms = [word["text"]
                for word in synonyms if (len(word["text"].split()) == 1)]

    synonyms.insert(0, word)

    return synonyms


class Command():
    def __init__(self, root, dobj=None, pobj=None):
        self.root = root
        self.dobj = dobj
        self.pobj = pobj

    def __repr__(self):
        return "Command({}, {}, {})".format(self.root, self.dobj, self.pobj)


if __name__ == "__main__":
    x = analyze("Take the mushrooms", {
                "take": {None: {"armour", "mushrooms"}}})

    print(x)
