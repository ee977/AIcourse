import pickle
import numpy as np
import os
import random
import math
import matplotlib.pyplot as plt

DATASET_DIR = "datasets/"
DATASET_NAME = "dataset1/"

with open(os.path.join(DATASET_DIR, DATASET_NAME, "requirements.pkl"), "rb") as f:
    requirements: np.ndarray = pickle.load(f)

with open(os.path.join(DATASET_DIR, DATASET_NAME, "proficiency_levels.pkl"), "rb") as f:
    proficiency_levels: np.ndarray = pickle.load(f)

population = []
populationNumber = 10
iteration = 10
elitismPercentage = 0.31
mutationRate = 0.001
fitnessBest = []
fitnessWorst = []
for i in range(populationNumber):   # population generation
    individual = []
    studentNum = proficiency_levels.shape[0]
    projectNum = requirements.shape[0]

    for x in range(projectNum):
        individual.append([-1])

    studentList = list(range(0, studentNum))
    checklist = np.zeros(studentNum)

    studentCount = 0
    while studentNum > projectNum:  # give 1 rand student to each project
        for x in range(projectNum):
            randStudent = random.randint(0, len(studentList) - 1)
            individual[x][0] = studentList[randStudent]
            checklist[studentList[randStudent]] += 1
            studentCount += 1
            del studentList[randStudent]
            studentNum -= 1
    sumInd = 0      # distrubute new students to projects
    randomChooseStudent = random.randint(0, studentNum) # choose how many rand students to distrubute
    while (randomChooseStudent > 0) and (sumInd <= requirements.shape[0] * 3):  # either no students left or all the projects are full
        sumInd = 0
        randStudent = random.randint(0, proficiency_levels.shape[0] - 1)
        randProject = random.randint(0, requirements.shape[0] - 1)
        if randStudent not in individual[randProject]:  # check already there or not
            if checklist[randStudent] < 2:  # check if in less than 2 projects
                if len(individual[randProject]) < 3:  # max 3 students
                    individual[randProject].append(randStudent)  # append for add to project
                    checklist[randStudent] += 1

        for i in range(projectNum):
            sumInd += len(individual[i])
        randomChooseStudent -= 1
    individualDict = {"fitness": float, "individual": [], "checklist": []}
    individualDict["individual"].append(individual)
    individualDict["checklist"].append(checklist)
    population.append(individualDict)

########################################################################################################################
########################################################################################################################
newGen = []
for iter in range(iteration):
    #print("########################################################################################################################")
    print(iter)
    print(population)
    if iter < 1:
        for x in range(populationNumber):  # fitness function for pop
            fitnessScore = 0
            for i in range(requirements.shape[0]):  # fitness function for ind
                for j in range(len(population[x]["individual"][0][i])):  # add all values
                    fitnessScore += np.dot(requirements[i], proficiency_levels[population[x]["individual"][0][i][j]])
            population[x]["fitness"] = fitnessScore  # update old 0
        sortedPop = sorted(population, key=lambda x: x['fitness'], reverse=True)  # sort by fitness score
        #print("POPULATION FIRST")
        #print(population)
        elitismNumber = math.ceil(populationNumber * elitismPercentage)
        for j in range(elitismNumber):  # ELITISM
            newGen.append(sortedPop[j])  # for holding the elites
    # check the elitism before and after selection
    else:
        #print("POPULATION FIRST")
        #print(population)
        """elitismNumber = math.ceil(populationNumber * elitismPercentage)
        for j in range(elitismNumber):  # ELITISM
            newGen.append(population[j])  # for holding the elites"""
    #print(newGen)
    parents = []
    indvList = list(range(0, populationNumber))
    mod0 = [-1, -1]
    counter = 0
    bestOf = 2
    for j in range(populationNumber):   # TOURNAMENT SELECTION
        randIndv = random.randint(0, len(indvList) - 1)
        mod0[1] = max(mod0[1], sortedPop[indvList[randIndv]]["fitness"])
        if mod0[1] == sortedPop[indvList[randIndv]]["fitness"]:
            mod0[0] = indvList[randIndv]
        if counter == (bestOf -1):
            parents.append(sortedPop[mod0[0]])
            mod0 = [-1, -1]
            counter = -1
        del indvList[randIndv]
        counter += 1
    if populationNumber % (bestOf) != 0:   # add the one ones that are left if number is not divisible
        parents.append(sortedPop[mod0[0]])

    parentList = list(range(0, len(parents)))
    childsss = []
    oddParent = False
    if len(parents)%2 == 1:
        oddParent = True
    for j in range(math.ceil(len(parents)/2)):  # CROSSOVER math.ceil(len(parents)/2)
        randFemale = random.randint(0, len(parentList) - 1)
        female = parentList[randFemale]
        del parentList[randFemale]
        randMale = random.randint(0, len(parentList) - 1)
        male = parentList[randMale]
        if oddParent == False:
            del parentList[randMale]
        else:
            oddParent = False
        child1 = {"fitness": float, "individual": [], "checklist": []}
        child2 = {"fitness": float, "individual": [], "checklist": []}
        child1["individual"] = parents[male]["individual"]
        child1["checklist"] = parents[male]["checklist"]
        child2["individual"] = parents[female]["individual"]
        child2["checklist"] = parents[female]["checklist"]
        k = 0
        for l in range(len(parents[female]["individual"][0])):
            possible = True
            for m in range(len(parents[female]["individual"][0][l])):
                if child1["checklist"][0][parents[female]["individual"][0][l][m]] >= 2: # if less than 2 project it has
                    possible = False
            if possible == True and k < requirements.shape[0] / 2:
                k += 1
                if len(parents[female]["individual"][0][l]) == len(child1["individual"][0][l]):
                    for n in range(len(parents[female]["individual"][0][l])):
                        child1["checklist"][0][child1["individual"][0][l][n]] -= 1
                        child1["individual"][0][l][n] = parents[female]["individual"][0][l][n]
                        child1["checklist"][0][child1["individual"][0][l][n]] += 1
                elif len(parents[female]["individual"][0][l]) < len(child1["individual"][0][l]):
                    forFixingNumber = -1
                    for n in range(len(child1["individual"][0][l])):
                        if n < len(parents[female]["individual"][0][l]):
                            child1["checklist"][0][child1["individual"][0][l][n]] -= 1
                            child1["individual"][0][l][n] = parents[female]["individual"][0][l][n]
                            child1["checklist"][0][child1["individual"][0][l][n]] += 1
                        elif n >= len(parents[female]["individual"][0][l]):
                            forFixingNumber += 1
                            child1["checklist"][0][child1["individual"][0][l][n - forFixingNumber]] -= 1
                            del child1["individual"][0][l][n - forFixingNumber]
                elif len(parents[female]["individual"][0][l]) > len(child1["individual"][0][l]):
                    for n in range(len(parents[female]["individual"][0][l])):
                        if n < len(child1["individual"][0][l]):
                            child1["checklist"][0][child1["individual"][0][l][n]] -= 1
                            child1["individual"][0][l][n] = parents[female]["individual"][0][l][n]
                            child1["checklist"][0][child1["individual"][0][l][n]] += 1
                        elif n >= len(child1["individual"][0][l]):
                            child1["individual"][0][l].append(parents[female]["individual"][0][l][n])
                            child1["checklist"][0][child1["individual"][0][l][n]] += 1
        childsss.append(child1)
        k = 0
        for l in range(len(parents[male]["individual"][0])):
            possible = True
            for m in range(len(parents[male]["individual"][0][l])):
                if child2["checklist"][0][parents[male]["individual"][0][l][m]] >= 2:  # if less than 2 project it has
                    possible = False
            if possible == True and k < requirements.shape[0] / 2:
                k += 1
                if len(parents[male]["individual"][0][l]) == len(child2["individual"][0][l]):
                    for n in range(len(parents[male]["individual"][0][l])):
                        child2["checklist"][0][child2["individual"][0][l][n]] -= 1
                        child2["individual"][0][l][n] = parents[male]["individual"][0][l][n]
                        child2["checklist"][0][child2["individual"][0][l][n]] += 1
                elif len(parents[male]["individual"][0][l]) < len(child2["individual"][0][l]):
                    forFixingNumber = -1
                    for n in range(len(child2["individual"][0][l])):
                        if n < len(parents[male]["individual"][0][l]):
                            child2["checklist"][0][child2["individual"][0][l][n]] -= 1
                            child2["individual"][0][l][n] = parents[male]["individual"][0][l][n]
                            child2["checklist"][0][child2["individual"][0][l][n]] += 1
                        elif n >= len(parents[male]["individual"][0][l]):
                            forFixingNumber += 1
                            child2["checklist"][0][child2["individual"][0][l][n - forFixingNumber]] -= 1
                            del child2["individual"][0][l][n - forFixingNumber]
                elif len(parents[male]["individual"][0][l]) > len(child2["individual"][0][l]):
                    for n in range(len(parents[male]["individual"][0][l])):
                        if n < len(child2["individual"][0][l]):
                            child2["checklist"][0][child2["individual"][0][l][n]] -= 1
                            child2["individual"][0][l][n] = parents[male]["individual"][0][l][n]
                            child2["checklist"][0][child2["individual"][0][l][n]] += 1
                        elif n >= len(child2["individual"][0][l]):
                            child2["individual"][0][l].append(parents[male]["individual"][0][l][n])
                            child2["checklist"][0][child2["individual"][0][l][n]] += 1
        childsss.append(child2)
    for c in childsss:  # MUTATION
        randomValue = random.random()
        if randomValue < mutationRate:
            randomTmp1 = random.randint(0, len(c) - 1)
            randomTmp2 = random.randint(0, len(c) - 1)
            temp = c["individual"][0][randomTmp1]
            c["individual"][0][randomTmp1] = c["individual"][0][randomTmp2]
            c["individual"][0][randomTmp2] = temp
    for x in range(len(childsss)):  # fitness function for pop
        fitnessScore = 0
        for i in range(requirements.shape[0]):  # fitness function for ind
            for j in range(len(childsss[x]["individual"][0][i])):  # add all values
                fitnessScore += np.dot(requirements[i], proficiency_levels[childsss[x]["individual"][0][i][j]])
        childsss[x]["fitness"] = fitnessScore  # update old 0
    #print("newGen with only elites")
    #print(newGen)
    for ind in childsss:
        newGen.append(ind)
    #print("newGen with only elites and childs")
    #print(newGen)
    for ind in parents:
        newGen.append(ind)
    #print("newGen before sort")
    #print(newGen)
    
    sortedNewGen = sorted(newGen, key=lambda x: x['fitness'], reverse= True)   #sort by fitness score
    #print("SORTED NEW GEEEEEEEEEEEEN")
    #print(sortedNewGen)
    #print(len(sortedNewGen))

    #population = []
    population = sortedNewGen[0:populationNumber]
    print("COPIED NEWGEEEEEEEEEEEEEEN")
    print(population)
    #print(len(population))
    newGen = []
    sortedNewGen = []
    fitnessBest.append(population[0]["fitness"])
    fitnessWorst.append(population[populationNumber-1]["fitness"])

#print(parents)
#print(childsss)

### plot
print("adasd")
print(len(fitnessBest))
print(len(fitnessWorst))
print(iteration)
geno = list(range(0, iteration))

plt.plot(geno,fitnessBest,geno,fitnessWorst)
plt.show()

plt.ylabel("Best - Worst Fitness")
plt.xlabel("Generation")
