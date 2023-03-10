
import requests
from bs4 import BeautifulSoup
import csv
import time

print('\nPlease put unfamiliar skill')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill} ...\n')

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    jobs_details = []
    for index, job in enumerate(jobs):      # enumerate for using index
        published_date = job.find('span', class_='sim-posted').span.text.strip()
        # discard publish_date contains 'few' word.
        if 'few' not in published_date:
            skills = job.find('span', class_='srp-skills').text.replace('  ,  ', ', ').strip()
            # filter out z skill u choose.
            if unfamiliar_skill not in skills.lower():
                company_name = job.h3.text.strip()
                experience = job.li.text.strip().split('vel')[1]        # li > first & no attribute
                location = job.span.text.strip()
                more_info = job.h2.a['href']
                # save z results in a separated TXT file.
                with open(f'timesjobs/no_{unfamiliar_skill}_{index}.txt', 'w') as f:
                    f.write(f'Pub_date: {published_date} \n')
                    f.write(f'Company Name: {company_name} \n')
                    f.write(f'Required Skills: {skills} \n')
                    f.write(f'More Info: {more_info}')
                print(f'File saved: no_{unfamiliar_skill}_{index}')

                # save z results in a CSV file.
                # job_description = job.find('ul', {'class': 'list-job-dtl clearfix'}).li.text.strip().split('Description:')[1]
                jobs_details.append({'publish_date': published_date, 'skills': skills, 'company_name': company_name, 'experience': experience, 'location': location})
                keys = jobs_details[0].keys()
                with open(f'timesjobs/jobs_details wo {unfamiliar_skill}.csv', 'w') as op_file:
                    dict_writer = csv.DictWriter(op_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(jobs_details)
print(f'File saved: jobs_details wo {unfamiliar_skill}.csv')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print()
        print(f'Waiting {time_wait} minutes ...')
        time.sleep(time_wait * 60)

# https://www.youtube.com/watch?v=XVv6mJpFOb0&t=3708s       > chapters
