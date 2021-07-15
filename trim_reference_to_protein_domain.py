user1 = input('What is the name of the input file?  ')
user2 = input('What is the delimiter to separate the accession from the fragment start/end?  ')
user3 = input('What is your out file?   ')
#open the fasta file 
f = open(user1, 'r')
in_f = f.readlines()
f.close() 

#make a dictionary of the fasta file 
in_dict = dict()
key = ""


for line in in_f:
	if line.startswith('>'):
		key = line.strip()
		in_dict[key] = ""
	else:
		in_dict[key] += line.strip()

#pull split key into accession and fragment start/end
#make out dict to pull that size of string out 
out_dict = dict()

for header in in_dict:
	#This gives the cooridnates as a list
	#start needs to be one less

	coordinates = header.split(user2)[1].split('-')

	out_dict[header.split(user2)[0]] = in_dict[header][int(coordinates[0]):int(coordinates[1])]

#write to an out file 
o = open(user3, 'w')

for header in out_dict: 
	o.write(header)
	o.write('\n')
	o.write(out_dict[header])
	o.write('\n')

quit()