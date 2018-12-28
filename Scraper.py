from bs4 import BeautifulSoup
from Database import DBInterface
from format_helpers import *

# soup = BeautifulSoup(open('prntfE02430CMHLOGPage.html'), 'html.parser')


# print(soup.title)

# tdz = soup.findAll('td', class_=["headerbody1", "data"])
# print(tdz[2].text.strip())


class EcmsScraper():
    ''' perform different scrapes...'''

    def scrape_log_search(self, page):
        ''' return list of cmh urls that need to be scraped and added to db'''

        soup = BeautifulSoup(page, 'html.parser')
        links = []
        db = DBInterface()
        for link in soup.findAll('a'):
            if ("INSPECTOR_LOG_ID" in str(link)):
                # url for cmh log: print(link.get('href'))
                # get agreement number: print(link.parent.text?)
                # TODO CHECK THAT DATES BETWEEN START AND END ('td')4 and 5 NOT IN DB BEFORE ADDING
                # TODO CHECK WORK ORDER
                # approval status

                log_search_cols = link.parent.parent.findAll('td')
                if (log_search_cols[6].text.lower().strip() == 'approved'):
                    if db.anyHoursLogged(log_search_cols[3].text.lower().strip(), log_search_cols[4].text.lower().strip(), log_search_cols[5].text.lower().strip()):
                        
                    links.append(link.get('href'))
        return(links)

    def scrape_inspector_log(self, page):
        ''' Gather all rows of data and filter into labor or mileage. 

            return: labor and mileage data lists '''
        soup = BeautifulSoup(page, 'html.parser')
        labor_rows = []
        mileage_rows = []

        tablerow_classes = ['PDEvenRow', 'PDOddRow']

        for row_class in tablerow_classes:
            data_tablerows = soup.findAll('tr', class_=row_class)

            for tablerow in data_tablerows:
                tds = tablerow.findAll('td')
                # labor has 9 tds mileage has 13 so look for rows that match
                if len(tds) == 9:
                    labor_rows.append(clean_labor(tds[1].text.strip(), tds[2].text.strip(),
                                                  tds[5].text.strip(), tds[6].text.strip()))
                elif len(tds) == 13:
                    # date type miles
                    mileage_rows.append(
                        clean_mileage(tds[1].text.strip(), tds[2].text.strip(), tds[7].text.strip()))

        return [labor_rows, mileage_rows]

    def scrape_inspector_name(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        tds = soup.findAll('td', class_=["headerbody1", "data"])
        return(tds[2].text.strip())
