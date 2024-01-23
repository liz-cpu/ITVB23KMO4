### a) De functie markovify.Text genereerd een Markov model. Leg uit wat de key en value zijn van deze dictionary.

De key is een tuple van woorden, in dit geval 2 woorden, de value is een dictionary met daarin de volgende woorden en het aantal keer dat deze voorkomen na de key.

### b) Gegeven de twee woorden of toestand ('Gare', 'du'), wat zijn mogelijke volgende woorden (toestanden), en met welke kansen (transition probabilities)?

Door `print(text_model.chain.model.__getitem__(('Gare', 'du')))` uit te voeren is te zien welke woorden volgens het model een kans hebben om te volgen op de woorden 'Gare' en 'du'. De output is als volgt:

```python
{'Nord': 1, 'Midi': 1}
```

De kans dat 'Nord' volgt op 'Gare' en 'du' is $\frac{1}{2}$, de kans dat 'Midi' volgt op 'Gare' en 'du' is ook $\frac{1}{2}$.

### c) Gegeven de drie woorden ('Japi', 'wist', 'wel'), wat zijn mogelijke volgende woorden, en met welke kansen?

Door `print(text_model.chain.model.__getitem__(('Japi', 'wist', 'wel')))` uit te voeren is te zien welke woorden volgens het model een kans hebben om te volgen op de woorden 'Japi', 'wist' en 'wel'. De output is als volgt:

```python
{'beter.': 1}
```

De kans dat 'beter.' volgt op 'Japi', 'wist' en 'wel' is $1$.
### d) Genereer twee keer 5 willekeurige zinnen, waarbij (1) een Markov-toestand bestaat uit 2 woorden en (2) een toestand bestaat uit 3.

De code die hiervoor gebruikt is staat in `start_generator.py`. De output is als volgt:
```
Sentences based on n=2:
Sentence 1 : Socialist had i haar met den trein laten vallen.
Sentence 2 : Z'n kantoor vrat i uit; iederen laatsten van de kou, werd je nat en beroerd of moe.
Sentence 3 : Te sappel had i de boeken van Appi, z'n jasje legde i de laatste drie, vier jaar.
Sentence 4 : Blijkbaar had i haar met den kolonel op het terras van een werkman uit een glasfabriek.
Sentence 5 : In zijn jongen tijd was i in de duisternis, de ijzige donkere ruimte, de nacht zou niet meer ophouden, de zon er al in en stroomde het water spatte en plenste over de meiden, met een borreltje kwam er al mee aanzetten.

Sentences based on n=3:
Sentence 1 : De ouwe boekhouder wist al heel gauw erger dan schraal bij kas.
Sentence 2 : Op en neer loopen van het Gare du Midi over de boulevards.
Sentence 3 : Blijkbaar had i zich al dien tijd zou hij dood zijn.
Sentence 4 : Japi zat op z'n bankje, hield z'n pet vast met z'n rechterhand, z'n rechterarm steunde op de verschansing.
Sentence 5 : Je kon toch de dingen niet en van je werk niet en van je werk niet en van jou niet.
```


### e) Kun je uitleggen hoe het genereren van zinnen werkt? Zie de source code van Markovify.

Twee funties van de Markovify library spelen een belangrijke rol bij het genereren van zinnen. De eerste is `gen()` die een staat bij houd en deze elke iteratie aanpast. De tweede is `move()` die de staat gebruikt om van de mogeijke opvolgende woorden een willekeurige te kiezen.

```python
    def gen(self, init_state=None):
        """
        Starting either with a naive BEGIN state, or the provided `init_state`
        (as a tuple), return a generator that will yield successive items
        until the chain reaches the END state.
        """
        state = init_state or (BEGIN,) * self.state_size
        while True:
            next_word = self.move(state)
            if next_word == END:
                break
            yield next_word
            state = tuple(state[1:]) + (next_word,)
```

```python

    def move(self, state):
        """
        Given a state, choose the next item at random.
        """
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
```

De `gen()` functie begint met een staat van BEGIN woorden. Vervolgens wordt er een willekeurig woord gekozen uit de mogelijke opvolgende woorden van de staat. Dit wordt herhaald tot er een END woord gekozen wordt. De `move()` functie kiest een willekeurig woord uit de mogelijke opvolgende woorden van de staat op basis van de kansverdeling van de woorden. De kansverdeling wordt bepaald door de frequentie van de woorden in de tekst.