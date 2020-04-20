#!/usr/bin/env python3
import timeit
from collections import defaultdict
import sys

class HashTable(object): #initialize the HashTable object

    def __init__(self, fileInput, fileOutput):
        self.words = self.initializeWords(fileInput)
        self.hashtable = defaultdict(list)
        self.fileOutput = fileOutput

    def initializeWords(self, filename): #reads the file and puts each word into a list
        mylist = []
        f = open(filename, 'r')
        for line in f:
            mylist.append(line[:-1])
        return mylist

    def sortWord(self, word): #insertion sort
        l = list(word)
        for i in range(1, len(l)):
            tmp = l[i]
            pos = i
            while pos > 0 and tmp < l[pos-1]:
                l[pos] = l[pos-1]
                pos -= 1
            l[pos] = tmp
        hashed = ''.join(l)
        return hashed

    def fillTable(self): #hashes each word and adds it to hashtable
        for word in self.words:
            hashstring = self.sortWord(word)
            self.hashtable[hashstring].append(word)

    def outputClasses(self): #writes to file
        f = open(self.fileOutput, 'w')
        for item in self.hashtable:
            if len(self.hashtable[item]) > 0 :
                f.write("%s\n" % str(self.hashtable[item]))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Error: Please include exactly 2 files: dictionary_file, output_file")
        return 1
    else:
        start = timeit.default_timer()
        anagram = HashTable(sys.argv[1], sys.argv[2])
        anagram.fillTable()
        anagram.outputClasses()
        stop = timeit.default_timer()
        print(stop - start)
