a) Geen antwoord nodig.

b) Om de tijd te berekenen dat het model gemiddeld in de toestand 'stay' zit, is het nodig om eerst de steady-state vector te berekenen. Deze steady-state vector wordt ook wel geschreven als $\pi$. Deze vector is te berekenen door de volgende formule: $\pi = \pi P$. Hierbij is $\pi$ de steady-state vector en P de transitie matrix. In het geval van dit model is dit de volgende matrix:

$P = \begin{bmatrix} 0.2 & 0.2 & 0.2 & 0.2 & 0.2 \\ 0.1 & 0.9 & 0 & 0 & 0 \\ 0.1 & 0 & 0.9 & 0 & 0 \\ 0.1 & 0 & 0 & 0.9 & 0 \\ 0.1 & 0 & 0 & 0 & 0.9 \end{bmatrix}$

Voor de volgorde van de toestanden is gekozen voor de volgende volgorde:

$S = \begin{bmatrix} stay & left & right & up & down \end{bmatrix}$

Vervolgend moet de matrix $\pi$ berekend worden.

$\pi = \begin{bmatrix} \pi_{stay} & \pi_{left} & \pi_{right} & \pi_{up} & \pi_{down} \end{bmatrix} \begin{bmatrix} 0.2 & 0.2 & 0.2 & 0.2 & 0.2 \\ 0.1 & 0.9 & 0 & 0 & 0 \\ 0.1 & 0 & 0.9 & 0 & 0 \\ 0.1 & 0 & 0 & 0.9 & 0 \\ 0.1 & 0 & 0 & 0 & 0.9 \end{bmatrix}$

Deze vergelijking kan opgelost worden met behulp van eigenwaarden en eigenvectoren. Hiervoor is gebruik gemaakt van de Python library numpy met de functie `linalg.eig`. Hieruit volgen meerder eigenwaarden en eigenvectoren. De eigenwaarde die gebruikt moet worden is de eigenwaarde met de waarde 1. Deze eigenwaarde heeft de volgende genormaliseerde eigenvector:

$\pi = \begin{bmatrix} 0.11111111 & 0.22222222 & 0.22222222 & 0.22222222 & 0.22222222 \end{bmatrix}$

Deze vector geeft de kans weer dat het model in een bepaalde toestand zit. De kans dat het model in de toestand 'stay' zit is dus $0.11111111$. Dit betekent dat het model gemiddeld ongeveer $11.11\%$ van de tijd in de toestand 'stay' zit en ongeveer $22.22%$ van de tijd in de toestand 'left'. \
Dit is ook logisch te beredeneren. Als we 'stay' als de begin toestand gebruiken, dan is de kans dat het model in de toestand 'stay' blijft $0.2$. De kans dat het model naar een andere toestand gaat is $0.8$, welke in de volgende stap een kans van $0.1$ heeft om weer terug te gaan naar de toestand 'stay'. Dit doet terecht vermoeden dat de toestand 'stay' slechts de helft zo vaak voorkomt als ieder van de andere toestanden. Gezien de kans op de andere toestanden gelijk moet zijn, zal de kans op 'stay' dus $0.11111111$ zijn. Dit is immers de enige manier waarop de toestand 'stay' slechts de helft zo vaak voorkomt als ieder van de andere toestanden.

c) De robot staat reeds in de toestand 'stay' dus om deze precies 3 keer uit te voeren zal deze toestand hierna nog 2 keer moeten volgen. Dit leidt tot de volgende berekening: $1 \cdot 0.2 \cdot 0.2 = 0.04$

d) Elke move duurt 40 milliseconden. De kans Dat deze de eerstvolgende move niet meer 'stay' is, is $0.8$. In $20%$ van de gevallen is de toestand wederom 'stay', etcetera. Deze kansen vormen een geometrische reeks. De verwachte tijd dat het model in de toestand 'stay' zit is dus $0.2^0 \cdot 40 + 0.2^1 \cdot 40 + 0.2^2 \cdot 40 + \ldots + 0.2^{\infty} \cdot 40$. Dit kan herschreven worden naar een som van een geometrische reeks: $\sum_{i=0}^{\infty} 40 \cdot 0.2^i = 50$. Zo te zien convergeert deze reeks naar $50$. Dit betekent dat het model gemiddeld $50$ milliseconden in de toestand 'stay' zit. Deze berekening is tevens te herschrijven als $40 \cdot \frac{1}{1 - 0.2} = 50$.

e) Ik kom hier doormiddel van gewoonweg permutaties genereren op 8212.

f) Vanaf een toestand anders dan 'stay' is de branching factor $2$. Vanaf de toestand 'stay' is de branching factor $5$. De kans op toestand 'stay' is $0.11111111$. De kans op een andere toestand is $0.88888889$. De verwachte branching factor is dus $2 \cdot 0.88888889 + 5 \cdot 0.11111111 = 2.33333333$.

g) Hiervoor is er 3 maal de toestand 'up' nodig en 3 maal de toestand 'right'. De aantal unieke permutaties is dus $6! / (3! \cdot 3!) = 20$.

h) In het geval van ($x_1$, $y_1$) naar ($x_2$, $y_2$) kan van beide de delta berekend worden. vervolgen is het aantal paden te berekenen door de volgende formule: $aantal\_paden = \frac{(\Delta x + \Delta y)!}{\Delta x! \cdot \Delta y!}$. Dit is echter enkel mogelijk door de beperking dat de lengte van het pad gelijk is aan de Manhattan afstand.

i) $20%$, gezien dit niet aan een rand ligt en per sensor waarde evenredig 5 verschillende actuele waarden mogelijk zijn.

j) Het geïmplementeerde algoritme had het pad exact goed (0 fouten).

k) Dit is te zien in lijn 115 en 119 van `model.py`. Hier is te zien dat een `for` lus doorlopen wordt voor elke mogelijke toestand. Per toestand wordt vervolgens een `for` lus doorlopen om de huidige toestand aan te passen op basis van de vorige toestand.

l) Als je dit doet loop je het risico dat deze toestand cruciaal was voor het daadwerkelijke pad. Zolang de kans niet 0 is, is er een kans dat deze toestand onderdeel is van het pad. Het is dus niet verstandig om deze toestand te verwijderen.

m) Evenals bij vraag j is het pad exact goed (0 fouten).

n) Zoals uitgelegd in vraag j en m is het pad exact goed (0 fouten) bij het gebruik van het geïmplementeerde algoritme.

o) De comlpexiteit van het Viterbi algoritme is $O(n^2 \cdot m)$, waarbij $n$ het aantal toestanden is en $m$ het aantal observaties. Dijkstra's algoritme heeft een complexiteit van $O(n^2)$, waarbij $n$ het aantal knopen is.

p) Die zijn er zeker. Eén manier om dat te doen is door de kansen van `observation_model` welke uit komen op 0 te over te slaan. In plaats van voor elke toestand de kans te berekenen, kunnen ook enkel de toestanden berekend worden waarbij de kans niet 0 is vanuit het observatie model.