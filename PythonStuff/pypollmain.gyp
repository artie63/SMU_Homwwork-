#your code
import csv
csvpath = "Resources/election_data.csv"

totalVotes = 0 
csvpath = r"r Resource/election_data.csv"
listcandidates = []
#percentage of votes 
totalpercenatge = []
totalnumberwin = 0
totalnumberlose = 0
 

rowcount = 0 

# Open the CSV
with open(csvpath) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    csv_header = next(csvreader)
    print(f"CSV Header: {csv_header}")

#Loop through rows
    for row in csvreader:
        #print(row)
        #increment total months
        totalVotes += 1

        #increment profit
        listcandidates += int(row[1])

       # calculate change
        if rowcount == 0:
            totalnumberwin  = int(row[1])
        else:
            totalnumberlose = int(row[1])
            change = totalpercenatge - totalnumberwin
            totalpercenatge.append(change) # add change to list
            totalnumberwin = totalnumberlose

rowcount += 1


