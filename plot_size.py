import matplotlib.pyplot as plt
import os
import re

#Move to the correct directory
os.chdir("merged")

regex_number = "[0-9]+"

commit_numbers = []
byte_size_list = []

#Open the file that stores the commit numbers
file = open("../commit_numbers.txt", "r")

#The commit numbers are stored newest to oldest in the file.
#We want them in ordered from oldest to newest.
lines = file.readlines()
lines.reverse()
for line in lines:
	#Get the size of the repo directory for each commit
	os.system("git checkout %s" % line)
	output = os.popen("du -s merged").read()
	size = re.findall(regex_number, output)[0]

	#Add the size data to the list for plotting	
	byte_size_list.append(int(size))
	
	#Add the first 6 characters of the commit number for plotting
	commit_numbers.append(line[:6])

#Plot the data and save the plot
plt.bar(commit_numbers, byte_size_list, align="center")
plt.xticks(range(len(commit_numbers)), rotation="vertical")
plt.tight_layout()
plt.savefig("../directory_size_plot.png")
plt.show()
