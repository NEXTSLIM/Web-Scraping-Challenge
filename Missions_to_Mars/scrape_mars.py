#!/usr/bin/env python
# coding: utf-8

# # ▌ Web Scraping Homework-Mission to Mars ▌

# Dependencies
import pandas as pd
from splinter import Browser
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup 
from flask import Flask, render_template, redirect


# Set Executable Path & Initialize Chrome Browser
def scrape_info():
  # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# ## Step 1 - Scraping: 

# ### NASA Mars News
# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Retrieve page with the requests module
html = browser.html
# Create BeautifulSoup object; HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# get results at the first <li> item under <ul> list of headlines
results_li = soup.find('li', class_='slide')

#save the news title
title = results_li.find('div', class_='content_title').text
print(title)

#save the news paragraph
news_p = results_li.find('div', class_='article_teaser_body').text
print(news_p)


#  ### JPL Mars Space Images
# URLs of page to be scraped

space_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
space_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(space_image_url)
def mars_news(browser):
# HTML object
html=browser.html
# Parse HTML
soup=BeautifulSoup(html,"html.parser")
# Retrieve anchor tag with the image url
img_url=soup.find_all('a')[2]
img_url

def featured_image(browser):
# Retrieve the image url
img_url=soup.find('a', class_='showimg')['href']
img_url

# Display the full image url of the featured image
featured_image_url = space_url+img_url
featured_image_url


#  ### Mars Facts
def mars_facts():
# Parse Results HTML with BeautifulSoup
html = browser.html
image_soup = BeautifulSoup(html, "html.parser")

#Mars Facts website
MarsFacts_url = 'https://space-facts.com/mars/'
browser.visit(MarsFacts_url)
time.sleep(2)

#HTML object
html = browser.html

table = pd.read_html(html)

facts_df = table[0]
facts_df.columns =['Description', 'Value']
facts_df

# Mars Hemispheres Web Scraper
def hemisphere(browser):
MarsHemImage_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(MarsHemImage_url)
time.sleep(2)

html = browser.html

soup = BeautifulSoup(html, 'html.parser')


hemisphere_divs = soup.find_all('div', class_="item")

hemisphere_image_data = []


for hemisphere in range(len(hemisphere_divs)):

    hem_link = browser.find_by_css("a.product-item h3")
    hem_link[hemisphere].click()
    time.sleep(1)
    
    img_detail_html = browser.html
    imagesoup = BeautifulSoup(img_detail_html, 'html.parser')
    
    base_url = 'https://astrogeology.usgs.gov'
    
    hem_url = imagesoup.find('img', class_="wide-image")['src']
    
   
    img_url = base_url + hem_url

  
    img_title = browser.find_by_css('.title').text
    
   
    hemisphere_image_data.append({"title": img_title,
                              "img_url": img_url})
    
    browser.back()
      
browser.quit()

hemisphere_image_data

 #################################################
# Main Web Scraping Bot
#################################################


    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())
