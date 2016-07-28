#!/usr/bin/python

import os
import re
import sys
import urllib

'''
usage:
python nterm_compare.py pfam_file all_data#

- pfam_file is input alignment (see below)
- all_data# is hash from make_unique_and_intersect.py script

this script takes a pfam file containing fragments of large alignments
and scores each sequence for the presence of a user-defined feature.
here i want to check for potential phospho sites, which i am shorthanding
by ss, st, or ts. counts the occurences of this motif on each line
and creates a dict: [gi,score].

here is a line from the pfam file:
gi|6325239|ref|NP_015307.1|/1-369     ----------------------------MD-----------------------FT--SDTTN------------------------------------------SHDTSNSHLS-------------------LEDAVGTHHAGE---------------------------------------------------------------------------ADVNIDG-DEKQQ

scores are then converted to rgb values (blue range) and written to file
formatted for manual input to a phyloT/TOL annotation file. blank
annotation file can be found here:
http://itol.embl.de/help/dataset_color_strip_template.txt

user should define:
- the input file (pfam formatted alignment)
- the motif to search for using regex
- the output filename, which is 'FORITOL' here
- the rgb colors
  for more complex seq features, should compute a hist for rgb --> bins
- note also that blank lines in the input file are not allowed
'''


def findsites(invars):
    #make a dict with [gi,seq]
    alignment_file = invars[0]
    taxid_gi_file = invars[1]
    dict = {}
    f = open(alignment_file, 'rU')
    for line in f:
      seq = re.search(r'\s([\w-]+)', line)
      if seq:
        seq = seq.group(1)
        seq = seq.replace('-','')
      else:
        seq = 0
      gi = re.search(r'gi\|(\w+)\|', line)
      if gi:
        gi = gi.group(1)
      else:
        gi = 0
        print 'WARNING: MISSING GI OR FORMATTING ERROR IN INPUT FILE!'
      dict[gi] = seq
    f.close()

    #replace values in dict with scores from parsing seq text
    for gi in dict:
      seq = dict[gi]
      seq = len(re.findall(r'[ST][ST]+',seq))
      dict[gi] = seq
    
    #replace dict keys with taxids to get [taxid,score]
    f = open(taxid_gi_file, 'rU')
    for line in f:
      line = line.split(',')
      taxid = line[0]
      gi = line[1].strip()
      dict[taxid] = dict[gi]
      del dict[gi]
    
    #convert dict values to rgb color codes
    blues = ['#ffffff','#9999ff','#3333ff','#0000cc','#000066']
    scores = dict.values()
    max = sorted(scores, reverse=True)[0]
    bin_size = max/5
    for taxid in dict:
      if dict[taxid] == 0:
        dict[taxid] = blues[0]
      elif dict[taxid] < bin_size*1:
        dict[taxid] = blues[1]        
      elif dict[taxid] < bin_size*2:
        dict[taxid] = blues[2]        
      elif dict[taxid] < bin_size*3:
        dict[taxid] = blues[3]
      else:
        dict[taxid] = blues[4]
    
    #write dict to file that can be copy-pasted into itol annotation file
    f = open('FORITOL', 'w')
    for item in dict.items():
      f.write(item[0] + ' ' + item[1] + '\n')
    f.close()





def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: alignment_file all_data'
    sys.exit(1)

  alignment_file = args[0]
  taxid_gi_key_file = args[1]
  invars = [alignment_file,taxid_gi_key_file]   
  scores = findsites(invars)

if __name__ == '__main__':
  main()
