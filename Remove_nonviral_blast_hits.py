#Date: 10.21.2020

#Purpose: Pull accessions/blast table rows that the subject protein taxonomy 
#is within a specific group 

#imports 
import os 
import csv

#user inputs 
blast_table_input = input('What is the name of the blast table file?   ')
taxonomy_list_input = input('What is the name of the taxonomy list file?   ') 

#create an output_directory based on blast_table input name 
out_path = os.getcwd() + '/' + blast_table_input.strip('.txt') + '_out'

count = 1
while os.path.isdir(out_path) == True:
	out_path += '_' + str(count)
	count = count + 1

os.mkdir(out_path)

#open the entire blast table file 
#and make a smaller blast table for just top hits
#write the smaller blast table to an outfile 
blast_table_top_hit = []
#add accessions of the query to a set
#and only add new lines to blast table if not
#found in the set 
seen = set()

with open(blast_table_input,'r') as f:
	for line in f: 
		#split line into list 
		line_data = line.strip().split('\t')
		#check to see if query in seen set
		if line_data[0] not in seen:
			#add query to set
			seen.add(line_data[0])
			#add whole line to make smaller blast table
			blast_table_top_hit.append(line_data)

#write smaller blast table to out

#create out name based on blast_table_input
out_top_hits_full_name = blast_table_input.strip('.txt') + '_all_top_hits.txt'

#write to a temp file first, then write to actual out
#this removes spaces in between lines with csv.writer
with open('temp.txt','w') as o: 
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(blast_table_top_hit)

#write to actual file
with open(os.path.join(out_path,out_top_hits_full_name),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			#if line is not just empty write
			#to out file
			if line != '\n':
				o.write(line)

#delete temp file
os.remove('temp.txt')

#open file with list of taxonomy and store as a set
taxonomy_of_group = set()

if taxonomy_list_input == 'bacteria.txt' or 'viruses.txt':
	with open(taxonomy_list_input,'r',encoding='UTF8') as f: 
		for line in f: 
			taxonomy_of_group.add(line.strip())
else:
	with open(taxonomy_list_input,'r') as f: 
		for line in f: 
			taxonomy_of_group.add(line.strip())

#split blast_table_top_hit table into two
#those with subjects found in accession list
#and those that do not 
found_in_taxonomy_list = []
found_in_query_names = []
not_found_in_taxonomy_list = []

taxonomy_of_found_in = set()
taxonomy_of_not_in = set()

for line in blast_table_top_hit:
	if len(line[13].split('[')) != 1:
		if line[13].split('[')[1].strip(']') in taxonomy_of_group:
			found_in_taxonomy_list.append(line)
			found_in_query_names.append(line[0])
			taxonomy_of_found_in.add(line[13].split('[')[1].strip(']'))
		else:
			not_found_in_taxonomy_list.append(line)
			taxonomy_of_not_in.add(line[13].split('[')[1].strip(']'))
#write to outfiles 

#create out name based on blast_table_input
out_top_hits_in_taxonomy_name = blast_table_input.strip('.txt') + '_top_hits_in_taxonomy_table.txt'

#write to a temp file first, then write to actual out
#this removes spaces in between lines with csv.writer
with open('temp.txt','w') as o: 
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(found_in_taxonomy_list)

#write to actual file
with open(os.path.join(out_path,out_top_hits_in_taxonomy_name),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			#if line is not just empty write
			#to out file
			if line != '\n':
				o.write(line)

#delete temp file
os.remove('temp.txt')

#create out name based on blast_table_input
out_top_hits_not_in_taxonomy_name = blast_table_input.strip('.txt') + '_top_hits_not_in_taxonomy_table.txt'

#write to a temp file first, then write to actual out
#this removes spaces in between lines with csv.writer
with open('temp.txt','w') as o: 
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(not_found_in_taxonomy_list)

#write to actual file
with open(os.path.join(out_path,out_top_hits_not_in_taxonomy_name),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			#if line is not just empty write
			#to out file
			if line != '\n':
				o.write(line)

#delete temp file
os.remove('temp.txt')

#write found in taxonomy 
queries_in_taxonomy_name = blast_table_input.strip('.txt') + '_in_taxonomy_query_names.txt'

with open(os.path.join(out_path,queries_in_taxonomy_name),'w') as o:
	for data in found_in_query_names:
		o.write(data)
		o.write('\n')


#search where each hit in the taxonomy comes from using taxonomy text files 
NCBI_directory = os.getcwd() + '/taxonomy_ncbi'

#get files in the NCBI_directory 
NCBI_files = os.listdir(NCBI_directory)


#for taxonomy found in and taxonomy not found in 
#parse through each NCBI file and find where it belongs 
tax_in_out = []

for taxonomy in taxonomy_of_found_in:
	out_tax = [taxonomy]
	#use count to say whether it was found in one or not 
	count = 0

	#go through each file and search for the name 
	for file in NCBI_files:
		data = set()
###################################################################
		if file == 'bacteria.txt' or 'virus.txt':
			with open(os.path.join(NCBI_directory,file), 'r', encoding='UTF8') as f:
				for line in f:
					data.add(line.strip())
		else:
			with open(os.path.join(NCBI_directory,file),'r') as f:
				for line in f:
					data.add(line.strip())
		if taxonomy in data:
			count = count + 1
			out_tax.append(file.strip('.txt'))
	if count == 0:
		out_tax.append('not found')

	tax_in_out.append(out_tax)

tax_not_out = []

for taxonomy in taxonomy_of_not_in:
	out_tax = [taxonomy]
	#use count to say whether it was found in one or not 
	count = 0

	#go through each file and search for the name 
	for file in NCBI_files:
		data = set()
		if file == 'bacteria.txt' or 'virus.txt':
			with open(os.path.join(NCBI_directory,file), 'r', encoding='UTF8') as f:
				for line in f:
					data.add(line.strip())
		else:
			with open(os.path.join(NCBI_directory,file),'r') as f:
				for line in f:
					data.add(line.strip())
		if taxonomy in data:
			count = count + 1
			out_tax.append(file.strip('.txt'))
	if count == 0:
		out_tax.append('not found')

	tax_not_out.append(out_tax)

#write taxonomy of things found in group and those not
subject_taxonomy_found = blast_table_input.strip('.txt') + '_subject_taxonomy_found.txt'

with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(tax_in_out)

with open(os.path.join(out_path,subject_taxonomy_found),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')

#write taxonomy of things found in group and those not
subject_taxonomy_not_found = blast_table_input.strip('.txt') + '_subject_taxonomy_not_found.txt'

with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(tax_not_out)

with open(os.path.join(out_path,subject_taxonomy_not_found),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')