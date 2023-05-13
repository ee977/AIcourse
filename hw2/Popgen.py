import pickle
import numpy as np
import os
import random
import math

DATASET_DIR = "datasets/"
DATASET_NAME = "dataset1/"

with open(os.path.join(DATASET_DIR, DATASET_NAME, "requirements.pkl"), "rb") as f:
    requirements: np.ndarray = pickle.load(f)

with open(os.path.join(DATASET_DIR, DATASET_NAME, "proficiency_levels.pkl"), "rb") as f:
    proficiency_levels: np.ndarray = pickle.load(f)

population = []
populationNumber = 17
iteration = 1
elitismPercentage = 0.1
mutationRate = 0.01

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


for iter in range(iteration):
    for x in range(populationNumber):  # fitness function for pop
        fitnessScore = 0
        for i in range(requirements.shape[0]):  # fitness function for ind
            for j in range(len(population[x]["individual"][0][i])):  # add all values
                fitnessScore += np.dot(requirements[i], proficiency_levels[population[x]["individual"][0][i][j]])
        population[x]["fitness"] = fitnessScore  # update old 0
    sortedPop = sorted(population, key=lambda x: x['fitness'], reverse= True)   #sort by fitness score
    newGen = []         # check the elitism before and after selection
    elitismNumber = math.ceil(populationNumber * elitismPercentage)
    for j in range(elitismNumber):     # ELITISM
        newGen.append(sortedPop[j])                        # for holding the elites

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
    #print(parentList)
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
        """print("çift")
        print(parents[male])
        print(parents[female])"""

        child1 = {"fitness": float, "individual": [], "checklist": []}
        child2 = {"fitness": float, "individual": [], "checklist": []}

        child1["individual"] = parents[male]["individual"][0]
        child1["checklist"] = parents[male]["checklist"][0]
        child2["individual"] = parents[female]["individual"][0]
        child2["checklist"] = parents[female]["checklist"][0]
        #print("child 1")
        #print(child1)
        k = 0
        for l in range(len(parents[female]["individual"][0])):
            possible = True
            for m in range(len(parents[female]["individual"][0][l])):
                if child1["checklist"][parents[female]["individual"][0][l][m]] >= 2: # if less than 2 project it has
                    possible = False
            if possible == True and k < requirements.shape[0] / 2:
                k += 1
                if len(parents[female]["individual"][0][l]) == len(child1["individual"][l]):
                    for n in range(len(parents[female]["individual"][0][l])):
                        child1["checklist"][child1["individual"][l][n]] -= 1
                        child1["individual"][l][n] = parents[female]["individual"][0][l][n]
                        child1["checklist"][child1["individual"][l][n]] += 1
                elif len(parents[female]["individual"][0][l]) < len(child1["individual"][l]):
                    forFixingNumber = -1
                    for n in range(len(child1["individual"][l])):
                        #print(child1["individual"][l])
                        if n < len(parents[female]["individual"][0][l]):
                            child1["checklist"][child1["individual"][l][n]] -= 1
                            child1["individual"][l][n] = parents[female]["individual"][0][l][n]
                            child1["checklist"][child1["individual"][l][n]] += 1
                        elif n >= len(parents[female]["individual"][0][l]):
                            forFixingNumber += 1
                            child1["checklist"][child1["individual"][l][n - forFixingNumber]] -= 1
                            del child1["individual"][l][n - forFixingNumber]
                elif len(parents[female]["individual"][0][l]) > len(child1["individual"][l]):
                    for n in range(len(parents[female]["individual"][0][l])):
                        #print(child1["individual"][l])
                        if n < len(child1["individual"][l]):
                            child1["checklist"][child1["individual"][l][n]] -= 1
                            child1["individual"][l][n] = parents[female]["individual"][0][l][n]
                            child1["checklist"][child1["individual"][l][n]] += 1
                        elif n >= len(child1["individual"][l]):
                            #child1["checklist"][child1["individual"][l][n]] -= 1
                            child1["individual"][l].append(parents[female]["individual"][0][l][n])
                            child1["checklist"][child1["individual"][l][n]] += 1
        #print(child1)
        childsss.append(child1)
        #print("child 2 ")
        #print(child2)
        k = 0
        for l in range(len(parents[male]["individual"][0])):
            possible = True
            for m in range(len(parents[male]["individual"][0][l])):
                if child2["checklist"][parents[male]["individual"][0][l][m]] >= 2:  # if less than 2 project it has
                    possible = False
            if possible == True and k < requirements.shape[0] / 2:
                k += 1
                if len(parents[male]["individual"][0][l]) == len(child2["individual"][l]):
                    for n in range(len(parents[male]["individual"][0][l])):
                        child2["checklist"][child2["individual"][l][n]] -= 1
                        child2["individual"][l][n] = parents[male]["individual"][0][l][n]
                        child2["checklist"][child2["individual"][l][n]] += 1
                elif len(parents[male]["individual"][0][l]) < len(child2["individual"][l]):
                    forFixingNumber = -1
                    for n in range(len(child2["individual"][l])):
                        # print(child1["individual"][l])
                        if n < len(parents[male]["individual"][0][l]):
                            child2["checklist"][child2["individual"][l][n]] -= 1
                            child2["individual"][l][n] = parents[male]["individual"][0][l][n]
                            child2["checklist"][child2["individual"][l][n]] += 1
                        elif n >= len(parents[male]["individual"][0][l]):
                            forFixingNumber += 1
                            child2["checklist"][child2["individual"][l][n - forFixingNumber]] -= 1
                            del child2["individual"][l][n - forFixingNumber]
                elif len(parents[male]["individual"][0][l]) > len(child2["individual"][l]):
                    for n in range(len(parents[male]["individual"][0][l])):
                        # print(child1["individual"][l])
                        if n < len(child2["individual"][l]):
                            child2["checklist"][child2["individual"][l][n]] -= 1
                            child2["individual"][l][n] = parents[male]["individual"][0][l][n]
                            child2["checklist"][child2["individual"][l][n]] += 1
                        elif n >= len(child2["individual"][l]):
                            # child1["checklist"][child1["individual"][l][n]] -= 1
                            child2["individual"][l].append(parents[male]["individual"][0][l][n])
                            child2["checklist"][child2["individual"][l][n]] += 1
        #print(child2)
        childsss.append(child2)
        #print(childsss)
        for c in childsss:          # MUTATION
            randomValue = random.random()
            if randomValue < mutationRate:
                randomTmp1 = random.randint(0, len(c) - 1)
                randomTmp2 = random.randint(0, len(c) - 1)
                temp = c["individual"][randomTmp1]
                c["individual"][randomTmp1] = c["individual"][randomTmp2]
                c["individual"][randomTmp2] = temp

    for ind in childsss:
        newGen.append(ind)
    for ind in parents:
        newGen.append(ind)
    print(newGen)
    print(newGen[0]["individual"][0][0])
    print(requirements[0])
    print(proficiency_levels[ newGen[0]["individual"][0][1][0] ])
    print(len(newGen))
    for x in range(len(newGen)):  # fitness function for pop
        fitnessScore = 0
        for i in range(requirements.shape[0]):  # fitness function for ind
            for j in range(len(newGen[x]["individual"][0][i])):  # add all values
                fitnessScore += np.dot( requirements[i], proficiency_levels[ newGen[x]["individual"][0][i][j] ]   )
        newGen[x]["fitness"] = fitnessScore  # update old 0
    sortedNewGen = sorted(newGen, key=lambda x: x['fitness'], reverse= True)   #sort by fitness score

#print(parents)
#print(childsss)

