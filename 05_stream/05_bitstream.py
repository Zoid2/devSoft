import random
f = open("krewes.txt")
all_duckies = f.read()
devos = {}
ducky_group = all_duckies.split('@@@')
for ducky in ducky_group:
    if "$$$" in ducky:
        ducky = ducky.split("$$$")
        devos[ducky[1]] = list((ducky[0], ducky[2]))
devo = random.choice(list(devos.keys()))

print("Devo: " + devo + ", " + "Period: " + devos[devo][0] + ", Duck: " + devos[devo][1])