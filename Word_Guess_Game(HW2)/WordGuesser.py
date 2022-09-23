import sys
import pathlib
import pickle
import re

def inputData(file):
  print("Processing data file.")
  with open(pathlib.Path.cwd().joinpath(file), 'r') as f:
    raw_text = f.readlines()
  return ""


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     sys.exit("Exiting Pogram: Please enter a file name as a system arg.")
    # else:
    #     file = sys.argv[1]
    #     dataInput(file)
    file = '/Word_Guess_Game(HW2)/anat19.txt'

    inputData(file)
