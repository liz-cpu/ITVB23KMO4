objects = "FGCW"
start = "FGCW|"
invCombs = ["GC", "GW"]
captains = 'F'
boatLoc = '<'
steps = []

# state, invalid combinations, begin, boat location, captains
def step(s, ic, b, bl, caps):
    if s.find('|') == 0:
        print("-------------------------------complete")
        return s, ic, b
    # check if current state is invalid or not
    i = 0
    while i < len(ic) and s is not b:
        if (ic[i][0] in s[0: s.find('|')] and ic[i][1] in s[0: s.find('|')]) \
                or (ic[i][0] in s[s.find('|') + 1: len(s)] and ic[i][1] in s[s.find('|') + 1: len(s)])\
                or len(steps) > len(b)**2:
            print(s + " -------invalid comb-------")
            if len(steps) > 0:
                steps.pop()
            return False
        i += 1
    caplocs = []
    for c in caps:
        caplocs.append(s.find(c))
    tograb = []
    # cycle through all pickup options
    for c in caplocs:
        s = s[0: c] + s[c + 1:]
    startstop = [0 if bl == '<' else s.find('|') + 1,
                 s.find('|') if bl == '<' else len(s)]
    print("to be cycled through: ", s[startstop[0]:startstop[1]])
    bl = '<' if bl == '>' else '>'
    i = startstop[0]
    while i <= startstop[1]:
        if i == startstop[1]:
            steps.append([caps + bl, dup])
            dup = s + caps if bl == '>' else caps + s
        else:
            dup = s + s[i] + caps if bl == '>' else s[i] + caps + s
            offset = 0 if bl == '>' else len(caps) + 1
            print(dup[i + offset] + caps + bl)
            steps.append([dup[i + offset] + caps + bl, dup])
            dup = dup[0: i + offset] + dup[i + offset + 1:]
            print(dup)
        step(dup, ic, b, bl, caps)
        i += 1


    # for i in range(s.find('|') - 1 if bl == '<' else len(s) - s.find('|') - 1):
    #     pass

    return s, ic, b


state = start
newVars = step(state, invCombs, "FGCW|", boatLoc, captains)
print(steps)
# state = newVars[0]
