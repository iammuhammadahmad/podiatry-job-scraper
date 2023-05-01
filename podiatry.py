import requests
from bs4 import BeautifulSoup
import random
import time
from google_sheet import GoogleSheet
import settings as config

# GET ALL JOBS FROM WEBSITE
def getJobLinks(proxies=None):
    jobsLinksList = []
    if proxies:
        randomProxy = random.choice(proxies)
        proxy = {'https':randomProxy}
        print("\nPROXY IS ENABLED: ", randomProxy)
        try:
            with requests.Session() as s:
                s.proxies.update(proxy)
                r = s.get(config.podiatry["BASE_URL"] + config.podiatry["BASE_URL_PATH"])
        except:
            # if catch any error then again make the request
            randomProxy = random.choice(proxies)
            print("\nRETRYING TO GET JOBS LINKS!\n")
            with requests.Session() as s:
                s = requests.Session()
                proxy = {'https': randomProxy}
                s.proxies.update(proxy)
                r = s.get(config.podiatry["BASE_URL"] + config.podiatry["BASE_URL_PATH"])
    else:
        try:
            r = requests.get(config.podiatry["BASE_URL"] + config.podiatry["BASE_URL_PATH"])
        except:
            # AGAIN REQUEST IF ANY ERROR
            print("\nRETRYING TO GET JOBS LINKS!\n")
            r = requests.get(config.podiatry["BASE_URL"] + config.podiatry["BASE_URL_PATH"])

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, features="html.parser")
        links = soup.select('#content-main > ul.records.clearfix > li')
        for link in links:
            try:
                jobsLinksList.append(config.podiatry["BASE_URL"] + link.find('a').get('href'))
            except:
                pass
        print("TOTAL JOBS LINKS: {}".format(len(jobsLinksList)))
        return jobsLinksList
    else:
        print("ERROR WHILE SCRAPING JOBS LINKS: ", r.status_code)

# SCRAPTE JOB'S DETAILS AND UPLOAD TO GOOGLE SHEET
def scrapeJob(jobsLinks, proxies=None):
    counter=1
    employer=''
    contact=''
    phone=''
    email=''
    jobType=''
    region=''
    closingDate=''
    for url in jobsLinks:
        if proxies:
            randomProxy = random.choice(proxies)
            print("\nPROXY IS ENABLED: ", randomProxy)
            try:
                with requests.Session() as s:
                    proxy = {'https': randomProxy}
                    s.proxies.update(proxy)
                    r = s.get(url)
            except:
                print("\nRETRYING TO GET JOB'S RECORD: ", url)
                with requests.Session() as s:
                    randomProxy = random.choice(proxies)
                    proxy = {'https': randomProxy}
                    s.proxies.update(proxy)
                    r = s.get(url)
        else:
            try:
                r = requests.get(url)
            except:
                # AGAIN REQUEST IF ANY ERROR
                print("\nRETRYING TO GET JOB'S RECORD!\n")
                r = requests.get(url)

        
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, features="html5lib")
            table_tr = soup.select('#content-main > section > table > tbody > tr')

            for tr in table_tr:
                th=tr.select_one('th').getText().strip()
                if th == "Employer":
                    employer = tr.select_one('td').getText().strip()
                if th == "Contact":
                    contact = tr.select_one('td').getText().strip()
                    contactList = contact.split(' ')
                    if len(contactList) == 1:
                        contactFirstName = contact
                        contactLastName = ''
                    else:
                        contactLastName = contactList[-1]
                        contactFirstName = contact.replace(contactLastName, '')
                if th == "Phone":
                    phone = tr.select_one('td').getText().strip()
                if th == "Email":
                    email = tr.select_one('td').getText().strip()
                if th == "Type":
                    jobType = tr.select_one('td').getText().strip()
                if th == "Job Region":
                    region = tr.select_one('td').getText().strip()
                if th == "Closing date":
                    closingDate = tr.select_one('td').getText().strip()
            
            # JOBS DETAILS SAVING INTO CSV File
            date_format = 'm/d/yy'
            if "/" in closingDate:
                closingDate = f'="{closingDate} {date_format}"'

           
            job={
                "Job URL": url,
                "Job Site": "Australian Podiatry Association",
                "Employer": employer,
                "Contact First": contactFirstName,
                "Contact Last": contactLastName,
                "Phone": phone,
                "Email": email,
                "Type": jobType,
                "Region": region,
                "Closing Date": closingDate,
                "Profession": "Podiatry"
            }

            # Saving to Google Sheet
            upload_record_google_sheet(config.podiatry["sheet_id"], config.podiatry["sheet_title"], job)
            print("\nCOMPLETED SITE: {}".format(counter))
            counter += 1
            time.sleep(2)

    print("\nTOTAL SCRAPED SITES: {}".format(counter))
# UPLOAD RECORD TO GOOGLE SHEET
def upload_record_google_sheet(sheet_id, sheet_title, job):
    # Google Sheet Object
    gs_obj = GoogleSheet()
    worksheet = gs_obj.worksheet(sheet_id, sheet_title)

    is_exist_job = gs_obj.isExist(worksheet, job)
    if is_exist_job:
        print("\nJOB ALREADY EXIST : ", job["Job URL"])
    else:
        gs_obj.add(worksheet, list(job.values()))