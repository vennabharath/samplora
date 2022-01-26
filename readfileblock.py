#!/usr/bin/env python

filename = "gitcomm.txt"

infile = open(filename, 'r')
data = infile.read()
infile.close()

print(data)
