#!/usr/bin/python

import csv
import sys
import numpy as np
import time

# s = word; dictionary = dict of words to check
def find_closest_word(s, dictionary):
  distances = []
  for i in range(0, 15):
    distance = levenshtein_distance(s, dictionary[i], 1, 1, 1)
    if distance == 0:
      return dictionary[i]
    distances.append(distance)

  return dictionary[distances.index(min(distances))]


# s = word 1; t = word 2
# m = strlength of s; n = strlength of t
# deletion_cost = insertion_cost = substitution_cost = 1
def levenshtein_distance(s, t, deletion_cost, insertion_cost, substitution_cost):
  m, n = len(s), len(t)

  if n == 0:
    return m

  # initialize matrix and zero it out
  d = [[0] * n for x in range(m)]

  # Set values for first row and first column
  for i in range(0, m):
    d[i][0] = i * deletion_cost
  for j in range(0, n):
    d[0][j] = j * insertion_cost

  for j in range(0, n):
    for i in range(0, m):
      if s[i] == t[j]:
        d[i][j] = d[i - 1][j - 1]
      else:
        d[i][j] = min(d[i - 1][j] + deletion_cost, d[i][j - 1] + insertion_cost, d[i - 1][j - 1] + substitution_cost)

  return d[m - 1][n - 1]

# each ith typo corresponds with the ith true word 
def measure_error(typos, true_words, dictionary):
  error_count = 0
  for i in range(0, len(typos)):
    closest_word = find_closest_word(typos[i], dictionary)
    if closest_word == true_words[i]:
      print 'match'
    else:
      print 'did not match'
      error_count = error_count + 1
  print float(error_count) / len(typos)


def main():
  args = sys.argv[1:]

  if len(args) != 2:
    print 'Usage: python spellcheck.py <fileToBeSpellChecked> <DictionaryOfWords>'
    sys.exit(1)

  filename = args[0]
  dict_word_list = args[1]

  # with open(dict_word_list) as word_dict_file:
  #   reader = csv.reader(word_dict_file)
  #   find_closest_word('abandonment', reader)

  words = []
  data = []
  with open(dict_word_list, 'r') as word_dict_file:
    words = [line.strip() for line in word_dict_file]

  with open(filename, 'r') as target_file:
    data = [line.strip() for line in target_file]

  measure_error(['abrodenment', 'abeck', 'abbrevate'], ['abandonment', 'aback', 'abbreviate'], words)


if __name__ == '__main__':
  main()

