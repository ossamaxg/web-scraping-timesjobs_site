
import requests
from bs4 import BeautifulSoup
import csv
import time

print('Plz put z skills u want to discard: ')
discarded_skill = input('> ')
print(f'Filtering out {discarded_skill} ...\n')
start = time.time()
page = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=')
def find_jobs(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    jobs_details = []
    jobs = soup.find_all('li', {'class': 'clearfix job-bx wht-shd-bx'})
    for index, job in enumerate(jobs):      # enumerate for using index
        publish_date = job.find('span', {'class': 'sim-posted'}).span.text.strip()
        # discard z publish_date contains 'few' word.
        if 'few' not in publish_date:
            skills = job.find('span', {'class': 'srp-skills'}).text.strip().replace('  ,  ', ', ')
            # filter out z skill u choose.
            if discarded_skill not in skills:
                # job_url = job.h2.a['href']
                company_name = job.find('h3', {'class': 'joblist-comp-name'}).text.strip()
                experience = job.li.text.strip().split('vel')[1]        # li > first & no attribute
                location = job.find('span').text.strip()
                # job_description = job.find('ul', {'class': 'list-job-dtl clearfix'}).li.text.strip().split('Description:')[1]
                jobs_details.append({'publish_date': publish_date, 'skills': skills, 'company_name': company_name, 'experience': experience, 'location': location})
                # save z results in a TXT file.
                with open(f'timesjobs/no_{discarded_skill}_{index}.txt', 'w') as f:
                    f.write(f'Company Name: {company_name} \n')
                    f.write(f'Required Skills: {skills} \n')
                    # f.write(f'Job URL: {job_url}')
                # print(f'File saved: no_{discarded_skill}_{index}')
    # save z results in a CSV file.
    keys = jobs_details[0].keys()
    with open(f'timesjobs/jobs_details wo {discarded_skill}.csv', 'w') as op_file:
            dict_writer = csv.DictWriter(op_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(jobs_details)
find_jobs(page)

# make z program excute every 10 minutes.
if __name__ == '__main__':
    while True:
        find_jobs(page)
        timt_wait = 10
        print(f'Waiting {timt_wait} minutes.')
        time.sleep(timt_wait * 60)
