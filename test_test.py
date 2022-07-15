a = {
    "monsters":[{"hp": 30},{"hp": 20}]
}
ms = a["monsters"]
m1 = ms[0]
m2 = ms[1]
m1hp = m1["hp"]
m2hp = m2["hp"]
m1hp = ms[0]["hp"]
m2hp = ms[1]["hp"]


m1hp = m1["hp"]

print(a)
print(m1hp)
#m1hp = m1hp - 5

#m1["hp"] = m1["hp"] - 5
ms[0]["hp"] = 25
a["monsters"][0]["hp"] = 13

print(a)
print(m1)




#print(a["monsters"{"hp"}])
