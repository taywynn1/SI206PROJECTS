import os
import filecmp
from datetime import date

def getData(file):
	fname = open(file, 'r')
	l = list()
	(first,last,email,age,DOB) = fname.readline().strip().split(',')
	for line in fname:
		lines = line.strip().split(',')
		#print (lines)
		d = dict()
		d[first] = lines[0]
		d[last] = lines[1]
		d[email] = lines[2]
		d[age] = lines[3]
		d[DOB] = lines[4]
		
		#print (d)
		l.append(d)
	return l
	
#Input: file name
#Ouput: return a list of dictionary objects where 
#the keys will come from the first row in the data.

#Note: The column headings will not change from the 
#test cases below, but the the data itself will 
#change (contents and size) in the different test 
#cases.


#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName
	sorted_data = sorted(data, key = lambda x: x[col])
	first = (sorted_data[0]['First'])
	last = (sorted_data[0]['Last'])
	return (first + " " + last)

#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g 
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
	d = dict()
	for each in data:
		class_size = each['Class']
		if class_size in d:
			d[class_size] += 1
		else:
			d[class_size] = 1 
	l = list()
	for key, value in d.items():
		l.append((value,key))
	l.sort(reverse = True)

	new_list = list()
	for val,key in l:
		new_list.append((key,val))
	return (new_list)

# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	d = dict()
	for each in a:
		date_of_birth = each['DOB'].split('/')
		day = date_of_birth[1]
		#print (day)
		if day in d:
			d[day] += 1
		else:
			d[day] = 1
	l = list()
	for key, value in list(d.items()):
		l.append((value,key))
	l.sort(reverse=True)

	for val, key in l[:1]:
		return int(key)

# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest 
# integer.  You will need to work with the DOB to find their current age.
	l = list()
	today = date.today()
	for each in a:
		age = each['DOB'].split('/')
		month = int(age[0])
		day = int(age[1])
		year = int(age[2])
		actual_age_year = today.year - year 
		if today.month < month:
			actual_age_year -= 1
		elif ((today.month == month) and (today.day < day)):
			actual_age_year -= 1
		l.append(actual_age_year)
	average_age = sum(l) / len(l)
	rounded_age = round(average_age)
	return (rounded_age)
	

#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None
	sorted_data = sorted(a, key = lambda x: x[col])
	#print(sorted_data)
	outfile = open(fileName, "w")
	l = list()
	for d in sorted_data:
		tup = (d["First"], d["Last"], d["Email"])
		l.append(tup)
	for x in l:
		outfile.write(''"{}"','"{}"','"{}"',\n'.format(*x))
	return outfile


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)
	
	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()

