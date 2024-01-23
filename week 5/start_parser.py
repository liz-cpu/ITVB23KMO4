import nltk
import sys

nltk.download('punkt')

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words. Pre-process sentence by converting all characters
    to lowercase and removing any word that does not contain at least one alphabetic character.
    """

    words = nltk.word_tokenize(sentence.lower())
    words = [word for word in words if any(c.isalpha() for c in word)]
    print(words)
    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree. A noun phrase chunk is defined
    as any subtree of the sentence whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    chunks = []

    # for each subtree in the tree
    for subtree in tree.subtrees():
        # if the subtree is a noun phrase and does not contain any other noun phrases
        if subtree.label() == "NP" and not list(subtree.subtrees(lambda t: t.label() == "NP" and t != subtree)):
            chunks.append(subtree)

    return chunks

def main():

    slist = [None for x in range(10)]
    slist[0] = "Jip roept moeder."
    slist[1] = "Jip en Janneke spelen in de slaapkamer."
    slist[2] = "Jip is nu heel voorzichtig."
    slist[3] = "Bijna valt Takkie overboord."
    slist[4] = "Takkie loopt weg, met zijn staart tussen zijn pootjes."
    slist[5] = "Er komt een grote rode brandweerauto voorbij."
    slist[6] = "Janneke komt terug met de keukentrap."
    slist[7] = "Hij heeft een slee gezien met twee jongetjes erop en twee hondjes ervoor."
    slist[8] = "De volgende morgen kijkt Jip uit het raam."
    slist[9] = "En als ze klaar zijn, wil Jip direct weer met de trein gaan spelen."

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
    grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)

    # nltk.ChartParser(grammar, trace=2) # debug
    # to show rules:
    # for p in grammar.productions():
    #    print(p).

    for i,s in enumerate(slist):
        print(s)

        s = preprocess(s)

        try:
            trees = list(parser.parse(s))
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
