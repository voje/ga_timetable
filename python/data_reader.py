#!/usr/bin/python
import csv
import sys

def read_data16(self, path):
    par_id = 0
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if not self.activities:
                # if activities is uninitiated (first row of file)
                for i in range(0, len(row)):
                    self.activities += [{
                        "id": i,
                        "name": row[i],
                        "count": 0}]
            else:
                # else, add to participants
                for i in range(0, len(row)):
                    tmps = row[i]
                    sp = tmps.split(" ")
                    if (len(sp) < 2):
                        continue  # empty cell

                    grade = int(sp[0])
                    name = " ".join(sp[1:])
                    activity_id = i

                    if name not in self.participants:
                        self.participants[name] = {
                            "id": par_id,
                            "name": name,
                            "grade": grade,
                            "activities": [activity_id]}
                        par_id += 1
                    else:
                        self.participants[name][
                            "activities"] += [activity_id]

                    # update count in self.activities
                    self.activities[i]["count"] += 1

def read_data17(path):
    print ("Reading data from %s." % path)
    participants = []
    activities = []
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
                par = { "name": row[0],
                        "age": row[1],
                        "pref": [],
                        "act": []
                        }
                for i,pref in enumerate(row[7:19]):
                    par["pref"] += [pref]
                participants += [par]
        return (participants, activities)
    print ("Finished reading data.")

if __name__ == "__main__":
    p,a = read_data17("../data/delavnice_2017.csv")










