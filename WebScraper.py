__author__ = 'Richard Fry'


import urllib2
import re
from bs4 import BeautifulSoup
import csv
import unicodedata

##http://www.burrows.co.uk/scripts_AA/db4_IBAA_09.dll/next_prev?PAGE=0&SID=40598917
##http://www.buburrows.co.uk/scripts_AA/db4_IBAA_09.dll/sf?who=**&what=&where=e.g.:+Lancaster+Road&sortby_=name&Searchbutton=Search&whatfrompopup=&SID=40598917

headers = ""
Companies = []

##Query the server to get the search results from the database
URL = "http://www.burrows.co.uk/scripts/db4_ibaa_09.dll/setdb?database=307928"
connection = urllib2.urlopen(URL)
HTML = connection.read()
connection.close()

soup = BeautifulSoup(HTML)


#print(soup.prettify())


SID = soup.find_all("input")

SessionID = SID[8].attrs['value']

DatabaseURL = "http://www.burrows.co.uk/scripts_AA/db4_IBAA_09.dll/sf?SID={0}&Searchbutton=Search&sortby_=name&what=e.g.%3A%20bank&whatfrompopup=&where=e.g.%3A%20Lancaster%20Road&who=**".format(SessionID)

connection2 = urllib2.urlopen(DatabaseURL)
HTML2 = connection2.read()
connection2.close()

DB_Soup = BeautifulSoup(HTML2)

records = DB_Soup.find_all("p", {"class":"bodytext"})

record_number = re.sub("[^0-9]", "", records[0].text)

maxPages = int(record_number) / 15
pageNo = 0

print("{0} pages to process, processing page {1}".format(maxPages, pageNo))



while pageNo <= maxPages:

    table_rows = DB_Soup.find_all("a", {"class":"atable"})

    for row in table_rows:
        href = row.attrs['href']
        name = str(unicodedata.normalize('NFKD', row.contents[0]).encode('ascii', 'ignore'))
        #print("Processing {0}.....".format(name))
        CompanyURL = "http://www.burrows.co.uk" + href
        try:
            connection3 = urllib2.urlopen(CompanyURL)
        except:
            connection3 = urllib2.urlopen(CompanyURL)
        finally:
            connection3 = urllib2.urlopen(CompanyURL)
        HTML3 = connection3.read()
        connection3.close()
        #print("Sucessfully retrieved details for {0}...".format(name))

        Company_Soup = BeautifulSoup(HTML3)
        #print("Processing data...")
        Table_Labels = Company_Soup.find_all("td", {"class": "labeltxt"})

        if headers == "":
            for row in Table_Labels:
                headers += row.text + ','
            with open("TravelToWork.csv", "wb") as f:
                writer = csv.writer(f)
                writer.writerows(headers)





        companyDetails = ""
        pattern = re.compile("[\r\n]", re.MULTILINE)
        Table_Details = Company_Soup.find_all("td", {"class": "entrytxt"})
        for detail in Table_Details:
            if not detail.text.strip() == '':
                companyDetails += detail.text + ','

            else:
                companyDetails += ','
        try:
            companyDetails = re.sub(pattern, ",", unicodedata.normalize('NFKD', companyDetails).encode('ascii', 'ignore'))
        except:
            print(companyDetails)
        Companies.append([companyDetails])

        #print("Processing complete....")


    print("Processed page {0}".format(pageNo))



    pageNo += 1
    with open("TravelToWork.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(Companies)

    Companies = []

    DatabaseURL = "http://www.burrows.co.uk/scripts_AA/db4_IBAA_09.dll/next_prev?PAGE={0}&SID={1}".format(pageNo,SessionID)

    connection2 = urllib2.urlopen(DatabaseURL)
    HTML2 = connection2.read()
    connection2.close()

    DB_Soup = BeautifulSoup(HTML2)


print(headers)



