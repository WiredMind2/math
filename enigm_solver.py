a = lambda x: int(x[-3])==int(x[-2])- 2
b = lambda x: sum(map(int, x)) == 12
c = lambda x: int(x[-1])*int(x[-2])*int(x[-3])==60

i = 0
while i < 1000:
    if all([y(str(i).zfill(5)) for y in [a, b, c]]):
        print(i)
        
    i += 1