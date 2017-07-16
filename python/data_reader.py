#!/usr/bin/python
import csv
import sys

def read_data17(path):
    print ("Reading data from %s." % path)
    participants = []
    activities = []
    participant_id = 0;
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if not row[0]:
                break
            if not activities:
                for i,act_name in enumerate(row[7:19]):
                    activities += [{
                        "name": act_name,
                        "id": i,
                        "count": 0}]
            else:
                par = { "id": participant_id,
                        "name": row[0],
                        "grade": int(row[1]),
                        "count": 1,
                        "pref": [],
                        "activities": []
                        }
                participant_id += 1
                for i,pref in enumerate(row[7:19]):
                    par["pref"] += [int(pref)]
                participants += [par]
        return (participants, activities)
    print ("Finished reading data.")

if __name__ == "__main__":
    p,a = read_data17("../data/delavnice_2017.csv")










