import pickle
import numpy as np
import os

DATASET_DIR = "datasets/"
DATASET_NAME = "dataset1/"

with open(os.path.join(DATASET_DIR, DATASET_NAME, "requirements.pkl"), "rb") as f:
    requirements: np.ndarray = pickle.load(f)

with open(os.path.join(DATASET_DIR, DATASET_NAME, "proficiency_levels.pkl"), "rb") as f:
    proficiency_levels: np.ndarray = pickle.load(f)


print(requirements.shape)           # project requirements
print(requirements)
print(proficiency_levels.shape)     # student proficiencies in that field
print(proficiency_levels)

print(proficiency_levels[0])
