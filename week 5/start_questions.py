#!/usr/bin/env python3

import math
import os
import string

import nltk

"""
OPGAVE 4: VRAGEN BE ANTWOORD EN MET TF - IDF
Op Blackboard is de file corpus.zip te vinden. Bekijk eerst de files/documenten
in de corpus. Elk tekstbestand bevat de inhoud van een verhaaltje. Ons doel is
een programma te schrijven die uit deze bestanden zinnen kan vinden die relevant
zijn voor opgegeven zoektermen.

Het programma bestaat uit twee delen: het verwerken van documenten en het
ophalen van passende zinnen. Wanneer een vraag wordt gesteld dan zal het
programma eerst bepalen welke documenten het meest relevant zijn voor die vraag.
Wanneer de meest passende documenten zijn gevonden worden deze verdeeld in
zinnen, zodat de meest passende zin voor de vraag kan worden bepaald.
Om de meest relevante documenten te vinden gebruiken we tf-idf om documenten te
rangschikken op basis van de waarde van een woord in dat document. Het idee
hierbij is dat woorden die in weinig documenten voorkomen meer informatie
opleveren dan woorden die in veel documenten voorkomen.

Op Blackboard is de file start_questions.py te vinden. De drie functies main,
load_files en tokenize zijn al
gegeven. Maar drie functies compute_idfs, top_files en top_sentences moeten nog
gemaakt worden.

(1) De functie compute_idfs geeft voor elk woord dat in de corpus voorkomt de
idf-waarde. Stel dat de corpus 6 documenten bevat, en 2 daarvan bevatten het
woord ‘computer’, dan wordt de return waarde

word_idfs[‘computer’] = ln(6/2) = 1.0986.

(2) De functie top_files moet, gegeven een query, de inhoud van de files en de
idf-waarden van alle woorden in de corpus een lijst met de meest passende
filenamen terug geven. De lijst met filenamen heeft een lengte n en is
gesorteerd met de best passende eerst. Bestanden moeten worden gerangschikt
volgens de som van de tf-idf-waarden voor elk woord in de query dat ook in het
bestand voorkomt. Woorden in de zoekopdracht die niet in het bestand voorkomen,
mogen niet bijdragen aan de score van het bestand.

(3) De functie top_sentences moet, gegeven een query, de best passende zinnen
en de idf-waarden een lijst van best passende zinnen terug geven. De lijst van
zinnen moet worden gesorteerd met de beste overeenkomst eerst.

De zinnen moeten worden gerangschikt volgens de idf-score, dit is de som van de
idf-waarden voor elk woord in de query die ook in de zin voorkomen. Dus als
woorden A en B in de zin voorkomen, dan is de

idf-score =idf(A) + idf(B).

Naast idf-score moeten zinnen ook worden gesorteerd op Query term density (qtd).
Qtd wordt gedefinieerd als het aandeel van de woorden in de zin die ook woorden
in de query zijn. Bijvoorbeeld, als een zin 10 woorden bevat, waarvan er 3 in
de query voorkomen, dan is de qtd van deze zin 3/10
"""

nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def load_files(directory: str) -> dict[str, str]:
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.

    :param directory: The directory containing the files to load.
    :type directory: str
    :return: The mapping of filename to file contents.
    :rtype: dict[str, str]
    """

    file_dict = dict()

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, mode="r", encoding="utf8") as file:
                file_string = file.read()
                file_dict[filename] = file_string

    return file_dict


def tokenize(document: str) -> list[str]:
    """
    Given a string return a list of all of the words
    convert to lowercase and remove punctuation or stopwords

    :param document: The document to be tokenized.
    :type document: str
    :return: The tokens.
    :rtype: list[str]
    """

    cleaned_tokens = []

    tokens = nltk.tokenize.word_tokenize(document.lower())

    # Ensure all tokens are lowercase, non-stopwords, non-punctuation
    for token in tokens:
        # replace with 'english'?
        if token in nltk.corpus.stopwords.words('dutch'):
            continue
        else:
            all_punct = True
            for char in token:
                if char not in string.punctuation:
                    all_punct = False
                    break

            if not all_punct:
                cleaned_tokens.append(token)

    return cleaned_tokens


def compute_idfs(documents: dict[str, list[str]]) -> dict[str, float]:
    """
    Given a dictionary where key=filename or sentence and value=list of
    words/tokens, return a dictionary that maps words to their IDF-value.

    IDF-value = ln(number of documents / number of documents containing word)

    ln = math.log() without base (base = e)

    :example:
    documents = {'jip.txt': ['jip', 'en', 'janneke', 'lopen', 'samen', 'naar', 'school']}
    Suppose corpus has 2 docs and 1 doc contains the word 'jip' then word_idfs["school"] = ln(1/2) = 0.693

    example:
    documents = {'Jip en Janneke lopen samen naar school.': ['jip', 'en', 'janneke', 'lopen', 'samen', 'naar', 'school']}
    Suppose corpus has 6 docs and 2 docs contain the word 'keuken' then word_idfs["keuken"] = ln(6/2) = 1.0986


    :param documents: The documents to compute the IDF-values for.
    :type documents: dict[str, list[str]]
    :return: The IDF-values.
    :rtype: dict[str, float]
    """

    num_docs = len(documents)
    count_docs_have_word = dict()
    word_idfs = dict()

    for doc in documents:
        for word in documents[doc]:
            count_docs_have_word[word] = count_docs_have_word.get(word, 0) + 1

    for word in count_docs_have_word:
        word_idfs[word] = math.log(num_docs / count_docs_have_word[word])
    return word_idfs


def top_files(query: set[str], files: dict[str, list[str]], idfs: dict[str, float], n: int) -> list[str]:
    """
    Given a query, the contents of the files, the IDF-values and the number of
    files to return, return a list of the n top files that match the query.

    The list of filenames should be sorted with the best match first.

    :param query: The query.
    :type query: set[str]
    :param files: The files to find matches in.
    :type files: dict[str, list[str]]
    :param idfs: The IDF-values.
    :type idfs: dict[str, float]
    :param n: The number of files to return.
    :type n: int
    :return: The filenames of the top n matches.
    :rtype: list[str]
    """
    n = 1 if n < 1 else n

    file_scores = {filename: 0 for filename in files}

    for filename in files:
        for word in query:
            if word in files[filename]:
                file_scores[filename] += idfs[word]

    # sorted(__iterable__: Iterable[_T], *, key: Optional[Callable[[_T], Any]], reverse: bool)
    sorted_files = sorted([filename for filename in files],
                          key=lambda x: file_scores[x], reverse=True)

    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """	
    Given a query, the contents of the files, the IDF-values and the number of
    sentences to return, return a list of the n top sentences that match the
    query.

    The list of sentences should be sorted with the best match first.

    :param query: The query.
    :type query: set[str]
    :param sentences: The sentences to find matches in.
    :type sentences: dict[str, list[str]]
    :param idfs: The IDF-values.
    :type idfs: dict[str, float]
    :param n: The number of sentences to return.
    :type n: int
    :return: The sentences of the top n matches.
    :rtype: list[str]
    """

    sentence_score = {sentence: {'idf_score': 0, 'length': 0,
                                 'query_words': 0, 'qtd_score': 0} for sentence in sentences}

    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                sentence_score[sentence]['idf_score'] += idfs[word]
                sentence_score[sentence]['query_words'] += 1

        sentence_score[sentence]['length'] = len(sentences[sentence])

        sentence_score[sentence]['qtd_score'] = sentence_score[sentence]['query_words'] / \
            sentence_score[sentence]['length']

    # example: Query: jip
    # sentence_score:
    # {'Jip en Janneke lopen samen naar school.': {'idf_score': 0.693, 'length': 8, 'query_words': 1, 'qtd_score': 0.125},
    #  'Takkie mag ook mee.': {'idf_score': 0, 'length': 5, 'query_words': 0, 'qtd_score': 0.0}}

    sorted_sentences = sorted([sentence for sentence in sentences], key=lambda x: (
        sentence_score[x]['idf_score'], sentence_score[x]['qtd_score']), reverse=True)

    return sorted_sentences[:n]


def google():
    files = load_files("corpus")
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }

    # calculate IDF values across files
    file_idfs = compute_idfs(file_words)

    # prompt user for query, ex. Query: blussen ladder
    query = set(tokenize(input("Query: ")))

    # determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # extract sentences from n top file(s)
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


if __name__ == "__main__":
    for i in range(1, 6):
        print(f"Question {i}:")
        google()
        print()
