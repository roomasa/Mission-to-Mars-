# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


#     url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     browser = Browser('chrome', **executable_path, headless=False)
#     browser.visit(url)
#     hemisphere_image_urls = []
#     image_url_link= browser.find_by_css('a.product-item h3')
# #writing a loop
#     for i in range(len(image_url_link)):
#         hemisphere_data={}
#         browser.find_by_css('a.product-item h3')[i].click()
#         initial_url=browser.find_by_text('Sample').first
#         hemisphere_data["image_url"]=initial_url["href"]
#         hemisphere_data["title"]=browser.find_by_css('h2.title').text
#         hemisphere_image_urls.append(hemisphere_data)
#         browser.back()
        

def scrape_all():
    # Initiate headless driver for deployment
    #browser = Browser("chrome", executable_path="chromedriver", headless=True)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser('chrome', executable_path="chromedriver", headless=False)
    browser.visit(url)
    #hemisphere_image_urls = []
    #image_url_link= browser.find_by_css('a.product-item h3')
#writing a loop
    # for i in range(4):
    #     hemisphere_data={}
    #     browser.find_by_css('a.product-item h3')[i].click()
    #     initial_url=browser.find_by_text('Sample').first
    #     hemisphere_data["image_url"]=initial_url["href"]
    #     hemisphere_data["title"]=browser.find_by_css('h2.title').text
    #     hemisphere_image_urls.append(hemisphere_data)
    #     browser.back()
    news_title, news_paragraph = mars_news(browser)
    #print(hemisphere_data)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere(browser)
        }
    print(data)

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
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
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_scrape(html):
    html_soup= soup(html,"html.parser")
    try: 
        title=html_soup.find("h2",class_="title").get_text()
        link=html_soup.find("a",text="Sample").get("href")
    except AttributeError: 
        title=None
        link=None
    hemisphere={
        "title":title,
        "image_url":link
    }
    return hemisphere

def hemisphere(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image=[]
    for i in range(4):
        #hemisphere_data={}
        browser.find_by_css('a.product-item h3')[i].click()
        data=hemisphere_scrape(browser.html)
        # initial_url=browser.find_by_text('Sample').first
        # hemisphere_data["image_url"]=initial_url["href"]
        # hemisphere_data["title"]=browser.find_by_css('h2.title').text
        hemisphere_image.append(data)
        browser.back()
        
    return hemisphere_image




if __name__ == "__main__":


    # If running as script, print scraped data
    print(scrape_all())