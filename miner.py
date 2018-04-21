#!/usr/bin/env python

__author__ = "Tobia Valerio"
__license__ = "Apache License 2.0"
__version__ = "1.2"
__status__ = "Testing"

from splinter import Browser
import time


def time_to_stop():
    ''' Webserver resets at 02:00, therefore the script is automatically stopped if the time matches. 
    If the time is different from the one pointed above, False is returned.
    '''
    
    if time.strftime("%H") == "02" and time.strftime("%M") == "00":
        print('''
        ============================
        SERVER RESETTING: EXITING...
        ============================
        ''')
        return True
    else:
        return False


# NOTE: REQUIRES GECKODRIVER.EXE IN THE SAME FOLDER AS THE SCRIPT TO FUNCTION!
with Browser('firefox') as browser:

    browser.visit('http://bitcofarm.com/login')

    # ! LOGIN CREDENTIALS !
    un = ""
    pwd = ""

    browser.find_by_name("username").first.fill(un)
    browser.find_by_name("password").first.fill(pwd)
    # Still working on a CAPTCHA solver... It'll arrive Soon(TM)
    input("Press ENTER once the CAPTCHA has been solved: ")

    print("\nCaptcha solved. Loading ads page...")

    # Access Ads Page
    browser.visit('http://bitcofarm.com/ads')

    # Set Ads as current window
    window = browser.windows[0]

    # Get all adverts page links
    ad_links = browser.find_link_by_partial_href('modules/adview.php?ad=')

    print("Ads page loaded. Beginning ads viewing...\n")

    while True:

        # Iterate over adverts page links list and open them one by one
        for link in reversed(ad_links):
            # Get advert value
            advert_type = link.text[-21:-18]

            if "60" in advert_type or "30" in advert_type:
                browser.execute_script("window.open('{}');".format(link['href']))
                window = browser.windows[1]

                print("Viewing advert...")
                
                # Stand by for 55 seconds (30 and 60 pts adverts need this much time to be counted as viewed)
                time.sleep(55)
                window.close()
            else:
                # No ads that are worth 30 or 60 points found. Refreshing the page to gather new ones.
                print("================"
                      "NO VALUABLE ADS FOUND. REFRESHING..."
                      "================\n")
                break

            # Time check before continuing
            if not time_to_stop():
                print("Viewing complete. Moving on to next advert.\n")
            else:
                exit()

        browser.reload()
        ad_links = browser.find_link_by_partial_href('modules/adview.php?ad=')
