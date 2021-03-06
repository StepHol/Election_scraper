--- ELECTION SCRAPER ---

This project scrapes 2017 election data from the Czech Satistical Office web
for one chosen district. It is using Beautiful Soup 4. Data are saved into CSV file.

--- Instalation ---

Before running the script please install appropriate versions of libraries 
which are listed in 'requirements.txt' file.

$ pip3 --version                        # check pip manager version
$ pip3 install -r requirements.txt      # install libraries in requirements.txt

--- Usage ---

Open Election_scraper script, copy district url to the 'district_url' variable.
To the 'dictrict_file' write the name of the file where you want to store scraped data.

For example:

$ python election_scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'results_prostejov.csv'

--- Output ---

Script saves the results in the csv file in your current directory.
The file can be imported to your spreadsheet editor.

Here is an example of the output (the header and top 3 rows):

code,name,voters,envelopes_issued,voter_turnout,valid_votes,...
506761,Alojzov,205,145,"70,73",144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589594,Kladky,289,140,"48,44",140,7,3,0,17,0,2,17,0,3,2,0,2,9,0,3,30,0,0,24,1,0,1,1,17,1
589926,Protivanov,805,549,"68,20",547,45,0,0,59,1,15,52,2,4,5,1,0,31,0,5,144,0,1,101,0,10,1,2,68,0