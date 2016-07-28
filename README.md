# phylogeny_tools
for co-registration of sequence features with phylogenies


INSTRUCTIONS FOR USE:
20160723

Protocol for generating an ITOL tree that shows which leafs have a given seq motif (automated motif identification)

1 - make huge alignments using blast with databases hosted on orchestra (see meeske's guides)

2 - use the blast output to harvest csv files (2): [taxid,gi] (use the tag: -outfmt "6 staxids sgi")(need to remove header + footer from blast_out)

3 - run 'make_unique_and_intersect_TSV.py' in the directory where the blast_out files are stored (usage: python make_unique_and_intersect_TSV.py blast_out0 blast_out1 ...)

4 - run batch entrez for each gi output file (called gi0, gi1, gi2, ...)

5 - recover fasta file from batch entrez and make alignment in mafft

6 - visualize alignment in jalview and subset the part of the alignment you care about --> pfam file (cut off extra lines from pfam file)

7 - run nterm_compare.py using pfam file and all_data# file (from step 3) as inputs (usage: python nterm_compare.py pfam_file all_data#)

8 - copy and paste output file contents from step 7 (FORITOL) into itol template file (http://itol.embl.de/help/dataset_color_strip_template.txt)

9 - open all_data in excel and copy and past the first column (taxids) to itol to make the tree

10 - drag the updated template file onto the tree

