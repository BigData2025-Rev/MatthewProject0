import random

start = random.randrange(0,4)
for i in range(4):

    print([(x+start) % 4 for x in range(4)])
    start +=1 
