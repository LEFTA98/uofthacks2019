from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../auth.json"

def analyze(sentence, verbs=None):
    client = language.LanguageServiceClient()

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
        # Say I don't know what you mean or smth
        pass

    root = findTokenOfLabel(tokens, "ROOT")
    if root is not None:
        root = root.lemma
    pobj = findTokenOfLabel(tokens, "POBJ")
    if pobj is not None:
        pobj = pobj.lemma
    dobj = findTokenOfLabel(tokens, "DOBJ")
    if dobj is not None:
        dobj = dobj.lemma

    return Command(root, pobj, dobj)


def getLabel(dependency_edge):
    split_tokens = str(dependency_edge).split()
    return split_tokens[split_tokens.index("label:")+1]


def findTokenOfLabel(tokens, label):
    for token in tokens:
        if getLabel(token.dependency_edge) == label:
            return token
    return None


class Command():
    def __init__(self, root, dobj=None, pobj=None):
        self.root = root
        self.dobj = dobj
        self.pobj = pobj

    def __repr__(self):
        return "Command({}, {}, {})".format(self.root, self.dobj, self.pobj)

x = analyze("Google, headquartered in Mountain View, unveiled the new Android phone at the Consumer Electronic Show.  Sundar Pichai said in his keynote that users love their new Android phones.")
x = analyze("The Blue chicken is furiously eating lasagna with a fork")

print(x)
