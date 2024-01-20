import nltk


def preprocess(sentence: str) -> list[str]:
    """
    Convert `sentence` to a list of its words. Pre-process sentence by converting all characters
    to lowercase and removing any word that does not contain at least one alphabetic character.
    """
    return [word.lower() for word in nltk.word_tokenize(sentence) if any(c.isalpha() for c in word)]


def np_chunk(tree: list) -> list:
    """
    Return a list of all noun phrase chunks in the sentence tree. A noun phrase chunk is defined
    as any subtree of the sentence whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        if not any(t.label() == "NP" for t in subtree.subtrees()):
            chunks.append(subtree)

    return chunks


def main(none: None = None) -> None:
    slist = [
        "Jip roept moeder.",
        "Jip en Janneke spelen in de slaapkamer.",
        "Jip is nu heel voorzichtig.",
        "Bijna valt Takkie overboord.",
        "Takkie loopt weg, met zijn staart tussen zijn pootjes.",
        "Er komt een grote rode brandweerauto voorbij.",
        "Janneke komt terug met de keukentrap.",
        "Hij heeft een slee gezien met twee jongetjes erop en twee hondjes ervoor.",
        "De volgende morgen kijkt Jip uit het raam.",
        "En als ze klaar zijn, wil Jip direct weer met de trein gaan spelen."
    ]

    TERMINALS = """
    N -> "jip" | "moeder" | "janneke" | "spelen" | "in" | "de" | "slaapkamer" | "is" | "nu"
    V -> "roept" | "spelen" | "zien" | "loopt" | "weg" | "komt" | "terug" | "kijkt" | "wil" | "gaan"
    P -> "met" | "in" | "over" | "op" | "voorbij" | "uit" | "naar"
    Adj -> "grote" | "rode" | "direct"
    Adv -> "nu" | "heel" | "weer"
    Det -> "de" | "een" | "zijn" | "twee" | "erop" | "ervoor" | "de" | "een" | "de" | "de" | "de" | "de"
    Con -> "en" | "met" | "en" | "als" | "en"
    """

    NONTERMINALS = """
    S -> NP VP
    VP -> V | V NP | VP P | VP Adv
    NP -> N | Det NP | NP Con NP | Adj NP
    """

    # parse CFG from strings
    grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)

    for s in slist:
        print(s)

        tokens = preprocess(s)

        try:
            trees = list(parser.parse(tokens))
        except ValueError as e:
            print(e)
            return
        if not trees:
            print("Could not parse sentence.")
            return

        # print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()

            print("Noun Phrase Chunks")
            for np in np_chunk(tree):
                print(" ".join(np.flatten()))


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
