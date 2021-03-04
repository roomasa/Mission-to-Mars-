
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Path to chromedriver
#!which chromedriver
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#driver = webdriver.Chrome(ChromeDriverManager().install())

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}

browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

#set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')
#so the code 'ul.item_list li.slide' pinpoints the <li /> tag with the class of slide and the <ul /> tag with a class of item_list
# In[6]
slide_elem.find("div", class_='content_title')
#When we chain fund to the slide_elem variable, we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data." 


# to just get the text, Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ### Featured Images


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# Find and click the full image button#the index 1 tells our browser to click the second button 
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
# We were able to pull the link to the image by pointing BeautifulSoup to where the image will be, instead of grabbing the URL directly

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


#we're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
df = pd.read_html('http://space-facts.com/mars/')[0]
#we assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'value']
#By using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df
df.to_html()

#once done with scraping need to end the session
browser.quit()





