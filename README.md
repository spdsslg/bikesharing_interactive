# Bike Sharing Analysis (Jan–Jun 2017)

A small Python project to explore US bike-sharing data (Chicago, New York City, Washington) from Jan–Jun 2017.
It’s a **terminal-driven app**: you choose _city_, _month_ (or all), and _day of week_ (or all).
The program prints quick stats:
- most common month/day/start hour 
- most common stations 
- most common combination of start station and end station 
- total travel time, mean travel time 
- user types 
- user gender 
- user birth-year stats

**Program can also show charts, including**:
- Daily trips (with optional 7-day smoothing for readability)
- Hourly profile (0–23) for a given month and/or weekday

**Additionally two plots are saved to** `/out`:

- Comparison of mean of rentals number per 7 day window for three cities during Jan - Jun
- Comparison of median travel time per 7 day window for three cities during Jan - Jun

**Data columns expected in CSVs**: `Start Time`, `End Time`, `Trip Duration`, `Start Station`, `End Station`, `User Type`, `Gender`, `Birth Year`.

## Installation Instructions and Software Dependencies

**Requirements:**
- Python 3.11+
- pip

1) **Clone and enter the project**
```
git clone https://github.com/<you>/bikesharing_interactive.git
cd bikesharing_interactive
```

2) **Create & activate a virtual environment**

- macOS/Linux:
```
    python3.11 -m venv .venv
    source .venv/bin/activate
```

- Windows (PowerShell):
```
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
```

3) **Install dependencies from requirements.txt**
```
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

4) **Verify install**
```
python -c "import pandas, matplotlib; print('OK')"
```

## Common Usage Information

You already have an input loop that asks for **city / month / weekday**. After reading those, it is possible get a snippet of the raw data for each person from the `.csv` table, finally you can get a plot for the **city / month / weekday** that was chosen. Additionally, two graphs that are saved to `/out` can be redrawn.

**NOTE**: When code prompts for user input for month or day of the week, input format can be either
**numerical**:
- [1,2,...] or [01,02,...]

**or text** :
- for months
 [Jan, Feb, ..., All] or [January, February, ..., June, All] 
- for day of the week
 [Mon, Tue,..., All] or [Monday, Tuesday, ..., Sunday, All]

If the parameter is `all`, code will analyse all possible entries. `All months` means consider all months, `all days` of the week means consider all days.

Also, prompts are _case insensitive_.
For example, those two prompts are the same:
```
# First prompt
Enter a month you want to get data on (all, january, february...): 
01
Enter a day of the week you want to get a data on (all, monday, tuesday...): 
1

# Second prompt
Enter a month you want to get data on (all, january, february...): 
jan
Enter a day of the week you want to get a data on (all, monday, tuesday...): 
Monday
```


**CLI (interactive) run:**
```
# Example: run your script (replace with your actual entry point)
python ./bikeshare_2.py
```

The script will prompt for:

- City: chicago, new york city, washington
- Month: 1..6 or all
- Day of week (DOW): 1..6 (Mon=1 … Sun=6) or all

It prints summary stats to the terminal and asks user if they want to 
- See first 5 rows of raw data (formatted)
- Redraw generated charts under `out/`.
- See the graphical representation of the data

**Suggested visualizations per selection:**
To avoid messy or meaningless plots, visuals are based on the user’s filter:
- _month = all, dow = all_ or _month = specific, dow = all_
Count of Daily trips (7-day rolling mean)
- _month = all, dow = specific_ or _month = specific, dow = specific_
Hourly profile for that weekday in that month

