#! /usr/bin/python
# Hash Identifier v1.0
# Made by Bart Bruininks and Tristan Moorlag

import numpy as np
import re

with open('search-hash.txt', 'r') as f:
	query = f.readlines()

#Preparing the file
with open('hash-file.csv', 'r') as f:
	raw_document = f.readlines()

with open('formatted-hash-file.csv', 'w') as f:
	for line in raw_document:
		if len(line.split(',')) == 3:
			f.write(line)

#Reading the file
data = np.genfromtxt('formatted-hash-file.csv', str, delimiter=',')
#Some preprocesing
hashmodes, hashnames, hashexamples = (data[:,0], data[:,1], data[:,2])

#functions
def hash_blast(data):
	"""
	Takes a 1D array(str) and returns its hash characteristics
	in an array.
	[len, ints_only, ints, alps_any, alphs, ALPHS]
	"""
	len_array = np.zeros([len(data), 6])
	for idx in range(len(data)):
		len_array[idx][0] = len(data[idx]) #length
		len_array[idx][1] = data[idx].isdigit() #ints
		len_array[idx][2] = bool(re.search('[0:9]', data[idx])) #contains ints
		len_array[idx][3] = bool(re.search('[a-zA-Z]', data[idx])) #aplhs
		len_array[idx][4] = bool(re.search('[a-z]', data[idx])) # alphs_a
		len_array[idx][5] = bool(re.search('[A-Z]', data[idx])) #ALPHS_A
	return len_array

# Here we write the files to text so we make sure all formatting is the same
# its ugly, but its works
template = hash_blast(query)
np.savetxt('template_temp.dat', template)
np.savetxt('data_temp.dat', hash_blast(hashexamples), delimiter = ' ')

with open('data_temp.dat') as f:
	stored_data = f.readlines()
for idx, line in enumerate(stored_data):
	stored_data[idx] = line.strip()

with open('template_temp.dat') as f:
	stored_template = f.readlines()
for idx, line in enumerate(stored_template):
        stored_template[idx] = line.strip()

# Here we actually make the comparision between the query and the reference
# library.
# and a nice print.
hit_list = []
hit_idx = 0
while True:
	try:
		hit_idx = stored_data[hit_idx:].index(stored_template[0])
	except ValueError:
		break
	if hit_idx not in hit_list:
		hit_list.append(hit_idx)
	else:
		break

for hit in hit_list:
	print("The hasmode is {} and the hashname is {}".format(hashmodes[hit_idx], hashnames[hit_idx]))
