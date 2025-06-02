'''
This file creates judge.csv and sum.csv which is used for analysis of this dataset
More details can be found in ../analysis
'''



import os

#creating sum.csv files
input_folder = "train-data/summary"  # Replace with the path to your folder containing text files
output_file = "sum.csv"  # Replace with the desired name of the output file

delimiter = "\t"  # You can change the delimiter to suit your needs

with open(output_file, "w") as f_out:
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            summary_name = os.path.splitext(filename)[0]  # Extract the name from the filename without extension
            with open(file_path, "r") as f_in:
                text = f_in.read().replace("\n", " ")  # Read the file contents and remove line breaks if needed
                row = f"{summary_name}{delimiter}{text}\n"
                f_out.write(row)

#Creating judge.csv files
input_folder = "train-data/judgement"  # Replace with the path to your folder containing text files
output_file = "judge.csv"  # Replace with the desired name of the output file

delimiter = "\t"  # You can change the delimiter to suit your needs

with open(output_file, "w") as f_out:
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            judgment_name = os.path.splitext(filename)[0]  # Extract the name from the filename without extension
            with open(file_path, "r") as f_in:
                text = f_in.read().replace("\n", " ")  # Read the file contents and remove line breaks if needed
                row = f"{judgment_name}{delimiter}{text}\n"
                f_out.write(row)

#Now as we have created two files, its time to zip these two files into one csvdataset.zip
#We have to do this because judge.csv was very large and was exceeding github's max limit

import pandas as pd
judgements = pd.read_csv('judge.csv',sep='\t',names=['filename','judgement'])
summaries = pd.read_csv('sum.csv',sep='\t',names=['filename','summary'])

dataset = pd.merge(judgements, summaries, on='filename')
dataset = dataset.dropna()

dataset.to_csv('dataset.csv', index=False)

# Now create dataset.csv which basically combines judge.csv and sum.csv
os.system("rm judge.csv")
os.system("rm sum.csv")
