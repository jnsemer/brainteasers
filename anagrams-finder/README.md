# Anagrams Finder

This script takes two command line parameters, a dictionary file and an output file, and returns an output of all words and their anagrams. The script fills out a hash table to find anagrams.

Each word is sorted in alphabetical order to create a table entry key, and all words that hash to the same string will be added to the list of values. These purposeful collisions identify all anagrams. 

### To Run

In the command line, execute the following command:
`python anagrams.py your_dict_file your_output_file`
For example:
`python anagrams.py dict1 anagram1`
