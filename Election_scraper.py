import requests
from bs4 import BeautifulSoup
import csv


district_url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'
district_file = 'results_prostejov.csv' # Has to contain .csv filename extension.


def main(url: str, file_name: str) -> None:
    '''
    Validates district url and file name.
    Data scraped from the url are saved to the csv file.
    After succesful process function prints 'Saved'.
    '''
    validate_url(url)
    validate_name(file_name)
    print(write_to_csv(get_data(url), file_name))


def validate_url(text: str) -> None:
    if 'https://volby.cz/pls/ps2017nss/' not in text:
        print('URL is not valid')
        exit()


def validate_name(name: str) -> None:
    if '.csv' not in name:
        print('Output has to be a csv file')
        exit()


def get_data(scraped_url: str) -> list:
     
    result = []
    tables = soup_from_url(scraped_url).find_all('table')
    for table in tables:
        table_trs = table.find_all('tr')
        for tr in table_trs[2:]:
            row_tds = tr.find_all('td')
            row_hrefs = tr.find_all(href = True)
            if row_hrefs:                
                result.append({**basic_data(row_tds) , **detail_data(row_hrefs[0]['href'])})
    return result


def soup_from_url(requested_url: str):
    '''
    Send request to given url and parse the response 
    using BeautifulSoup.
    '''
    response = requests.get(requested_url)
    return BeautifulSoup(response.text, 'html.parser')


def basic_data(row_tds: 'bs4.element.ResultSet') -> dict:
    '''
    Returns dict containing code and name of the municipality.
    '''
    return {
        'code': row_tds[0].getText(),
        'name': row_tds[1].getText(),
    }



def detail_data(href: str) -> dict:
    '''
    Get soup from url with municipality detail informaton.
    Returns dict containing number of voters, envelopes issued, 
    voter turnout, number of valid votes 
    and number of votes for each party.
    '''    

    all_tds = soup_from_url(
        f'https://volby.cz/pls/ps2017nss/' + href
        ).find_all('td')  

    detail = {}
    detail['voters'] = all_tds[3].getText().replace('\xa0','')
    detail['envelopes_issued'] = all_tds[4].getText().replace('\xa0','')
    detail['voter_turnout'] = all_tds[5].getText()
    detail['valid_votes'] = all_tds[7].getText().replace('\xa0','')


    # Get number of votes for each party:
    i = 0
    while all_tds[10+i].getText() != '-': 
        detail[all_tds[10+i].getText()] = all_tds[11+i].getText().replace('\xa0','')
        i+=5

    return detail


def write_to_csv(data: list, file_name: str) -> str:
    try:
        csv_file = open(file_name, mode = 'w', encoding = 'utf-8', newline='')
        columns = data[0].keys()

    except FileExistsError:
        return traceback.format_exc()
    except IndexError:
        return traceback.format_exc()
    else:
        entry = csv.DictWriter(csv_file, fieldnames = columns)
        entry.writeheader()
        entry.writerows(data)
        return 'Saved'
    finally:
        csv_file.close()


if __name__ == "__main__":
	main(district_url, district_file)