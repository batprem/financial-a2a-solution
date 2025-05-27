
import pickle

with open("part.pkl", "rb") as f:
    part = pickle.load(f)

print(part)