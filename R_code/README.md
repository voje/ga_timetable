# Timetable using a Genetic Algorithm
Kristjan Voje

## Task
There are approximately 111 participants, which I will organize into 11 different workshops. The event will take place for 4 days. Each day, all 11 workshops will be open simulateneously. Each participant has selected 4 workshops, that he will attend. For every workshop he has selected, I need to assign which day he will be taking it.  
The main restraint is that each participant can take only one workshop per day.  
I should also group participant so they would be roughly of the same age group. Age groups are represented as school grades from 1 to 9.

## Data representation
The data is encoded in a binary string (a chromosome).  
* N ... number of participants
* D ... number of days  

String length: N*D*4.

Each participant is represented with D days. Each day is represented with 4 bits. The 4 bits encode the ID of the workshop the participant is attending. This way we make sure, each participant is attending no more than 1 workshop per day.

## Results
It's a balance between group sizes and distribution of age inside grups. Table pretty5.csv was created by takking inco acount both factors equally.

