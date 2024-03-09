import os
import pandas as pd


# Function to process and store election results for a given file
def process_and_store_election_results(file_path, PVR):
    data = pd.read_csv(file_path)
    electoral_district_number = data['Electoral District Number/Numéro de circonscription'].iloc[0]
    election_results = data.groupby(['Candidate’s First Name/Prénom du candidat',
                                     'Candidate’s Family Name/Nom de famille du candidat',
                                     'Political Affiliation Name_English/Appartenance politique_Anglais']) \
        .agg(Total_Votes=('Candidate Poll Votes Count/Votes du candidat pour le bureau', 'sum')) \
        .reset_index()
    PVR[electoral_district_number] = election_results.to_dict(orient='records')


# Path to the results folder
results_folder_path = './results'

# Dictionary to store the election results
PVR = {}

# Process and store the election results for each CSV file in the results folder
for file_name in os.listdir(results_folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(results_folder_path, file_name)
        process_and_store_election_results(file_path, PVR)

# Print or save the PVR dataset as needed
print(PVR)

# Analysis 1: Total votes for each party across all electoral districts
party_votes = {}
for district in PVR.values():
    for result in district:
        party = result['Political Affiliation Name_English/Appartenance politique_Anglais']
        votes = result['Total_Votes']
        if party in party_votes:
            party_votes[party] += votes
        else:
            party_votes[party] = votes

# Print total votes for each party
print("Total votes for each party across all electoral districts:")
for party, votes in party_votes.items():
    print(f"{party}: {votes}")

# Analysis 2: Electoral districts with the highest voter turnout
district_turnout = {}
for district_number, results in PVR.items():
    total_votes = sum(result['Total_Votes'] for result in results)
    district_turnout[district_number] = total_votes

# Sort districts by turnout and get the top 10
top_districts = sorted(district_turnout.items(), key=lambda x: x[1], reverse=True)[:10]

# Print top 10 districts with highest voter turnout
print("\nTop 10 electoral districts with the highest voter turnout:")
for district_number, votes in top_districts:
    print(f"District {district_number}: {votes} votes")

# Total number of seats available
total_seats = 338

# Calculate the total votes across all parties
total_votes_across_parties = sum(party_votes.values())

# Calculate the number of seats for each party based on the proportion of votes received
party_seats = {}
for party, votes in party_votes.items():
    party_seats[party] = (votes / total_votes_across_parties) * total_seats

# Print the number of seats each party would win (rounded to the nearest whole number)
print("\nNumber of seats each party would win if seats were proportional to votes received:")
for party, seats in party_seats.items():
    rounded_seats = round(seats)
    if rounded_seats > 0:
        print(f"{party}: {rounded_seats} seats")

