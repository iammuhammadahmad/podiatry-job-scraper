import podiatry as podiatry
import proxy

def robotInfo():
    print("\n")
    print("       ===============================================================")
    print("       =               WELCOME TO Job SCRAPER :-)                    =")
    print("       = ----------------------------------------------------------- =")
    print("       = VERSION: 1.00                                               =")
    print("       = DATE: APRIL 30, 2023                                        =")
    print("       = DEVELOPER : MUHAMMAD AHMAD                                  =")
    print("       = heremuhammadahmad@gmail.com                                 =")
    print("       ===============================================================")
    print("\n\n")
    print("-------->>> JOB SCRAPER START... :-)\n")


def menu():
    print("FOLLOWING SITES ARE AVAILABLE TO SCRAPES!\n")
    print("1: PODIATRY.ORG.AU")


if __name__ == '__main__':
    start = True
    robotInfo()
    while start:
        menu()
        proxy_input = input("\n-> DEFAULT PROXY IS DISABLED.TO ENABLE WRITE (yes)? OR PRESS (ENTER) FOR DEFAULT SETTING: ")
        scrapeSite = int(input("\n-> SELECT SITE TO SCRAPE: "))

        if proxy_input !='yes':
           if scrapeSite == 1:
               jobsLinks=podiatry.getJobLinks()
               podiatry.scrapeJob(jobsLinks)
        else:
            if scrapeSite == 1:
                proxies = proxy.getProxies()
                jobsLinks = podiatry.getJobLinks(proxies=proxies)
                podiatry.scrapeJob(jobsLinks, proxies=proxies)
        
        isRun = input("\nDO YOU WANT TO RUN AGAIN THEN WRITE (yes)? TO CANCEL PRESS ANY KEYWORD: ")

        if isRun == 'yes':
            pass
        else:
            start = False
               
               



