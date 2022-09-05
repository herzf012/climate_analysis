# climate_analysis
Analyzing the climate around Honolulu, Hawaii using Python and SQLAlchemy to perform basic climate analysis and data exploration of a climate database.

# climate.ipynb
This jupyter notebook pulls data from the 'hawaii.sqlite' database using SQLAlchemy and proceeds to:
- Use the last 12 months of data provided.
- Graphs the last 12 months of precipitation data.
- Provides summary statistics on the last 12 months of precipitation data.
- Determines how many weather stations there are.
- Determines the ranking and amount of observations of each weather station.
- Finds minimum, maximum, and average temperatures of the most active weather station.
- Generates a histogram of temperatures for the most active weather station using the last 12 months of temperature data.

# app.py
This python Flask API is used to:
- Returns a JSON of dates and their respective precipitations.
- Returns a JSON of weather stations.
- Returns a JSON of temperatures for the most active station with the last 12 months of data.
- Returns a JSON of minimum, maximum, and average temperatures on and after a given date.
- Returns a JSON of minimum, maximum, and average temperatures on and after a given date and on and before a given date.
