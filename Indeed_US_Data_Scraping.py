#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import time
from time import sleep
import pandas as pd
from random import randint

website = "https://www.indeed.com/"


print(website)
start_time = datetime.now()
print('Crawl starting time : {}' .format(start_time.time()))

job_list = ["data+analyst", "project+management", "business+analyst"]

job_position = []
application_links = []
job_titles = []
company_names = []
salary=[]
job_locations = []
application_types = []
publication_dates = []
scraping_dates = []
job_descriptions=[]

for job in job_list:
    job_position = job
    driver = webdriver.Chrome('C:/Drivers/network/chromedriver')

    driver.get(
            "https://www.indeed.com/jobs?q=" + job + "&l=United+States&start=0"
        )

    sleep(randint(7,10))
    print('Collecting data for "{}"...' .format(job))
    # First, get the number of jobs available
    job_number = driver.find_element_by_xpath("//div[@id='searchCountPages']").text
    print("Full text",job_number)
    # Calculating number of pages to be crawled (number of jobs available - number of jobs per page (here, 30))
    job_number = job_number.split(" ", 4)
    job_number = int(job_number[3].replace(',', ''))
    print("- Number of open positions : {}" .format(job_number))
    exact_page_nb = job_number / 15
    print("- Exact number of pages to be crawled : {}" .format(exact_page_nb))
    min_page_nb = job_number // 15
    print("- Minimum number of pages to be crawled : {}" .format(min_page_nb))

    
    if exact_page_nb > min_page_nb:
        page_nb = (min_page_nb) * 10
        pages = [str(i) for i in range(0, page_nb, 10)]
    else:
        page_nb = (min_page_nb - 1) * 10
        pages = [str(i) for i in range(0, page_nb, 10)]
        


    for page in pages:
        driver.get(
            "https://www.indeed.com/jobs?q=" + job + "&l=United+States&start=" + page
        )
        c_page = (int(page)/10)+1
        disp_page = driver.find_element_by_xpath("//div[@id='searchCountPages']").text
        disp_page = disp_page.split(" ")[1]
        d_page= int(disp_page)
        print(c_page)
        print(d_page)
    
        if c_page != d_page:
            continue
        
        sleep(randint(5, 12))

        # Locating job container
        all_cards = driver.find_elements_by_xpath("//div[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")

        for card in all_cards:

            # Collecting job link
            application_link = card.find_elements_by_css_selector('a')
            if not application_link:
                application_link = "Unknown"
                
            else:
                application_link = application_link[0].get_attribute('href')
            application_links.append(application_link)
            
            

            # Collecting job title
            job_title = card.find_elements_by_css_selector('a')
            if not job_title:
                job_title = "Unknown"
            else:
                job_title = job_title[0].text
            job_titles.append(job_title)

            # Collecting company name
            company_name = card.find_elements_by_css_selector('div.sjcl div span.company')
            if not company_name:
                company_name = "Unknown"
            else:
                company_name = company_name[0].text
            company_names.append(company_name)

            
            # Collecting job location
            job_location = card.find_elements_by_css_selector('.location.accessible-contrast-color-location')
            if not job_location:
                job_location = "Unknown"
            else:
                job_location = job_location[0].text
            job_locations.append(job_location)
            
            # Collecting application type (easy apply)
            application_type = card.find_elements_by_css_selector('.jobCardShelfContainer')
            if not application_type:
                application_type = "company's website"
            else:
                application_type = application_type[0].text
            application_types.append(application_type) 
            
            
            # Collecting publication date
            publication_date = card.find_elements_by_css_selector('span.date')
            if not publication_date:
                publication_date = "Undefined"
            else:
                publication_date = publication_date[0].text
            publication_dates.append(publication_date)
            
            # Collecting generated scraping time 
            scraping_dates.append(datetime.now())

    print('Crawling status for "{}" : Done' .format(job))
    print()

    driver.quit()



# In[6]:


len(job_locations)


# In[14]:


from selenium.common.exceptions import NoSuchElementException
#Description
for link in application_links:
    driver = webdriver.Chrome('C:/Drivers/network/chromedriver')
    driver.get(link) 
    try:
        jd = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
        job_descriptions.append(jd)
    except NoSuchElementException: 
        job_descriptions.append("Unknown")
    
    driver.quit()

tempdf= pd.DataFrame({'job_descriptions': job_descriptions})
tempdf.head()


# In[7]:


print('Crawling time : {}' .format(datetime.now() - start_time))
print('Dataframe successfuly created and exported')

# Dataframe creation
df = pd.DataFrame({'job_position':job_position,
'job_title': job_titles,
'company_name': company_names,
'job_location': job_locations,
'application_link': application_links,
'publication_date': publication_dates,
'application_type': application_types,
'scraping_date': scraping_dates,
'job_descriptions': job_descriptions                   
})


# In[8]:


#Save
df.to_csv(r'Path\FileName.csv') 


# +In browser window, goes page to page consecutively
# -Stops after 20 pages
# +All US
# 
