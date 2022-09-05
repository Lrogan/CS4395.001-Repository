import sys
import pathlib
import pickle
import re
from typing import Dict

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone
    
    def display(self):
        print("Employee id: " + self.id)
        print("\t" + self.first + " " + self.mi + " " + self.last)
        print("\t" + self.phone)

def dataInput(file):
    print("Processing data file.")
    with open(pathlib.Path.cwd().joinpath(file), 'r') as f:
        text_in = f.readlines()
    text_in.pop(0)
    person_dict = {}
    count = 1
    for line in text_in:
        print("Parsing Line: " + str(count) + "/" + str(len(text_in)))
        count += 1
        fields = line.split(sep=",")
        fields[0] = fields[0].capitalize
        fields[1] = fields[1].capitalize
        fields[2] = 'X' if fields[2] == '' else fields[2].capitalize
        fields[3] = validID(fields[3], list(person_dict.keys()))
        fields[4] = validPhone(fields[4])
        print("Valid Person Detected Adding to Dictionary")
        person_dict[fields[3]] = Person(fields[0], fields[1], fields[2], fields[3], fields[4])
    return person_dict

#checks for a valid phone number, and repeats asking for a valid one until one is given
def validPhone(phone):
    newPhone = phone
    while(not re.search("", newPhone)):
        print("Phone " + newPhone + " is invalid")
        print("Enter phone number in from 123-456-7890")
        newPhone = input("Enter phone number: ")
    return newPhone

#checks for a valid Id and repeats asking for a valid one until one is given
def validID(id, keys):
    newId = id
    uniqueID = not newId in keys
    while(not re.search("^[a-zA-Z]{2}[0-9]{4}$", newId) and uniqueID):
        print("ID invalid: " + id)
        print("ID is two letters followed by 4 digits")
        newId = input("Please input a valid ID: ")
        uniqueID = not newId in keys
    return newId
        

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("Please enter a file name as a system arg")
    # elif sys.argv[1] != 'data/data.csv':
    #     print("The relative path must data/data.csv must be specified in the sysargs")
    # else:
    #     file = sys.argv[1]
    #     dataInput(file)
    file = 'Homework1/data/data.csv'
    dict_created = dataInput(file)
    pickle.dump(dict_created, 'dict.p', 'wb')
    dict_in = pickle.load(open('dict.p', 'rb'))
    print(dict_in)