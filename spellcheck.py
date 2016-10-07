#!/usr/bin/python

import csv
import sys
import numpy as np
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Find Closest Word
# s = word; dictionary = dict of words to check
def find_closest_word(s, dictionary):
  distances = []
  for i in range(0, len(dictionary)):
    distance = levenshtein_distance(s, dictionary[i], 1, 1, 1)
    if distance == 0:
      return dictionary[i]
    distances.append(distance)
  print distances.index(min(distances))
  return dictionary[distances.index(min(distances))]


# Levenshtein Distance
# s = word 1; t = word 2
# m = strlength of s; n = strlength of t
# deletion_cost, insertion_cost, substitution_cost are fixed
def levenshtein_distance(s, t, deletion_cost, insertion_cost, substitution_cost):
  first_len, second_len = len(s), len(t)
  if s == t:
    return 0

  if first_len > second_len:
    s, t = t, s
    first_len, second_len = second_len, first_len

  if second_len == 0:
    return first_len

  # initialize matrix and zero it out
  d = [[0] * second_len for x in range(first_len)]

  # Set values for first row and first column
  for i in range(0, first_len):
    d[i][0] = i * deletion_cost
  for j in range(0, second_len):
    d[0][j] = j * insertion_cost

  for j in range(1, second_len):
    for i in range(1, first_len):
      if s[i] == t[j]:
        d[i][j] = d[i - 1][j - 1]
      else:
        d[i][j] = min(d[i - 1][j] + deletion_cost, d[i][j - 1] + insertion_cost, d[i - 1][j - 1] + substitution_cost) + 1

  # print d[m - 1][n - 1]
  return d[first_len - 1][second_len - 1]

# Measure Error 
# each ith typo corresponds with the ith true word 
def measure_error(typos, true_words, dictionary):
  error_count = 0
  start = time.time()
  for i in range(0, len(typos)):
    closest_word = find_closest_word(typos[i], dictionary)
    if closest_word == true_words[i]:
      print 'match'
    else:
      print 'typo was: ' + typos[i]
      print closest_word + ' did not match ' + true_words[i]
      error_count = error_count + 1
  print 'Error rate is ' + str(float(error_count) / len(typos))
  print 'Calculation took ' + str(time.time() - start) + ' secs'


def keyboard_distance(a, b):
  if not a.isalpha() or not b.isalpha():
    print 'Please enter alphanumeric characters'
    return

  letter_1 = a.lower()
  letter_2 = b.lower()

  keyboard = np.array([['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'], ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'], ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']])

  print keyboard
  distances = []
  a_index = np.where(keyboard == letter_1)
  b_index = np.where(keyboard == letter_2)
  x1 = a_index[0][0]
  y1 = a_index[1][0]
  x2 = b_index[0][0]
  y2 = b_index[1][0]
  return abs(x1 - x2) + abs(y1 - y2)


# QWERTY Levenshtein Distance
# Deletion cost, insertion cost are fixed
# Substitution cost is based on keyboard distance
def qwerty_levenshtein_distance(str1, str2, deletion_cost, insertion_cost):
  first_len, second_len = len(s), len(t)
  if s == t:
    return 0

  if first_len > second_len:
    s, t = t, s
    first_len, second_len = second_len, first_len

  if second_len == 0:
    return first_len

  # initialize matrix and zero it out
  d = [[0] * second_len for x in range(first_len)]

  # Set values for first row and first column
  for i in range(0, first_len):
    d[i][0] = i * deletion_cost
  for j in range(0, second_len):
    d[0][j] = j * insertion_cost

  for j in range(1, second_len):
    for i in range(1, first_len):
      if s[i] == t[j]:
        d[i][j] = d[i - 1][j - 1]
      else:
        d[i][j] = min(d[i - 1][j] + deletion_cost, d[i][j - 1] + insertion_cost, d[i - 1][j - 1] + substitution_cost) + 1

  return d[first_len - 1][second_len - 1]

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
  typos = []
  true_words = []
  with open(dict_word_list, 'r') as word_dict_file:
    words = [line.strip() for line in word_dict_file]

  with open(filename, 'r') as target_file:
    for line in target_file:
      typos.append(line.split('\t')[0].strip())
      true_words.append(line.split('\t')[1].strip())

  # print typos[:50]
  # measure_error(typos[:200], true_words[:200], words)
  print keyboard_distance('Q', 'q')
  # word = find_closest_word('abilties', words[:50])
  # print word
  ## distance = levenshtein_distance('abilities', 'abilities', 1, 1, 1)
  # print distance

if __name__ == '__main__':
  main()

