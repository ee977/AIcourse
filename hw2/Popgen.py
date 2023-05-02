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

print(studentNum)
print(projectNum)

individual = []
for x in range(projectNum):
    individual.append([-1])

studentList = list(range(0,studentNum))
checklist = np.zeros(studentNum)
individual[3][0] = 31
print("checklist 1")
print(checklist)
print("studentList")
print(studentList)
print("individual")
print(individual)
studentCount = 0
while studentNum > projectNum:       # 1kere hepsine 1 student dağıt
    for x in range(projectNum):
        randStudent = random.randint(0, len(studentList)-1)
        individual[x][0] = studentList[randStudent]
        checklist[studentList[randStudent]] += 1

        studentCount += 1
        del studentList[randStudent]
        studentNum -= 1

print("checklist 2")
print(checklist)


while studentCount <= 20:
    j = 0
    randStudent = random.randint(0,  proficiency_levels.shape[0]-1)
    if checklist[randStudent] <= 2:
        individual[x].append(proficiency_levels[randStudent])       # appendle extre ekliyoz
        checklist[randStudent] += 1
        #del studentList[randStudent]
    studentNum -= 1
    j += 1

individualDict = {"individual":[], "checklist":[]}
individualDict["individual"].append(individual)
individualDict["checklist"].append(checklist)
print("individual")
print(individual)
print("studentList")
print(studentList)
print(individualDict)
