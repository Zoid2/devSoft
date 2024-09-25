'''
Ziyad, Sascha
Team Sizzle
K06 StI/O: Divine your Destiny!
'''
import csv
def processData():
    with open("occupations.csv", "r") as file:
        data = csv.reader(file)
    dic = {}
    for row in data:
        for c in row:
            c = dic[c][row]
    print(dic)
processData()