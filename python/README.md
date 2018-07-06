## Environment
Set up the environment:
`$ virtualenv -p /usr/bin/python3 venv`
`$ source ./venv/bin/activate`

Install the package:
`$ pip install -e .`

## Running the code:
Set the right path and other document specific variables in `main.py`.
Run with: `$ python3 main.py`. 
Logs are in `main.log`.

## Input format:
See `python/data/input_format.csv`. 
You can generate with `Excel -> SaveAs -> .csv -> pick , delimiter`.  

## Fine tuning ga2
You can pick different ga2 parameters in `main.py try_ga2_runs`. Just add a tuple in `args_list`.  

## Possible improvements
Algorithm wise: speed. Calculating the cost function is time consuming. There might be a faster way to calculate scores (caching for nonchanged members etc.).  
After running a few times, certain groups tend to be overpopulated. I could modify input data ba removing some participants from the overpopulated groups and assigning participants to underpopulated ones. 
