#!/usr/bin/python

import os
import re
import sys
import shutil


def sort_genes(files):
    """
    usage:
    python make_unique_and_intersect_TSV.py blast_out0 blast_out1 ...
    
    Given a list of csv with [list of taxid,gi], writes them to dicts.
    writes each dict as a list entry. then finds the intersection between all
    taxids and writes files:
    gi# - a list of gis for each input file
    all_data# - a hash table with [taxid,gi] for each input file"""
     
    #make a list of dicts with the data from each file truncated stored
    
    all_data = []
    for file in files:
      dict = {}
      f = open (file, 'rU')
      for line in f:
        line = line.strip()
        gi = line.split('\t')[0]
        gi = gi.split(';').pop()
        if not line.split('\t')[1] in dict.values() and not gi in dict.keys():
          dict[gi] = line.split('\t')[1]
      all_data.append(dict)
      
    #print the gis to a gicount dict and append to all_data
    
    taxidcounts = {}
    for dict in all_data:
      for taxid in dict.keys():
        if not taxid in taxidcounts.keys():
          taxidcounts[taxid] = 1
        else:
          taxidcounts[taxid] = taxidcounts[taxid] + 1

    #harvest all gis from gicounts with n = # input files
    
    taxidcounts = {k:v for k,v in taxidcounts.items() if v == len(files)}
    for dict in all_data:
      dict = {k:v for k,v in dict.items() if v in taxidcounts.keys()}

    #write gi to csv
    counter = -1
    for dict in all_data:
      counter = counter +1
      filename1 = 'gi' + str(counter)
      filename2 = 'all_data' + str(counter)
    #write gi files
      f = open(filename1, 'w')
      for item in dict.items():
        f.write(item[1] + '\n')
      f.close()
    #write all_data files
      f = open(filename2, 'w')
      for item in dict.items():
        f.write(item[0] + ',' + item[1] + '\n')
      f.close() 
    #return list of dicts to main
    return all_data

      


  

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: file0 file1'
    sys.exit(1)
  
  files = []
  for arg in args:
    files.append(arg)
    
  unique_dict = sort_genes(files)

if __name__ == '__main__':
  main()
