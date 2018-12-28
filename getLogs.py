from Crawlers import EcmsCrawler
from Scraper import EcmsScraper
from Database import DBInterface


def main():
    projects = ['L00209','E04222' ]
    crawler = EcmsCrawler()
    print(crawler.base_url)
    crawler.navigate_to('http://www.dot14.state.pa.us/ECMS/')
    crawler.login('rwlawson', 'Prudent4life')
    crawler.navigate_to(
        'http://www.dot14.state.pa.us/ECMS/SVMHLSearch?action=SHOWMAINPAGE')
    db = DBInterface()
    scraper = EcmsScraper()
    # Iterate over each project grabbing needed logs
    for project in projects:
        crawler.go_to_cmh_logs(project)
        mhl_logs = scraper.scrape_log_search(crawler.current_page_source())
        for log in mhl_logs:
            crawler.navigate_to(crawler.root_url + log)
            crawler.navigate_to(
                "http://www.dot14.state.pa.us/ECMS/PDTagServlet?action=printerFriendly&jspName=WEB-INF/jsp/MHLmanageInspectorLog.jsp")
            INSPECTOR = scraper.scrape_inspector_name(
                crawler.current_page_source())
            labor_data, mileage_data = scraper.scrape_inspector_log(
                crawler.current_page_source())
            # ADD EACH ROW OF DATA TO THE RESPECTIVE DB
            for labor_row in labor_data:
                db.add_to_hours(labor_row, INSPECTOR, project)
            for mileage_row in mileage_data:
                db.add_to_mileage(mileage_row, INSPECTOR, project)
            # print(labor_data, INSPECTOR, project)
            # print(mileage_data)
            # break
            # db.add_to_mileage(mileage_data, INSPECTOR, project)
            # db.add_to_hours(labor_data, INSPECTOR, project)

    crawler.shutdown()


if __name__ == '__main__':
    main()
