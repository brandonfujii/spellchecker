#!/usr/bin/python

import csv
import sys
import numpy as np
import time
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Find Closest Word
# s = word; dictionary = dict of words to check
def find_closest_word(s, dictionary):
  distances = []
  for i in range(0, len(dictionary)):
    # To test levenshtein distance, use code below:
    distance = levenshtein_distance(s, dictionary[i], 1, 1, 1)
    # To test qwerty_levenshtein_distance, comment out code below:
    # distance = qwerty_levenshtein_distance(s, dictionary[i], 4, 8)
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
    true_word = true_words[i]
    if ',' in true_word:
      true_word_arr = true_word.split(',')
      has_match = False
      for x in range(0, len(true_word_arr)):
        word = true_word_arr[x].strip()
        if closest_word == word:
          has_match = True 
          break
      if has_match:
        print 'match'
      else:
        print 'typo was: ' + typos[i]
        print closest_word + ' did not match ' + true_word
        error_count = error_count + 1
    elif ' ' in true_word:
      true_word_arr = true_word.split(' ')
      has_match = False
      for x in range(0, len(true_word_arr)):
        word = true_word_arr[x].strip()
        if closest_word == word:
          has_match = True 
          break
      if has_match:
        print 'match'
      else:
        print 'typo was: ' + typos[i]
        print closest_word + ' did not match ' + true_word
        error_count = error_count + 1

    else:
      if closest_word == true_word:
        print 'match'
      else:
        print 'typo was: ' + typos[i]
        print closest_word + ' did not match ' + true_word
        error_count = error_count + 1
  print 'Error rate is ' + str(float(error_count) / len(typos))
  print 'Calculation took ' + str(time.time() - start) + ' secs'


# Keyboard distance
# Calculates the distance between two letters on a keyboard
def keyboard_distance(a, b):
  if not a.isalpha() or not b.isalpha():
    return 0

  letter_1 = a.lower()
  letter_2 = b.lower()

  keyboard = np.array([['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'], ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'], ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']])

  distances = []
  a_index = np.where(keyboard == letter_1)
  b_index = np.where(keyboard == letter_2)
  x1 = a_index[0][0]
  y1 = a_index[1][0]
  x2 = b_index[0][0]
  y2 = b_index[1][0]
  return abs(x1 - x2) + abs(y1 - y2)

def better_keyboard_distance(a, b):
  if not a.isalpha() or not b.isalpha():
    return 0
  letter_1 = a.lower()
  letter_2 = b.lower()
  keyboard_dict = {
    'q' : (0, 0), 'w' : (0, 1), 'e' : (0, 2), 'r' : (0, 3), 't' : (0, 4), 'y' : (0, 5), 'u' : (0, 6), 'i' : (0, 7), 'o' : (0, 8), 'p' : (0, 9),
    'a' : (1, 0), 's' : (1, 1), 'd' : (1, 2), 'f' : (1, 3), 'g' : (1, 4), 'h' : (1, 5), 'j' : (1, 6), 'k' : (1, 7), 'l' : (1, 8), ';' : (1, 9),
    'z' : (2, 0), 'x' : (2, 1), 'c' : (2, 2), 'v' : (2, 3), 'b' : (2, 4), 'n' : (2, 5), 'm' : (2, 6), ',' : (2, 7), '.' : (2, 8), '/' : (1, 9)
  }

  a_coordinates = keyboard_dict[letter_1]
  b_coordinates = keyboard_dict[letter_2]

  return abs(a_coordinates[0] - b_coordinates[0]) + abs(a_coordinates[1] - b_coordinates[1])

# QWERTY Levenshtein Distance
# Deletion cost, insertion cost are fixed
# Substitution cost is based on keyboard distance
def qwerty_levenshtein_distance(s, t, deletion_cost, insertion_cost):
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
        d[i][j] = min(d[i - 1][j] + deletion_cost, d[i][j - 1] + insertion_cost, d[i - 1][j - 1] + better_keyboard_distance(s[i], t[j])) + 1

  return d[first_len - 1][second_len - 1]

def main():
  args = sys.argv[1:]

  if len(args) != 2:
    print 'Usage: python spellcheck.py <fileToBeSpellChecked> <DictionaryOfWords>'
    sys.exit(1)

  filename = args[0]
  dict_word_list = args[1]

  words = [] 
  typos = []
  true_words = []
  with open(dict_word_list, 'r') as word_dict_file:
    words = [line.strip() for line in word_dict_file]

  with open(filename, 'r') as target_file:
    for line in target_file:
      typos.append(line.split('\t')[0].strip())
      true_words.append(line.split('\t')[1].strip())

  random_indices = random.sample(range(1, len(typos)), 100)
  random_typos = [ typos[i] for i in random_indices ]
  random_true_words = [ true_words[i] for i in random_indices ]

  # By default, we measure error on a random subset of 100
  measure_error(random_typos, random_true_words, words)
  # To measure error on the entire data set, comment out the code below:
  # measure_error(typos, true_words, words)


if __name__ == '__main__':
  main()

