from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re

# Initialize the webdriver
driver = webdriver.Chrome('/Users/manassinghal/Downloads/chromedriver')

# Initialize lists to store data
Configuration = []
Description = []
Location_address = []
name = []
Price = []
Price_unit = []
Area = []
Type_area = []
bathroom=[]

# Specify the page to target
target_page = 'https://www.99acres.com/property-in-haridwar-ffid-page-25'

# Get the target page
driver.get(target_page)

# Give the browser time to load the page content
time.sleep(5)

# Parse the page content
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
results = soup.findAll('div', attrs={'class': 'tupleNew__contentWrap'})

# Extract data from the target page
for row in results:
    # Configuration or Area
    area_tags = row.findAll('span', attrs={'class': 'tupleNew__area1Type'})
    if area_tags:
        area_texts = [tag.get_text(strip=True) for tag in area_tags]
        if len(area_texts) >= 1:
            Area.append(area_texts[0])
        else:
            Area.append("N/A")
        if len(area_texts) >= 2:
            Configuration.append(area_texts[1])
        else:
            Configuration.append("N/A")
    else:
        Configuration.append("N/A")
        Area.append("N/A")

    #for bathroom
    bath_tags=row.findAll('span', attrs={'class': 'tupleNew__area2Type'})
    if bath_tags:
        bath_texts = [tag.get_text(strip=True) for tag in bath_tags]
        
        match = re.search(r'(\d+)', bath_texts[1])
        if match:
            bathroom.append(match.group(1))
        else:
            bathroom.append("0")
    else:
        bathroom.append("N/A")


    # Location/Bldng_name and Address
    address_tag = row.find('a', attrs={'class': 'tupleNew__propertyHeading'})
    if address_tag:
        title_attr = address_tag.get('title', '')
        match = re.search(r'in\s+(.+)$', title_attr)
        if match:
            address = match.group(1)
            Location_address.append(address)
        else:
            Location_address.append("N/A")
    else:
        Location_address.append("N/A")


    # Description (if available)
    description_tag = row.find('p', attrs={'class': 'descPtag_undefined tupleNew__descText'})
    if description_tag:
        desc_text = description_tag.get_text(strip=True)
        Description.append(desc_text)
    else:
        Description.append("N/A")
    
    # Name
    location_tag = row.find('div', attrs={'class': 'tupleNew__locationName'})
    if location_tag:
        loc_text = location_tag.get_text(strip=True)
        name.append(loc_text)
    else:
        name.append("N/A")

    # Type_area (if available)
    type_area_tag = row.find('div', attrs={'class': 'tupleNew__areaType'})
    if type_area_tag:
        type_area_text = type_area_tag.get_text(strip=True)
        Type_area.append(type_area_text)
    else:
        Type_area.append("N/A")
    
    # Price and Price_unit
    price_tag = row.find('div', attrs={'class': 'tupleNew__priceValWrap'})
    if price_tag:
        price_text = price_tag.find('span').get_text(strip=True)
        Price.append(price_text)
        price_unit_tag = row.find('div', attrs={'class': 'tupleNew__perSqftWrap'})
        if price_unit_tag:
            price_unit_text = price_unit_tag.get_text(strip=True)
            Price_unit.append(price_unit_text)
        else:
            Price_unit.append("N/A")
    else:
        Price.append("N/A")
        Price_unit.append("N/A")

# Ensure all lists are of the same length
max_length = max(len(Configuration), len(Description), len(Location_address), len(name), len(Price), len(Price_unit), len(Area), len(Type_area),len(bathroom))

Configuration += ["N/A"] * (max_length - len(Configuration))
Description += ["N/A"] * (max_length - len(Description))
Location_address += ["N/A"] * (max_length - len(Location_address))
name += ["N/A"] * (max_length - len(name))
Price += ["N/A"] * (max_length - len(Price))
Price_unit += ["N/A"] * (max_length - len(Price_unit))
Area += ["N/A"] * (max_length - len(Area))
Type_area += ["N/A"] * (max_length - len(Type_area))
bathroom += ["N/A"] * (max_length - len(bathroom))

# Create DataFrame
df = pd.DataFrame({
    'Configuration': Configuration,
    'Address': Location_address,
    'Name': name,
    'Description': Description,
    'Area': Area,
    'Area type': Type_area,
    'Price': Price,
    'Price Unit': Price_unit,
    'No of Bathroom': bathroom
})

# Save DataFrame to CSV
df.to_csv('99acres_25.csv', index=False)

driver.quit()
