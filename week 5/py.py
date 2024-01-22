
with open("input.txt", "r") as f:
    w = f.readlines()

d = {}

for line in w:
    word, wtype = line.split()
    d[wtype] = d.get(wtype, []) + [word]

print(d)

for wtype in d:
    wordlist = d[wtype]
    wordlist = ["\""+word+"\"" for word in wordlist]
    print(f'{wtype} -> {" | ".join(wordlist)}')