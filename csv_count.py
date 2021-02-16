import csv
import random

read_row = []
with open('items_list.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    item_amount = 0
    
    for row in csv_reader:
        print(len(row))
        print(row)
        read_row = row
# generate db
with open('db1.txt', mode='w', newline='') as db:
    db_writer = csv.writer(db, delimiter=',')
    print(len(read_row))
    for _ in range(20):
        x = random.randint(1,12)
        list = random.sample(range(30), x)
        print(list)
        transaction = []
        for num in list:
            #print("adding: " + read_row[num])
            transaction.append(read_row[num])
        #print("items per line" + str(x))

        db_writer.writerow(transaction)
        