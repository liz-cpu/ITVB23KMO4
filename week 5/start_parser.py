#!/usr/bin/env python3

import nltk

nltk.download('punkt')

"""
OPGAVE 1:   EEN CONTEXT -VRIJE GRAMMATICA
Een veel voorkomende taak bij de verwerking van natuurlijke taal is ontleding
(‘parsing’), het proces waarbij de structuur van een zin wordt bepaald. Dit kan
nuttig zijn om de computer te helpen de betekenis van een zin beter te
begrijpen; met name het bepalen van de zelfstandig naamwoorden helpt bij het
begrijpen waar de zin over gaat.

In deze opgave gaan we enkele Nederlandse zinnen ontleden op basis van een
(contextvrije) grammatica. Een formele grammatica is een verzameling
productieregels die aangeven hoe een symbool aan de linkerkant mag worden
vervangen door symbolen aan de rechterkant. Als S een zin representeert, dan
kunnen we herhaaldelijk productregels toepassen totdat een volledige zin van
eind-symbolen ontstaat.

De functie preprocess moet een zin als invoer accepteren en een lijst van
woorden met kleine letters teruggeven. Hiervoor moet de word_tokenize functie
uit nltk worden gebruikt. Elk woord dat niet minstens één alfabetisch teken
bevat moet worden uitgesloten van de lijst.

De functie np_chunk moet een parse-tree accepteren en een lijst teruggeven van
alle zinsdelen die als zelfstandig naamwoord functioneren (deze noemen we noun
phrases of NP’s). Een NP-chunk is een zinsdeel dat verder geen andere NP-chunks
bevat. Bijvoorbeeld "de stoel in het huis" is wel een NP, maar geen NP-chunk,
want "het huis" is ook een NP-chunk. Of “de markt voor Android applicaties” is
een NP die bestaat uit twee NP-chunks.
"""


def preprocess(sentence: str) -> list[str]:
    """
    Convert `sentence` to a list of its words. Pre-process sentence by
    converting all characters to lowercase and removing any word that does not
    contain at least one alphabetic character using nltk.word_tokenize().

    :param sentence: The sentence to be preprocessed.
    :type sentence: str
    :return: The preprocessed sentence.
    :rtype: list[str]
    """
    return [word.lower() for word in nltk.word_tokenize(sentence) if any(c.isalpha() for c in word)]


def np_chunk(tree: list) -> list:
    """
    Return a list of all noun phrase chunks in the sentence tree. A noun phrase
    chunk is defined as any subtree of the sentence whose label is "NP" that
    does not itself contain any other noun phrases as subtrees.

    :param tree: The tree to be chunked.
    :type tree: list
    :return: The chunks.
    :rtype: list
    """
    chunks = []

    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        if not any(t.label() == "NP" for t in subtree.subtrees()):
            chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    sentences = ["Jip roept moeder.",
                 "Jip en Janneke spelen in de slaapkamer.",
                 "Jip is nu heel voorzichtig.",
                 "Bijna valt Takkie overboord.",
                 "Takkie loopt weg, met zijn staart tussen zijn pootjes.",
                 "Er komt een grote rode brandweerauto voorbij.",
                 "Janneke komt terug met de keukentrap.",
                 "Hij heeft een slee gezien met twee jongetjes erop en twee hondjes ervoor.",
                 "De volgende morgen kijkt Jip uit het raam.",
                 "En als ze klaar zijn, wil Jip direct weer met de trein gaan spelen."]

    TERMINALS = """
    N -> "jip" | "moeder" | "janneke" | "slaapkamer" | "takkie" | "staart" | "pootjes" | "brandweerauto" | "keukentrap" | "hij" | "slee" | "jongetjes" | "hondjes" | "morgen" | "raam" | "ze" | "trein"
    V -> "roept" | "spelen" | "is" | "valt" | "loopt" | "komt" | "heeft" | "gezien" | "kijkt" | "wil" | "gaan" | "zijn"
    Con -> "en" | "als"
    Det -> "de" | "het" | "een" | "zijn" | "twee"
    P -> "in" | "tussen" | "met" | "uit"
    Adj -> "grote" | "rode" | "voorzichtig" | "volgende" | "klaar"
    Adv -> "heel" | "bijna" | "overboord" | "weg" | "voorbij" | "nu" | "er" | "terug"  | "erop" | "ervoor" | "morgen" | "direct" | "weer"
    """

    NONTERMINALS = """
    S -> NP VP | VP VP | Con S
    PP -> P NP
    VP -> V | VP PP | S V | VP V | V NP | V NP PP
    NP -> N | Adv NP | NP Con NP | Det Nom | NP Adv | Adv NP | Adj Nom | NP Adj | Adv
    Nom -> N | Adj Nom
    """

    # parse CFG from strings
    grammar = nltk.grammar.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)

    for s in sentences:
        print(s)

        tokens = preprocess(s)

        try:
            trees = list(parser.parse(tokens))
        except ValueError as e:
            print(e)
            continue
        if not trees:
            print("Could not parse sentence.")
            continue

        # print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()

            print("Noun Phrase Chunks")
            for np in np_chunk(tree):
                print(" ".join(np.flatten()))
