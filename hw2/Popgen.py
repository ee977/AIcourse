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
populationNumber = 10
iteration = 1
elitismPercentage = 0.1

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
                # print(proficiency_levels[population[x]["individual"][0][i][j]])
                # print(population[x]["individual"][0][i][j])
                fitnessScore += np.dot(requirements[i], proficiency_levels[population[x]["individual"][0][i][j]])
                # print(np.dot(requirements[i], proficiency_levels[population[x]["individual"][0][i][j]]))
        population[x]["fitness"] = fitnessScore  # update old 0

    """print(population[0]["fitness"])
    print(population[1]["fitness"])
    print(population[2]["fitness"])
    print(population[3]["fitness"])"""

    sortedPop = sorted(population, key=lambda x: x['fitness'], reverse= True)   #sort by fitness score
    #print(sortedPop)


    newGen = []         # check the elitism before and after selection
    #print(math.ceil(populationNumber * elitismPercentage))
    elitismNumber = math.ceil(populationNumber * elitismPercentage)
    for j in range(elitismNumber):     # ELITISM
        newGen.append(sortedPop[j])                        # for holding the elites

    indvList = list(range(0, populationNumber))
    print(sortedPop)
    print(newGen)
    print(indvList)
    mod0 = [-1, -1]
    mod1 = [-1, -1]
    mod2 = [-1, -1]
    mod3 = [-1, -1]
    for j in range(populationNumber):
        randIndv = random.randint(0, len(indvList) - 1)
        del indvList[randIndv]
        if j % 4 == 0:
            mod0[1] = max(mod0[1], population[randIndv]["fitness"])
            if mod0[1] == population[randIndv]["fitness"]:
                mod0[0] = randIndv
            print(mod0[1])
        elif j % 4 == 1:
            mod1[1] = max(mod1[1], population[randIndv]["fitness"])
            if mod1[1] == population[randIndv]["fitness"]:
                mod1[0] = randIndv
            print(j)
        elif j % 4 == 2:
            mod2[1] = max(mod2[1], population[randIndv]["fitness"])
            if mod2[1] == population[randIndv]["fitness"]:
                mod2[0] = randIndv
            print(j)
        else:
            mod3[1] = max(mod3[1], population[randIndv]["fitness"])
            if mod3[1] == population[randIndv]["fitness"]:
                mod3[0] = randIndv
            print()


    print(indvList)
print(newGen)
print()
# asd = sorted(population,key = "fitness")
