import pickle
import numpy as np
import os
import random

DATASET_DIR = "datasets/"
DATASET_NAME = "dataset1/"

with open(os.path.join(DATASET_DIR, DATASET_NAME, "requirements.pkl"), "rb") as f:
    requirements: np.ndarray = pickle.load(f)

with open(os.path.join(DATASET_DIR, DATASET_NAME, "proficiency_levels.pkl"), "rb") as f:
    proficiency_levels: np.ndarray = pickle.load(f)

studentNum = proficiency_levels.shape[0]
projectNum = requirements.shape[0]

print("asdasdasdasdasd")
print(studentNum)
print(projectNum)

individual = []
for x in range(projectNum):
    individual.append([-1])

studentList = list(range(0,studentNum))
checklist = np.zeros(studentNum)
print("checklist 1")
print(checklist)
print("studentList")
print(studentList)
print("individual")
print(individual)

studentCount = 0
while studentNum > projectNum:       # 1kere hepsine 1 student dağıt
    for x in range(projectNum):
        randStudent = random.randint(0, len(studentList) - 1)
        if randStudent not in individual[x]:  # check already there or not
            if checklist[randStudent] < 2:  # check if in less than 2 projects
                if len(individual[x]) < 3:  # max 3 students
                    individual[x][0] = studentList[randStudent]
                    checklist[studentList[randStudent]] += 1
                    studentNum -= 1
print(individual)
print("checklist 2")
print(checklist)

print(studentNum)
sumInd = 0
randomChooseStudent = random.randint(0, studentNum)
print(randomChooseStudent)
while (randomChooseStudent > 0) and (sumInd <= requirements.shape[0]*3): # either no students left or all the projects are full
    sumInd = 0
    randStudent = random.randint(0,  proficiency_levels.shape[0]-1)
    randProject = random.randint(0, requirements.shape[0] - 1)
    if randStudent not in individual[randProject]: # check already there or not
        if checklist[randStudent] < 2:            # check if in less than 2 projects
            if len(individual[randProject]) < 3:   # max 3 students
                individual[randProject].append(randStudent)  # append for add to project
                checklist[randStudent] += 1

    for i in range(projectNum):
        sumInd += len(individual[i])
    randomChooseStudent -= 1

#print(sumInd)
#print("checklist 2")
#print(checklist)
individualDict = {"individual":[], "checklist":[]}
individualDict["individual"].append(individual)
individualDict["checklist"].append(checklist)
print("individual")
print(individual)
print("studentList")
print(studentList)
print(individualDict)
