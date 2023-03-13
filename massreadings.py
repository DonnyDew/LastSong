import requests
from bs4 import BeautifulSoup

# URL for the daily Bible readings
url = 'https://bible.usccb.org/daily-bible-reading'

# Send a GET request to the URL and get the page content
response = requests.get(url)
page_content = response.content

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser')

# Find the container element for the daily Bible readings
daily_readings_container = soup.find('div', {'class': 'col-md-8 col-lg-9'})

if daily_readings_container is None:
    print('Error: Could not find daily readings container.')
    #print(soup)  # print the soup variable to inspect the HTML code
    exit()

# Get the date of the readings
date = daily_readings_container.find('h3').text.strip()

# Find the list of readings for the day
readings_list = daily_readings_container.find('ul', {'class': 'bibleReadings'})

if readings_list is None:
    print('Error: Could not find readings list.')
   # print(soup)  # print the soup variable to inspect the HTML code
    exit()

# Get each reading from the list and print it
for reading in readings_list.find_all(['li', 'div']):
    if reading.name == 'li':
        print(reading.text.strip())
    elif reading.name == 'div':
        reading_text = reading.find('div', {'class': 'p-wrap'}).text.strip()
        print(reading_text)
