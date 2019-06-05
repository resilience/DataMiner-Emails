from selenium import webdriver as webdriver1
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
import tkinter as tk1
import tkinter.filedialog
import csv as csv1
import os as os1
import sys as sys1
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

##################################
########REDACTION#######
#################################

start = time.time()

# variables
i1 = 0
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-gpu')
chrome_options.add_argument('window-size=1900,1080')

dt = str(datetime.datetime.today().strftime("-%B %d %Y "))
startHour = str(datetime.datetime.today().strftime("%H "))
root = tk1.Tk()
root.withdraw()

dstatus = 0

# --- AUTO LOADER -----------------------------------------------------------------------
# this segment asks for current cores' input file location,
# Version 1 : input file has to be manually cut into appropriate pieces to allow multiprocessing
#             input file x is then opened by Autoloader to automatically load in every line

# Version 2 : Revamped Regex to be more accurate (removes outputs like nr@seen or nr@error)
#             Sticks to * @ * . * format

# FUTURE REVISION :      Amend: Currently Thread 1 - 7 are on [14] when it should be [13]
#                        Remove : First item on first list for Thread 1 has an invisible character sometimes
#                        Include: removal of h from code
#                        Include: IF website == previous website, output previous value, skip.
#                                       (should save a lot of time and quota)
#


file_path1 = tk1.filedialog.askopenfilename(initialdir='C:/Users/dmare/Dropbox/Hunt/
##################################
########REDACTION#######
#################################',
                                            title="Select file", filetypes=[("ALL Files", "*.*")])
counter = 0
tally = 0
avgTime = 0
timeSum = 0
timeTaken = 0
reader = csv1.reader(sys1.stdin)
startline = 0
endline = 0


# Temporary Storage created below :  HuntStorage-x.csv
# This is used to remove blanks and create a file, acting as a short term backup, and an isolated state between
# The input file and the working code.
# It's essentially 'n clone that we can safely rip apart for parts.

# FUTURE:

# FILE NAMES --------------
thread = 1
output = 'emails output' + dt + ' ' + "thread " + str(thread)
storage = 'HuntStorage thread '+str(thread)+'.csv'
regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
with open(file_path1, encoding='utf8', errors='surrogateescape') as input1, open(storage, 'w',
                                                                                 encoding='utf8') as output1:
    non_blank1 = (line for line in input1 if line.strip())
    output1.writelines(non_blank1)
with open(storage, encoding='utf8') as f1:
        row_count = sum(1 for row in f1)
        print(row_count, ' rows')
with open(storage, encoding='utf8') as f1:
    # ------- LOAD IN CSV FILES, LINE BY LINE ----------

    for line1 in f1:

        print(line1)

        line1 = line1.replace('"', '')
        line1 = line1.replace(' ', '')

        try:
            web = line1
            counter = counter + 1
            print(line1)
            print('NEXT SITE : ')
            startline = time.time()
            code = web[:14]
            print(code)
            line1 = web[14:]  # website

            line1 = line1.replace('http://', '')
            line1 = line1.replace('ttp://', '')
            line1 = line1.replace('ttps://', '')
            line1 = line1.replace('https://', '')
            print('line1 before addition: ', line1)
            line1 = 'http://' + line1

            print('website: (line1)', line1, 'end')
            if line1.strip() == 'http://' or line1 == 'https://':
                print('skipping')
                with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                    thewriter1 = csv1.writer(d1, delimiter='|')

                    thewriter1.writerow([code, '1 empty'])
                    timeTaken = endline - startline

                    timeSum = timeSum + timeTaken
                    avgTime = timeSum / counter
                    print('this loop took : ', timeTaken, ' seconds')
                    print('On Average loops are taking : ', timeSum / counter, ' seconds')
                    print('Estimate remaining time : ', avgTime * row_count, ' seconds')
                continue
            driver1 = webdriver1.Chrome(options=chrome_options)
            dstatus = dstatus + 1
            print(dstatus, ' drivers active')

            print(' ACCESSING WEBSITE: --> ', line1)
            driver1.get(line1)
            print('      Saving page source')
            doc = driver1.page_source
            time.sleep(1)
            # \.[a-zA-Z0-9-.]+$
            emailfirst = re.findall(regex, doc)

            try:

                print('New REGEX email: ', emailfirst[0])
                emailfirst = emailfirst[0]
            except IndexError as indexError:
                print('index error for email')

            # with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
            # thewriter1 = csv1.writer(d1, delimiter='|')

            # thewriter1.writerow([code, line1, emailfirst])
            print('      Saving emails found on page source')
            i1 = i1 + 1
        except (InvalidArgumentException, WebDriverException, ElementNotVisibleException) as y1:
            print('error', y1)
            with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                thewriter1 = csv1.writer(d1, delimiter='|')
                thewriter1.writerow([code, '2 empty'])
                timeTaken = endline - startline

                timeSum = timeSum + timeTaken
                avgTime = timeSum / counter
                print('this loop took : ', timeTaken, ' seconds')
                print('On Average loops are taking : ', timeSum / counter, ' seconds')
                print('Estimate remaining time : ', avgTime * row_count, ' seconds')
            continue
        print('navigating to contact page')

        try:
            contactpage1 = driver1.find_element_by_xpath('//a[contains(@href, "contact")]')
            print('pointing Driver to Contact Page')
            cplink1 = contactpage1.get_attribute('href')
            print(cplink1)
            try:
                contactpage1.click()
                doc = driver1.page_source
                emailcontact = re.findall(regex, doc)

                try:

                    print('Contact Page email: ', emailcontact[0])
                    emailcontact = emailcontact[0]
                except IndexError as indexError:
                    print('No Email in List')

                with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                    thewriter1 = csv1.writer(d1, delimiter='|')

                    thewriter1.writerow([code, line1, emailcontact])

            except (ElementNotInteractableException, ElementClickInterceptedException, ElementNotVisibleException,
                    WebDriverException) as e1:
                try:
                    with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                        thewriter1 = csv1.writer(d1, delimiter='|')

                        thewriter1.writerow([code, line1, emailfirst])
                        print('Contact Email failed - trying to output first page email')
                except NameError:
                    with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                        thewriter1 = csv1.writer(d1, delimiter='|')
                        thewriter1.writerow([code, '3 empty'])
                        print('outputting failed - first page email empty')
                    pass

            # BACKING UP CONTACT PAGE HTTP LINKS:
            # saves all contact page links to _cplink x output.csv_ file
            # APPENDS: HTTP LINK, CONTACT PAGE HTTP LINK, LINE NUMBER

            with open('' + dt + ' cplink 1 output.csv', 'a', newline='', encoding='utf8') as g1:
                thewriter1 = csv1.writer(g1, delimiter='|')

                thewriter1.writerow([line1, cplink1, i1, doc])

        except NoSuchElementException as ee1:
            print('error', ee1)

            try:
                contactpage1 = driver1.find_element_by_xpath('//a[contains(@href, "contact-us")]')
                print('pointing Driver to Contact US Page')
                cpuslink1 = contactpage1.get_attribute('href')
                #
                #         NAVIGATES TO CONTACT_US PAGE
                #         COLLECTS AND OUTPUTS EMAIL DATA

                try:
                    contactpage1.click()
                    doc = driver1.page_source
                    emailsold = re.findall(regex, doc)

                    try:

                        print('Contact US email: ', emailsold[0])
                        emailsold = emailsold[0]
                    except IndexError as indexError:
                        print('index error for email')

                    with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                        thewriter1 = csv1.writer(d1, delimiter='|')

                        thewriter1.writerow([code, line1, emailsold])
                except (ElementNotInteractableException, ElementClickInterceptedException, ElementNotVisibleException,
                        WebDriverException) as e1:
                    endline = time.time()
                    print('this loop took : ', endline - startline, ' seconds')
                    print('error', e1)
                    try:
                        with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                            thewriter1 = csv1.writer(d1, delimiter='|')

                            thewriter1.writerow([code, line1, emailfirst])
                            print('contact US email error - trying to output first page email')
                    except NameError:
                        with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                            thewriter1 = csv1.writer(d1, delimiter='|')
                            thewriter1.writerow([code, '4 empty'])
                            print('outputting failed - line empty')
                        pass

                    pass
                print(cpuslink1)
                with open('core1' + dt + '-cpus1linkoutput.csv', 'a', newline='', encoding='utf8') as h1:
                    thewriter1 = csv1.writer(h1, delimiter='|')

                    thewriter1.writerow([line1, cpuslink1, i1])
            except (NoSuchElementException, UnexpectedAlertPresentException) as d1:
                print("couldn't find a contact page on", line1, "row", i1)
                endline = time.time()
                timeTaken = endline - startline

                timeSum = timeSum + timeTaken
                avgTime = timeSum / counter
                print('this loop took : ', timeTaken, ' seconds')
                print('On Average loops are taking : ', timeSum / counter, ' seconds')
                print('Estimate remaining time : ', avgTime * row_count, ' seconds')
                with open(output + '.csv', 'a', newline='', encoding='utf8') as d1:
                    thewriter1 = csv1.writer(d1, delimiter='|')

                    thewriter1.writerow([code, '5 empty'])
                    driver1.quit()
                    dstatus = dstatus - 1
                continue

        # -----------------------------------------------------
        # ENDS THE CURRENT WEBDRIVER SESSION
        # THEN LOOPS BACK FOR LINE IN LINES TO CREATE NEW WEBDRIVER SESSION
        endline = time.time()

        timeTaken = endline - startline

        timeSum = timeSum + timeTaken
        avgTime = timeSum / counter
        print('this loop took : ', timeTaken, ' seconds')
        print('On Average loops are taking : ', timeSum / counter, ' seconds')
        print('Estimate remaining time : ', avgTime * row_count, ' seconds')
        print('Estimate remaining time : ', avgTime * row_count / 60 / 60, ' hours')
        print('Starting Hour was ', startHour)
        print('Ending Time should he in: ', avgTime * row_count / 60 / 60 / 24, ' days')

        cplink1 = ''
        driver1.quit()
        dstatus = dstatus - 1

# ------------------------------------------------------
# NO ACTUAL END OF PROGRAM SPECIFIED WHEN LINE IN LINES COMPLETED

end = time.time()
print(end - start)
