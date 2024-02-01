import nltk


def preprocess(sentence: str) -> list[str]:
    """
    Convert `sentence` to a list of its words. Pre-process sentence by converting all characters
    to lowercase and removing any word that does not contain at least one alphabetic character using
    nltk.word_tokenize().

    :param sentence: The sentence to be preprocessed.
    :type sentence: str
    :return: The preprocessed sentence.
    :rtype: list[str]
    """
    return [word.lower() for word in nltk.word_tokenize(sentence) if any(c.isalpha() for c in word)]

def np_chunk(tree: list) -> list:
    """
    Return a list of all noun phrase chunks in the sentence tree. A noun phrase chunk is defined
    as any subtree of the sentence whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

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
