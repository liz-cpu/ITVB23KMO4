#!/usr/bin/env python3

from pprint import pprint

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

> De key is een tuple van de woorden die de toestand van het model bepalen, in
> dit geval 2 woorden. De value is een dictionary met als key de volgende
> woorden en het aantal keer dat dit woord voorkomt na de toestand.

b) Gegeven de twee woorden of toestand ('Gare', 'du'), wat zijn mogelijke
    volgende woorden (toestanden), en met welke kansen (transition probabilities)?

> Door `print(text_model.chain.model.__getitem__(('Gare', 'du')))` uit te
> voeren is te zien welke woorden volgens het model een kans hebben om te volgen
> op de woorden 'Gare' en 'du'. De output is als volgt:

    {'Nord': 1, 'Midi': 1}

> Ook is dit terug te zien in de dictionary die gegenereerd wordt door
> markovify.Text, te lezen op regel 28600 in dict.txt (zie bijlage):
>   [
        "Gare",
        "du"
    ],
    {
        "Nord": 1,
        "Midi": 1
    }
> De kans dat deze woorden volgen is 1/2, omdat er 2 woorden zijn die kunnen
> volgen op de toestand ('Gare', 'du').

c) Gegeven de drie woorden ('Japi', 'wist', 'wel'), wat zijn mogelijke volgende
    woorden, en met welke kansen?

> Door `print(text_model.chain.model.__getitem__(('Japi', 'wist', 'wel')))` uit
> te voeren is te zien welke woorden volgens het model een kans hebben om te
> volgen op de woorden 'Japi', 'wist' en 'wel'. De output is als volgt:

    {'beter.': 1}

d) Genereer twee keer 5 willekeurige zinnen, waarbij (1) een Markov-toestand
    bestaat uit 2 woorden en (2) een toestand bestaat uit 3.

    Sentences based on n = 2:
    Sentence 1: Anders kon ik in mijn ledekant en sliep slecht, door de ijzige
        donkere ruimte, de nacht zou niet meer ophouden, de zon en had er geen
        weet van.
    Sentence 2: Een heelen zomer had Bavink ooit een woord gezegd als i klaar
        was hatti er geschreven, zei i, als i maar wat jaren.
    Sentence 3: Het bandje deed i er nog maar wat jaren.
    Sentence 4: De kachel was niet verwonderd.
    Sentence 5: Ze wisten er wat leven in Japi.

    Sentences based on n = 3:
    Sentence 1: Je kon toch de dingen niet en van jou niet.
    Sentence 2: Blijkbaar had i zich gemaakt.
    Sentence 3: Op en neer loopen van het Gare du Midi over de boulevards.
    Sentence 4: Den uitvreter, die je sigaren oprookte, en van je werk niet en
        van jou niet.
    Sentence 5: Blijkbaar had i zich gemaakt.

e) Kun je uitleggen hoe het genereren van zinnen werkt? Zie de source code van
    Markovify.

Twee funties van de Markovify library spelen een belangrijke rol bij het
genereren van zinnen. De eerste is `gen()` die een staat bij houd en deze elke
iteratie aanpast. De tweede is `move()` die de staat gebruikt om van de mogeijke
opvolgende woorden een willekeurige te kiezen.

def gen(self, init_state=None):
    state = init_state or (BEGIN,) * self.state_size
    while True:
        next_word = self.move(state)
        if next_word == END:
            break
        yield next_word
        state = tuple(state[1:]) + (next_word,)

def move(self, state):
    if self.compiled:
        choices, cumdist = self.model[state]
    elif state == tuple([BEGIN] * self.state_size):
        choices = self.begin_choices
        cumdist = self.begin_cumdist
    else:
        choices, weights = zip(*self.model[state].items())
        cumdist = list(accumulate(weights))
    r = random.random() * cumdist[-1]
    selection = choices[bisect.bisect(cumdist, r)]
    return selection

De `gen()` functie begint met een staat van BEGIN woorden. Vervolgens wordt er
een willekeurig woord gekozen uit de mogelijke opvolgende woorden van de staat.
Dit wordt herhaald tot er een END woord gekozen wordt. De `move()` functie kiest
een willekeurig woord uit de mogelijke opvolgende woorden van de staat op basis
van de kansverdeling van de woorden. De kansverdeling wordt bepaald door de
frequentie van de woorden in de tekst.

"""

# Read text from file
f = open('Nescio-de-Uitvreter.txt', 'r')
text = f.read()

# Train and print model for n = 2
text_model = markovify.Text(text, state_size=2)

print()

# Print possible next words for 'Gare' and 'du'
print(text_model.chain.model.__getitem__(('Gare', 'du')))

print()
# Generate 5 sentences, do not accept None
print("Sentences based on n = 2:")
for i in range(1, 6):
    while True:
        sentence = text_model.make_sentence()
        if sentence is not None:
            print(f"Sentence {i}: {sentence}")
            break

# Train and print model for n = 3
text_model = markovify.Text(text, state_size=3)

print()

# Print possible next words for 'Japi', 'wist' and 'wel'
print(text_model.chain.model.__getitem__(('Japi', 'wist', 'wel')))
# Needs to be under the n = 3 model, otherwise the key is too big. You could take
# the last 2 words of the key and use those to get the possible next words if
# you want to use the n = 2 model.

print()

# Generate sentences n = 3
print("Sentences based on n = 3:")
for i in range(1, 6):
    while True:
        sentence = text_model.make_sentence()
        if sentence is not None:
            print(f"Sentence {i}: {sentence}")
            break
