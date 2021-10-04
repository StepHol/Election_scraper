import requests
from bs4 import BeautifulSoup
import csv
import traceback
import sys

try:
    district_url = sys.argv[1]
    district_file = sys.argv[2]
except:
    print('Two arguments required: URL and output file name.')
    exit()


def main(url: str, file_name: str) -> None:
    '''
    Validates district url and file name.
    Data scraped from the url are saved to the csv file.
    After succesful process function prints 'Saved'.
    '''
    validate_url(url)
    validate_name(file_name)
    print(f'Accessing URL: {url}')
    district_tables = tables_from_url(url)
    status = write_to_csv(district_data(district_tables), file_name)
    print(status)


def validate_url(text: str) -> None:
    if 'https://volby.cz/pls/ps2017nss/' not in text:
        print('URL is not valid.')
        exit()
    elif '.csv' in district_url:
        exit()


def validate_name(name: str) -> None:
    if '.csv' not in name:
        print('Output has to be a csv file')
        exit()


def tables_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('table')


def district_data(district_tables: 'bs4.element.ResultSet') -> list:
    '''
    Returns data for each municipality in the district.
    '''
    result = []
    for table in district_tables:
        table_trs = table.find_all('tr')
        for tr in table_trs[2:]:
            row_tds = tr.find_all('td')
            if row_tds[0].text != '-':
                row_href = row_tds[0].find('a').get('href')
                mun_tables = tables_from_url(
                    f'https://volby.cz/pls/ps2017nss/' + row_href
                    )
                result.append({
                    **basic_data(row_tds),
                    **voters_info(mun_tables),
                    **votes_for_party(mun_tables)
                })
    return result


def basic_data(row_tds: 'bs4.element.ResultSet') -> dict:
    '''
    Returns dict containing code and name of the municipality.
    '''
    return {
        'code': row_tds[0].getText(),
        'name': row_tds[1].getText(),
    }


def voters_info(tables) -> dict:
    '''
    Returns number of voters, envelopes issued, voter turnout,
    and number of valid votes.
    '''
    detail = {}
    table_trs = tables[0].find_all('tr')
    row_tds = table_trs[2].find_all('td')

    detail['voters'] = row_tds[3].getText().replace('\xa0','')
    detail['envelopes_issued'] = row_tds[4].getText().replace('\xa0','')
    detail['voter_turnout'] = row_tds[5].getText()
    detail['valid_votes'] = row_tds[7].getText().replace('\xa0','')
    return detail

def votes_for_party(tables) -> dict:
    votes = {}
    for table in tables[1:]:
        table_trs = table.find_all('tr')
        for tr_tag in table_trs[2:]:
            row_tds = tr_tag.find_all('td')
            party = row_tds[1].getText()
            if party != '-':
                votes[party] = row_tds[2].getText().replace('\xa0','')
    return votes

  
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
        return f'Saved in file: {file_name}'
    finally:
        csv_file.close()


if __name__ == "__main__":
	main(district_url, district_file)