# Analyzing my games at chess.com

I am an amateur chess player, love playing over the board when possible, but also enjoy playing casual games on chess.com.
Recently I discovered that chess.com has a very useful and easy to use API to retrieve different types of information, 
such as your own games (or games from any other user).

The goal of this project is to retrieve the information from my games played on chess.com using its API, clean and process the 
data collected and save it as useful information in `.csv` files, to then analyze and visualize any relevant trends or 
other among my games.

### The `api-processing.py` script

This script contains a few useful functions that will be used to retreive the data from chess.com API and process it to get
useable information. All if this will be explained in detail below. If you find it useful, feel free to fork the repo and
use it yourself!

#### Retreiving the information

This is done with the `requests` module, and the json obtained is passed into a pandas DataFrame. In this case, the 
url provided retreives information of the games played by a particular username id in a month, but many other things
can be obtained. The full API documentation can be found [here](https://www.chess.com/news/view/published-data-api).

#### Cleaning and processing the data

While the information provided by the API directly is useful, some things aren't and some other relevant ones are hidden. A simple 
`.csv` file with only the relevant information is desired for data analysis later, and this is done mainly using pandas, regex 
and a few helper functions. All the information about these can be found in the corresponding *docstrings*, and the final output is 
the mentioned `.csv` file, and an example header is shown below:

pieces | result | game\_ending | end\_time | moves | white\_rating | white\_accuracy | black\_rating | black\_accuracy | white\_seconds | black\_seconds | time\_control | time\_class |
----- | --- | -------- | ---------- | --- | --- | ----- | ---- | ----- | ----- | ----- | --- | -----
black | win | resigned | 1662018289 | 27 | 1217 | 54.62 | 1193 | 68.21 | 389.6 | 356.1 | 600 | rapid
white | loss | checkmated | 1662111628 | 51 | 1184 | 54.97 | 1139 | 60.36 | 208.4 |211.2 | 600 | rapid

### Exploratory data analysis of my games

This is an ongoing process! As soon as I have some visuals and trends to show about my games I will share with all of you.
