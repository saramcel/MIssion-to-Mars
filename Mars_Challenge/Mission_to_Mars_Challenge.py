# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')

# this element has all the other elements in it
# CSS works from right to left, such as returning the last item on the list instead of the first. 
# Because of this, when using select_one, the first matching element returned will be a <li /> element with a class 
# of slide and all nested elements within it.
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.
# This for loop will iterate over all 4 hemispheres and collect the urls and titles in a dictionary, then append to a list.
# We know there are 4 hemispheres so I'm hard coding the loop so we don't have to worry about grabbing extra things

for i in range(4):
    
    #make a dictionary
    hemispheres = {}
    
    try:
        # Click to get the full image by finding the h3 heading tag for each hemisphere
        full_image_elem = browser.find_by_tag('h3')[i].click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        # filter down the results to a class that has both the image and the title
        results = img_soup.find('div', class_='container')

        # scrape the relative url (the src) and combine with the rest of the url
        ## I tested this in the browser and it brings up the correct thing, so fingers crossed!
        rel_url = results.find('img', class_='wide-image')['src']
        img_url = f'https://marshemispheres.com/{rel_url}'

        # Grab title text
        title = results.find('h2', class_='title').text

        # Append the dictionary and the list
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)

        # go back to the main url so you can overwrite the variables from the beginning
        browser.back()
    
    except AttributeError as e:
        print(e)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()