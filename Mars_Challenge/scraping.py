from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#connect Mongo and establish communication btw code and database
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemisphere = []

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

# mars news scrape  
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# featured image scrape
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Mars Facts scrape
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemispheres(browser):
   
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

    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

    
# tell flask we are ready
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())