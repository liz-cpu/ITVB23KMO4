from pprint import pprint
import json
import markovify

# read text from file
f = open('Nescio-de-Uitvreter.txt', 'r')
text = f.read()

# train and print model for n=2
text_model = markovify.Text(text, state_size=2)

# print possible next words for 'Gare' and 'du'
print(text_model.chain.model.__getitem__(('Gare', 'du')))

# generate 5 sentences, do not accept None
print("Sentences based on n=2:")
for i in range(1, 6):
    while True:
        sentence = text_model.make_sentence()
        if sentence is not None:
            print("Sentence", i, ":", sentence)
            break

# train and print model for n=3
text_model = markovify.Text(text, state_size=3)

# print possible next words for 'Japi', 'wist' and 'wel'
print(text_model.chain.model.__getitem__(('Japi', 'wist', 'wel')))

# generate sentences n=3
print("Sentences based on n=3:")
for i in range(1, 6):
    while True:
        sentence = text_model.make_sentence()
        if sentence is not None:
            print("Sentence", i, ":", sentence)
            break

