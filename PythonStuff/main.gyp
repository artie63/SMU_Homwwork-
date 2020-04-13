
import csv


csvpath = "Resources/budget_data.csv"


totalMonths = 0
csvpath = "Resources/budget_data.csv"

totalProfit = 0


profitChanges = []
lastProfit = 0
currProfit = 0


rowCount = 0


with open(csvpath) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    csv_header = next(csvreader)
    print(f"CSV Header: {csv_header}")

    #Loop through rows
    for row in csvreader:
        #print(row)
        #increment total months
        totalMonths += 1

        #increment profit
        totalProfit += int(row[1])

        # calculate change
        if rowCount == 0:
            lastProfit  = int(row[1])
        else:
            currProfit = int(row[1])
            change = currProfit - lastProfit
            profitChanges.append(change) # add change to list
            lastProfit = currProfit

        rowCount += 1 # check to skip first profit change

# finished reading CSV

averageChange = sum(profitChanges) / len(profitChanges)

print(f"Total Months: {totalMonths}")
print(f"Total Profit: {totalProfit}")
print(f"Average Change: {averageChange}")