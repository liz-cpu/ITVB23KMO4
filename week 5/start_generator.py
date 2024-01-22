from pprint import pprint
import json
import markovify
"""
OPGAVE 2:  WAT IS HET  VOLGENDE WOORD ?
In deze opgave gebruiken we de klassieke roman "de Uitvreter" van Nescio
(Nescio-de-Uitvreter.txt). De vraag hierbij is: gegeven een n aantal worden,
wat is de kans op het volgende word n+1, en met welke kansen? Dit  kunnen we 
beantwoorden door een Markov model te trainen. Hiervoor gebruiken we Markovify
library. Zie  https://github.com/jsvine/markovify.

a) De functie markovify.Text genereerd een Markov model. Leg uit wat de key en
    value zijn van deze dictionary.

> De key is een tuple van de woorden die de toestand van het model bepalen.
> De value is een dictionary met als key de volgende woorden en als value de
    kans dat dit woord volgt op de toestand.
> Bijvoorbeeld van regel 17 in dict.txt (zie bijlage):
> '"Dat": 15,
                "Af": 3,
                "Hij": 50,
                "Aan": 2,
                "Het": 13,
                "Alleen": 1, '
> Hier is de key Dat, en de value is een dictionary met als key de volgende
> woorden en als value de kans dat dit woord volgt op de toestand.
> Dus de kans dat het woord 'Dat' gevolgd wordt door 'Hij' is 50, de kans dat
> het woord 'Dat' gevolgd wordt door 'Af' is 3, etc.

b) Gegeven de twee woorden of toestand ('Gare', 'du'), wat zijn mogelijke
    volgende woorden (toestanden), en met welke kansen (transition probabilities)?

> De mogelijke volgende woorden zijn 'Nord' en 'Midi', met respectievelijk
> kansen van 1 voor beide.

c) Gegeven de drie woorden ('Japi', 'wist', 'wel'), wat zijn mogelijke volgende
    woorden, en met welke kansen?

> De mogelijke volgende woorden zijn 'beter' en 'dat', met respectievelijk
> kansen van 1 voor beide.

d) Genereer twee keer 5 willekeurige zinnen, waarbij (1) een Markov-toestand
    bestaat uit 2 woorden en (2) een toestand bestaat uit 3.


e) Kun je uitleggen hoe het genereren van zinnen werkt? Zie de source code van Markovify.


"""


# read text from file
f = open('Nescio-de-Uitvreter.txt', 'r')
text = f.read()

# train and print model for n=2
text_model = markovify.Text(text, state_size=2)

# generate some sentences
pprint(text_model.to_dict())

# train and print model for n=3
text_model = markovify.Text(text, state_size=3)
pprint(text_model.to_dict())

# generate sentences n=3
for i in range(5):
    print(text_model.make_sentence())
