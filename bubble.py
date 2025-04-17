from random import randint
def sorting(x):
        for i in range(0,len(x)-1):
            for j in range(0,len(x)-1-i):
                if x[j] > x[j+1]:
                    dat = x[j]
                    x[j] = x[j+1]
                    x[j+1] = dat
        return x

data = []
for i in range(100):
     data.append(randint(1,99))
print(data)
d = sorting(data)
print(d)