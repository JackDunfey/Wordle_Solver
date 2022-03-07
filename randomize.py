from random import randint
import os

file1 = open("alphabetical_words.txt", "r")
words = []
for x in file1:
  words += [x[:-1].upper()]
words[-1] += str(file1)[-1][-1]

def switch(lisT, oldIndex, newIndex):
    temp = lisT[oldIndex]
    lisT[oldIndex] = lisT[newIndex]
    lisT[newIndex] = temp

for i in range(len(words)):
    switch(words,i,randint(0,len(words)-1))

with open("words.txt","w") as f2:
    f2.write('\n'.join(words))