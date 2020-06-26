import pickle
import os

#Create a list

save_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents","audioManagement.dat")
print(save_path)

names = ["James Allnutt", "Tom Lewis", "Madiha Aasim"]

print("Original List")
print(names)

#Save List

pickle.dump(names, open(save_path, "wb"))

#Change List
names.remove("James Allnutt")

print("Changed List")
print(names)

##Load the save data
names = pickle.load(open(save_path, "rb"))

print("Original List")
print(names)