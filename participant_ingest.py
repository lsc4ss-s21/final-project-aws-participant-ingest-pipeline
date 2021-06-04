# Participant Ingest Script
# Large Scale Computing for the Social Sciences, Final Project
# Max Kramer

import csv
import argparse
from os import path

# fields to collect
FIELDS = ['First Name','Last Name','Date of Birth','Height','Weight','Gender Identity','Handedness','Email Address','Cell Phone Number','Preferred Language']

def dataFromParticipant(fromParticipant):
    '''
    Reads in a csv and amends its contents to the ingest CSV file.

    Inputs:
        fromParticipant: A CSV file 
    Returns:
        None: Modifies ingest_output.csv
    '''
    amend_to_ingest = []
    with open(fromParticipant, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file) # read in csv as dictionaries
        for row in csv_reader:
            amend_to_ingest.append(row) # append each row to the list
    
    output_writer(amend_to_ingest) # call output_writer to handle output


def dataEnteredByResearcher(num_participants_to_ingest):
    '''
    Prompts the user to enter each field in ingest_output.csv manually,
    creating a new row in the output file.

    Inputs:
        num_participants_to_ingest: The number of participants to be added
    
    Returns:
        None: Modifies ingest_output.csv
    '''
    amend_to_ingest = []

    for participant in range(num_participants_to_ingest):
        row = {} # intialize a row for the dictionary

        for field in FIELDS:
            print("Enter value for",field,": ",end="")
            fromUser = input() # collect value from participant
            row[field] = fromUser # update row
        amend_to_ingest.append(row) # add row to ingest_output
    
    output_writer(amend_to_ingest) # call output_writer to handle output


def output_writer(amend_to_ingest):
    '''
    Handles either the creation of ingest_output.csv or amends it.

    Inputs:
        amend_to_ingest: A list of dictionaries that form the rows

    Returns:
        None: Modifies ingest_output.csv
    '''
    if path.exists('ingest_output.csv'): # if file already exists, append to it
        with open('ingest_output.csv', mode='a',newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
            for row in amend_to_ingest:
                writer.writerow(row)

    else: # if not, create it
        with open('ingest_output.csv', mode='w',newline='') as csv_file: 
            writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
            writer.writeheader()
            for row in amend_to_ingest:
                print(row)
                writer.writerow(row)


def participantIngest():
    '''
    Depending on flags, either parse data entered by researcher or add participant
    data to ingest_output.csv

    Inputs: 
        None: Only takes CLI args

    Returns:
        None: Generates/Modifies ingest_output.csv
    '''
    parser = argparse.ArgumentParser() # instantiate CLI argument parser
    parser.add_argument("-m","--manual",action="store_true",help="Flag for manual input of participant data")
    args = parser.parse_args() # parse CLI arguments
    
    if args.manual:
        print("number of participants to manually add: ",end='')
        num_participants = input()
        dataEnteredByResearcher(int(num_participants))
    else:
        print("name of csv file to load in: ",end='')
        filename = input()
        dataFromParticipant(filename)

if __name__ == "__main__":
    participantIngest()