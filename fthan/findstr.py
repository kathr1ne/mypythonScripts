#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:kongshuai

import os
import timeit

s = os.sep
start = timeit.default_timer()

def walkFiles(root,string):
    for dirpath,dirname,filename in os.walk(root):
        #print(filename)
        for fn in filename:
            try:
                name = dirpath + s + fn
                #print(name)
                #print("Searcing file'" + name + "'...")
                flag = 0
                #fp = open(name,'r')
                fp = open(name,'r',encoding='UTF-16')
                #print(fp)
                count = 0
                for line in fp.readlines():
                    count += 1
                    if string in line:
                        flag = 1
                        print()
                        #print("Your string is in file'" + name + "'line" + str(count))
                        print( ''+ name +'' )
                if flag == 0:
                    pass
                    #print("Not Found")
            except:
                pass
                #print()
                #print("File'" + name + "'cant't be read")
                    
def main():
    print()
    print("######START######")
    print()
    print("Please input the directory you want to search: ")
    #root = raw_input() python 2.x
    root = input()
    print("Please input your string: ")
    #string = raw_input()
    string = input()
    walkFiles(root,string)
    print()
    print("######OVER#######")

if __name__ == "__main__":
    main()
    
end = timeit.default_timer()
print("spend time: %.2fs" % (end-start))
