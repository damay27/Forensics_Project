import matplotlib.pyplot as plt
import os
import re

#Move the correct directory
os.chdir("merged")

regex = "[0-9]+ files changed"
regex_number = "[0-9]+"

commit_numbers = []
counts = []

#Open the file that stores the commit numbers
file = open("../commit_numbers.txt", "r")

#The commit numbers are stored newest to oldest in the file.
#We want them in ordered from oldest to newest.
lines = file.readlines()
lines.reverse()
for line in lines:
	#Read the number of changes for each commit
	os.system("git checkout %s" % line)
	output = os.popen("git show --stat").read()
	count = re.findall(regex, output)
	if len(count) != 0:
		count = count[0]
		count = re.findall(regex_number, count)[0]

		#Add the number of changes to the list for plotting
		counts.append(int(count))

		#Add the first 6 characters of the commit number for plotting
		commit_numbers.append(line[:6])

#Plot the data and save the plot
plt.bar(commit_numbers, counts, align="center")
plt.xticks(range(len(commit_numbers)), rotation="vertical")
plt.tight_layout()
plt.savefig("../file_change_plot.png")
plt.show()
