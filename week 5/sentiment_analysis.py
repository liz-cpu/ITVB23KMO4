#!/usr/bin/env python3

import colorama
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

colorama.init()
nltk.download('movie_reviews')

"""
OPGAVE 3:  SENTIMENT ANALYSE MET NAIVE BAYES
In deze opgave proberen we te voorspellen of een filmrecensie positief of
negatief is. Hiervoor gebruiken we de Naive Bayes model uit NLTK en een
verzameling documenten (corpus) uit NLTK met filmrecensies om de model te
trainen.

Op Blackboard is de file start_sentiment_analysis.py te vinden. Hier hoeft niet
veel meer aan worden toegevoegd. We moeten de model gaan trainen met de
training-set. Verder moeten getoond worden:
• de nauwkeurigheid van de model (nltk.classify.util.accuracy);
• de 20 meest informatieve woorden (features);
• voor elk van de 9 recensies of de recensie positief of negatief is,
    en met welke kans dit is.
"""

green, red, clear = colorama.Fore.GREEN, colorama.Fore.RED, colorama.Fore.RESET


def extract_features(word_list: list) -> dict[str, bool]:
    """
    Return the word features for all words in `word_list`.
    """
    return dict([(word, True) for word in word_list])


positive_fileids = movie_reviews.fileids('pos')
negative_fileids = movie_reviews.fileids('neg')

"""
Go through all 'positive files', extract the words and put them in a dict.

Example:
[
    ({
            'films': True,
            'adapted': True,
            'from': True,
            'comic': True,
            'books': True,
            'have': True
        },
        'Positive')
]
"""

pos = [(extract_features(movie_reviews.words(
    fileids=[f])), 'Positive') for f in positive_fileids]
neg = [(extract_features(movie_reviews.words(
    fileids=[f])), 'Negative') for f in negative_fileids]

print(f"Number of positive datapoints: {green}{len(pos)}{clear}")
print(f"Number of negative datapoints: {red}{len(neg)}{clear}")

print()

threshold_factor = 0.8
threshold_positive = int(threshold_factor * len(pos))
threshold_negative = int(threshold_factor * len(neg))

train = pos[:threshold_positive] + neg[:threshold_negative]
test = pos[threshold_positive:] + neg[threshold_negative:]

print(f"Number of training datapoints: {len(train)}")
print(f"Number of test datapoints: {len(test)}")

model = NaiveBayesClassifier.train(train)

print(f"Accuracy of the model: {nltk.classify.util.accuracy(model, test)}")

print()

print("Top 20 most informative words:")
model.show_most_informative_features(20)


input_reviews = [
    "Started off as the greatest series of all time, but had the worst ending of all time.",
    "Exquisite. 'Big Little Lies' takes us to an incredible journey with its emotional and intriguing storyline.",
    "I love Brooklyn 99 so much. It has the best crew ever!!",
    "The Big Bang Theory and to me it's one of the best written sitcoms currently on network TV.",
    "'Friends' is simply the best series ever aired. The acting is amazing.",
    "SUITS is smart, sassy, clever, sophisticated, timely and immensely entertaining!",
    "Cumberbatch is a fantastic choice for Sherlock Holmes-he is physically right (he fits the traditional reading of the character) and he is a damn good actor",
    "What sounds like a typical agent hunting serial killer, surprises with great characters, surprising turning points and amazing cast."
    "This is one of the most magical things I have ever had the fortune of viewing.",
    "I don't recommend watching this at all!"
]

print("Predictions: ")

print()
for review in input_reviews:
    probdist = model.prob_classify(extract_features(review.split()))
    pred_sentiment = probdist.max()
    confidence = round(probdist.prob(pred_sentiment), 2)

    color = colorama.Fore.GREEN if pred_sentiment == 'Positive' else colorama.Fore.RED
    conf = colorama.Fore.YELLOW if confidence < 0.6 else colorama.Fore.GREEN
    clear = colorama.Fore.RESET

    print(f"Review: {review}")
    print(f"Predicted sentiment: {color}{pred_sentiment}{clear}")
    print(f"Probability: {conf}{confidence}{clear}")
