from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Configuration
SITES = {

    "Visit Chattanooga": {
        "url": "https://www.visitchattanooga.com/events/",
        "content_list_class": {"div": "content list"},
        "item_attr": {"div": {"data-type": "events"}},
        "title": {"a": {"class": "title truncate"}},
        "date": {"span": {"class": "mini-date-container"}},
        "month": {"span": {"class": "month"}},
        "day": {"span": {"class": "day"}},
        "img": {"img": {"class": "thumb"}},
        "location": {"li": {"class": "locations truncate"}},
        "recurrence": {"li": {"class": "recurrence"}}
    },
    "Nooga Today": {
        "url": "https://noogatoday.6amcity.com/events#/", # preloaded_lightbox blocking site
        "content_list_class": "",
        "item_attr": {},
        "title_tag": "a",
        "title_class": "",
        "date_class": "",
        "month_class": "",
        "day_class": "",
        "img_class": "",
        "location_class": "",
        "recurrence_class": ""
    },
    "Choose Chatt": {
        "url": "https://choosechatt.com/chattanooga-events/", # dialog-lightbox-message blocking site
        "content_list_class": "",
        "item_attr": {},
        "title_tag": "a",
        "title_class": "",
        "date_class": "",
        "month_class": "",
        "day_class": "",
        "img_class": "",
        "location_class": "",
        "recurrence_class": ""
    },
    "CHA Guide Events": {
        "url": "https://www.cha.guide/events",
        "content_list_class": {"div": "flex-table w-dyn-list"},
        "item_attr": {"div": {"role": "listitem"}},
        "title": {"h3": {"class": "event-title"}},
        "date": {"div": {"class": "event-date-div"}},
        "month": {"div": {"class": "event-month"}},
        "day": {"div": {"class": "event-card-date"}},
        "img": {"div": {"class": "event---category-circle"}},
        "location": {"div": {"class": "location-2"}},
        "recurrence": {"div": {"class": "event---category-circle"}}
    },
    "Chattanooga Pulse": {
        "url": "https://www.chattanoogapulse.com/search/event/the-pulse-event-search/#page=1",
        "content_list_class": "",
        "item_attr": {},
        "title_tag": "a",
        "title_class": "",
        "date_class": "",
        "month_class": "",
        "day_class": "",
        "img_class": "",
        "location_class": "",
        "recurrence_class": ""
    },
    "Times Free Press": {
        "url": "https://www.timesfreepress.com/tfpevents/?_evDiscoveryPath=/",
        "content_list_class": "",
        "item_attr": {},
        "title_tag": "a",
        "title_class": "",
        "date_class": "",
        "month_class": "",
        "day_class": "",
        "img_class": "",
        "location_class": "",
        "recurrence_class": ""
    },
    "CHA Guide Weekly": {
        "url": "https://www.cha.guide/explore/things-to-do-in-chattanooga-this-week",
        "content_list_class": "",
        "item_attr": {},
        "title_tag": "a",
        "title_class": "",
        "date_class": "",
        "month_class": "",
        "day_class": "",
        "img_class": "",
        "location_class": "",
        "recurrence_class": ""
    },
    "Chattanooga Chamber": {
        "url": "https://chattanoogachamber.com/",
        "content_list_class": "",
        "item_attr": {},
        "title_tag": "a",
        "title_class": "",
        "date_class": "",
        "month_class": "",
        "day_class": "",
        "img_class": "",
        "location_class": "",
        "recurrence_class": ""
    },
    "Chattanooga Library": {
        "url": "https://www.chattlibrary.org/events/",
        "content_list_class": "",
        "item_attr": {},
        "title_tag": "a",
        "title_class": "",
        "date_class": "",
        "month_class": "",
        "day_class": "",
        "img_class": "",
        "location_class": "",
        "recurrence_class": ""
    }
}

def fetch_page(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load content
        return driver.page_source
    except Exception as e:
        print(f"Error fetching the page: {e}")
        return None
    finally:
        driver.quit()

def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')

def extract_events(parsed_content, config):
    events = []
    print(f"Searching for content list with: {config['content_list_class']}")
    
    # Unpack the content_list_class dictionary
    tag, class_name = next(iter(config['content_list_class'].items()))
    content_list = parsed_content.find(tag, class_=class_name)
    
    if not content_list:
        print("Couldn't find content list")
        return events

    # Unpack the item_attr dictionary
    item_tag, item_attrs = next(iter(config['item_attr'].items()))
    items = content_list.find_all(item_tag, **item_attrs)
    
    print(f"Found {len(items)} items with specified attributes")
    
    for item in items:
        event = {}
        
        # Extract title and URL
        title_tag, title_attrs = next(iter(config['title'].items()))
        title_element = item.find(title_tag, **title_attrs)
        if title_element:
            event['title'] = title_element.text.strip()
            url_element = title_element if title_element.name == 'a' else title_element.find_parent('a')
            event['url'] = config["url"] + url_element['href'] if url_element else ''
        else:
            print("Couldn't find title element")
            continue
        
        # Extract date
        date_tag, date_attrs = next(iter(config['date'].items()))
        date_element = item.find(date_tag, **date_attrs)
        if date_element:
            month_tag, month_attrs = next(iter(config['month'].items()))
            day_tag, day_attrs = next(iter(config['day'].items()))
            month = date_element.find(month_tag, **month_attrs)
            day = date_element.find(day_tag, **day_attrs)
            if month and day:
                event_date = f"{month.text.strip()} {day.text.strip()}, {datetime.now().year}"
                event['date'] = event_date
            else:
                event['date'] = date_element.text.strip()
        else:
            event['date'] = None
        
        # Extract image URL
        if config["img"]:
            img_tag, img_attrs = next(iter(config['img'].items()))
            img_element = item.find(img_tag, **img_attrs)
            event['image_url'] = img_element.get('data-lazy-src') or img_element.get('src') if img_element else None
        else:
            event['image_url'] = None
        
        # Extract location
        location_tag, location_attrs = next(iter(config['location'].items()))
        location_element = item.find(location_tag, **location_attrs)
        event['location'] = location_element.text.strip() if location_element else None
        
        # Extract recurrence information
        recurrence_tag, recurrence_attrs = next(iter(config['recurrence'].items()))
        recurrence_element = item.find(recurrence_tag, **recurrence_attrs)
        event['recurrence'] = recurrence_element.text.strip() if recurrence_element else None
        
        events.append(event)
    
    return events

def main():
    for site_name, config in SITES.items():
        url = config["url"]
        print(f"Fetching and parsing {site_name}")
        html_content = fetch_page(url)  # This should be using Selenium
        if html_content:
            parsed_content = parse_html(html_content)
            print(f"Length of parsed content: {len(str(parsed_content))}")
            events = extract_events(parsed_content, config)
            print(f"Extracted {len(events)} events")
            for event in events:
                print(f"Title: {event.get('title')}")
                print(f"URL: {event.get('url')}")
                print(f"Date: {event.get('date')}")
                print(f"Image URL: {event.get('image_url')}")
                print(f"Location: {event.get('location')}")
                print(f"Recurrence: {event.get('recurrence')}")
                print("-" * 40)
        else:
            print(f"Skipping {site_name} due to fetch error")
        time.sleep(1)  # Be polite, wait a second between requests

if __name__ == "__main__":
    main()
