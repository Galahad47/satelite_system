import subprocess
import sys

with open("data.json","r") as data:
    level1 = []; level2 = []; level3 = []; level4 = []
    level1.append(data["level_1"]); level2.append(data["level_2"])
    level3.append(data["level_3"]); level4.append(data["level_4"])
    print(level1,level2,level3,level4)
    if subprocess.run(["ping","W1531"]) != True:
        subprocess.run(["mstsc","/v:W1531","/f"])
    else:
        print("Соединение прервано")