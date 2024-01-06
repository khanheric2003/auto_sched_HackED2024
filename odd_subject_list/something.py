import re

string = ""
# Split the string into lines

course_numbers = re.findall(r'\b\d+\b', string)

with open('course_numbers.txt', 'w') as file:
    for number in course_numbers:
        file.write(number + '\n')
