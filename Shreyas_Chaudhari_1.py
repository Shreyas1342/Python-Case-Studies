# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:59:40 2023

@author: Shreyas_Chaudhari
"""

#Q1
"""Download first 5 text files (Shakespeare’s plays) from the following URL using a python script:
http://www.textfiles.com/etext/AUTHORS/SHAKESPEARE/
Store these in a separate folder.
(Find the 5 URLs pointing to .txt files in the above page using code. Do not manually put any URL
other than the above mentioned one in the code.)"""

import urllib.request
import os
from bs4 import BeautifulSoup

# URL to the Shakespeare plays page
url = "http://www.textfiles.com/etext/AUTHORS/SHAKESPEARE/"

# create a folder named "shakespeare" to save the downloaded files
if not os.path.exists("shakespeare"):
    os.makedirs("shakespeare")

# fetch the HTML content of the page
response = urllib.request.urlopen(url)
html = response.read()

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# find all the links in the page
links = soup.find_all("a")

# counter to keep track of downloaded files
counter = 0

# iterate over the links and download the first 5 .txt files
for link in links:
    href = link.get("href")
    if href.endswith(".txt"):
        file_url = url + href
        file_name = href.split("/")[-1]
        file_path = os.path.join("shakespeare", file_name)
        urllib.request.urlretrieve(file_url, file_path)
        counter += 1
        if counter == 5:
            break

print("Finished downloading 5 text files.")




#Q2
#Get all { file name : { line number : number of words in the line } } combinations in a dictionary.

import os

# Define the folder containing the text files
folder = 'shakespeare'

# Initialize the dictionary to store the results
results = {}

# Iterate over the text files in the folder
for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        # Initialize the nested dictionary for the current file
        file_dict = {}

        # Open the file and iterate over its lines
        with open(os.path.join(folder, filename), 'r') as file:
            for i, line in enumerate(file):
                # Count the number of words in the line
                num_words = len(line.split())

                # Add the result to the nested dictionary for the current file
                file_dict[i+1] = num_words

        # Add the nested dictionary to the main dictionary
        results[filename] = file_dict

# Print the dictionary of results
print(results)



#Q3
#Find number of lines with more than 10 words in each file.

import os

# Define the folder containing the text files
folder = 'shakespeare'

# Initialize a dictionary to store the line counts for each file
line_counts = {}

# Iterate over the text files in the folder
for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        # Initialize the line counter
        line_count = 0
        
        # Open the file and iterate over its lines
        with open(os.path.join(folder, filename), 'r') as file:
            for line in file:
                # Count the number of words in the line 
                num_words = len(line.split())
                
                # Check if the number of words in the line is greater than 10
                if num_words > 10: 
                    line_count += 1 
        
        # Add the line count to the dictionary
        line_counts[filename] = line_count

# Print the line counts for each file
for filename, count in line_counts.items():
    print(f"{filename}: {count} lines with more than 10 words")



#Q4 & Q5
#Find number of words spoken by each character in all the plays.
#Find 10 most common words spoken by each character.

import re 
import os      

#changing working directories
os.chdir(r'C:\Users\Shreyas_Chaudhari\Desktop\logo\Python\shakespeare')
all_files = os.listdir() #listing all files in the folder 
result = {} # to store data of all files
for file in all_files:
    with open(file,'r') as f:
        text = f.read()
    
        #remove DRAMATIS PERSONAE and anything which is written in []
        new_text = re.sub(r"DRAMATIS.*?ACT I*",'',text, flags=re.DOTALL)
        clean_text = re.sub(r'\[.*?\]', '', new_text, flags=re.DOTALL)
    
        #remove title from play
        lines = clean_text.split('\n')
        title = lines[0] 
        new_lines = [line for line in lines if line != title]
    
        #remove lines that starts with ACT or  SCENE
        new_lines1 = [line for line in new_lines if not line.startswith('ACT') | line.startswith('SCENE')]
    
        #Extracting the character names
        characters = []
        for line in new_lines:
            if re.match(r"^[a-zA-Z]", line):
                index = line.find('\t')
                name = line[0:index]
                if name not in characters and name not in ('Both', 'BOTH', 'ALL', 'All'): 
                    characters.append(name)
    
        #create a dictionary which contains characters and all dialogues by that character
        char_dialogue = {} # Characters and all the dialogues as single string
        for char in characters:
            line_no=[] # getting the line number where dialogue of that character starts
            for i,line in enumerate(new_lines1):
                if line.startswith(char):
                    line_no.append(i)
        
            dialouge='' # all dialogues as single string
            for line in line_no:
                i = new_lines1[line].find('\t')
                dialouge = dialouge+' '+new_lines1[line][i+1:]
                next_line = line + 1
                # checking the condition if next is empty or dialogue in continuation or a new dialogue
                while len(new_lines1[next_line]) != 0 and len(new_lines1[next_line]) != 1 and (new_lines1[next_line][0] == '\t'):
                    new_index = new_lines1[next_line].find('\t')
                    dialouge = dialouge+' '+new_lines1[next_line][new_index+1:]
                    next_line +=1
                char_dialogue[char] = dialouge
                
                #count the number of words spoken by each charachter
                #Find 10 most common words spoken by each character.
                word_frequency = {} # no of words spoken by each character
                most_common_words ={}# 10 most common words spoken by each character
                
                for key,value in char_dialogue.items():
                        word_count = {} # word count of each word by character
                        words = value.split()
                        freq = len(words)
                        word_frequency[key] = freq
                    
                        for word in words:
                            if word in word_count:
                                word_count[word] += 1
                            else:
                                    word_count[word] = 1
                    # 10 most common words by character
                        top_10_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10] 
                        most_common_words[key] = top_10_words
                        result[file] = [word_frequency , most_common_words]
print(result)
                


"""
#Q6
Find the following information about each file and store in a single csv:
a. Size in bytes
b. Last modified datetime
c. Absolute path#"""     
   
import os
import csv
import datetime

# Folder to scan for files
folder_path = (r'C:\Users\Shreyas_Chaudhari\Desktop\logo\Python\shakespeare')

# CSV file to write to
csv_path = "file_info.csv"

# List to hold file info dictionaries
file_info_list = []

# Loop over all files in the folder
for file_name in os.listdir(folder_path):
    # Get absolute path to file
    file_path = os.path.join(folder_path, file_name)
    
    # Get file size in bytes
    file_size = os.path.getsize(file_path)
    
    # Get file last modified datetime
    mod_time = os.path.getmtime(file_path)
    mod_datetime = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
    
    # Add file info to list
    file_info_list.append({
        "file_name": file_name,
        "file_size": file_size,
        "mod_datetime": mod_datetime,
        "file_path": file_path
    })

# Write file info list to CSV file
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["file_name", "file_size", "mod_datetime", "file_path"])
    writer.writeheader()
    writer.writerows(file_info_list)
            
        
        
    




