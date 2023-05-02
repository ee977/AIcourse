import random

def foo(x,y,z):
    return 6*x**3 + 9*y**2 + 90 *z -25

def fitness(x,y,z):
    ans = foo(x,y,z)

    if ans == 0:
        return 99999
    else:
        return abs(1/ans)

sol = []    #generate sol
for s in range(1000):
    sol.append((random.uniform(0,10000),
                random.uniform(0,10000),
                random.uniform(0,10000)))
for i in range(10000):

    rankedSol = []
    for s in sol:
        rankedSol.append( (fitness(s[0],s[1],s[2]), s))
    rankedSol.sort()
    rankedSol.reverse()

    print(f"=== Gen {i} best solutions ===")
    print(rankedSol[0])

    if rankedSol[0][0] > 9999:
        break

    bestSol = rankedSol[:100]

    elements = []
    for s in bestSol:
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])

    newGen = []
    for _ in range(1000):
        e1 = random.choice(elements) * random.uniform(0.99, 1.01)
        e2 = random.choice(elements)    * random.uniform(0.99, 1.01)
        e3 = random.choice(elements)* random.uniform(0.99, 1.01)

        newGen.append((e1,e2,e3))

    sol = newGen
