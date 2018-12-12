import csv

# with open('other_files/tweets.csv', newline='') as csvfile:
#     testreader = csv.reader(csvfile, delimiter='\t')

testreader = ['row 1', 'row 2']

with open('other_files/new_tweets.csv', 'a') as newcsv:
    testwriter = csv.writer(newcsv)

    for row in testreader:
        testwriter.writerow(row)
