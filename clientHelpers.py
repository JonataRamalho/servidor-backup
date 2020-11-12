import os

def getFileName(directory):
  directory = directory.split("/")
  return directory[len(directory)-1]

def listDirectory(directory):
  listDirectory = os.listdir(directory)
  for i in listDirectory:
    print(i)

def getData(directory):
  with open(directory, 'r') as file:
    content = (file.read())

  return content

def isEmpty(file):
  data = getData(file) 
  
  return len(data) == 0 and True or False