file = open("krewes.txt", "r")
print(file.read())
data = file.read().split("@@@")
print(data)
