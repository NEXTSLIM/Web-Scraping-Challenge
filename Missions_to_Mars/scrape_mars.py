#!/usr/bin/env python
# coding: utf-8

# # Step 1 - Scraping

# ## Declare dependencies

# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager

# ## Initialize Browser Funcion

def init_browser():
    
     executable_path = {'executable_path': ChromeDriverManager().install()}
     browser = Browser('chrome', **executable_path, headless=True)



def scrape():
    # ## NASA Mars News

    # Run init_browser function and open it
    browser = init_browser()
    # Visit https://mars.nasa.gov/news/
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get Title and Paragrapht Text
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

    browser.quit()
    #print(news_title + "\n" +  news_p)


    # ## JPL Mars Space Images - Featured Image

    # Run init_browser function and open it
    browser = init_browser()
    # Visit https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    time.sleep(3)

    # Click in one of the images
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    # Click in the button for more information
    browser.click_link_by_partial_text('more info')
    time.sleep(3)

    # Get the new url after clicking "more info" and visiting it
    url = browser.url
    browser.visit(url)
    time.sleep(3)

    # Scrape clicked page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the base url to be used with relative paths
    parsed = urlparse(url)
    base_url = parsed.scheme +"://"+ parsed.netloc

    time.sleep(3)

    # Get the high resolution image from the accesed page
    featured_image_url = base_url +  soup.find('img', class_="main_image")["src"]

    browser.quit()
    #print(featured_image_url)


    # ## Mars Weather

    # Run init_browser function and open it
    browser = init_browser()
    # Visit https://twitter.com/marswxreport?lang=en
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the twit
    mars_weather = soup.find("div", class_="js-tweet-text-container")
    mars_weather = mars_weather.find("p").text

    browser.quit()
    print(mars_weather)


    # ## Mars Facts

    # Run init_browser function and open it
    browser = init_browser()
    # Visit https://space-facts.com/mars/
    url = "https://space-facts.com/mars/"

    time.sleep(1)

    # Scrape with Paandas
    tables_df = pd.read_html(url)

    # Get first table with the facts
    mars_facts_df = tables_df[0]

    # Rename column of the dataframe
    mars_facts_df = mars_facts_df.rename(columns={0: "Description", 1: "Value"})


    # Use the titles as index
    mars_facts_df.set_index("Description", inplace=True)

    # Convert the dataframe to html
    mars_facts_html = mars_facts_df.to_html()

    browser.quit()
    #print (mars_facts_html)
    #print (mars_facts_df)


    # ## Mars Hemispheres

    # Run init_browser function and open it
    browser = init_browser()

    # Visit https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Get the base url to be used with relative paths
    parsed = urlparse(url)
    base_url = parsed.scheme +"://"+ parsed.netloc

    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the image URL

    results = soup.find("div", class_="collapsible results")

    # Initialize the Dictionary
    hemisphere_image_urls = []
    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return title of the image
            title = result.find("div").h3.text
            
            # Identify and return link to the high resolution image
            link_parent = base_url + result.a['href']
            
            # Use the link to the page to get the high resolution Page
            link_son = link_parent
            browser.visit(link_son)
            
            time.sleep(1)
            
            # Scrape the socond page into Soup
            html = browser.html
            soup = bs(html, "html.parser")
            
            # Get the image URL of the high resolution URL
            # For getting the Original .tif
            #link_son = soup.find("a", text="Original")['href']
            
            # For getting the Sample .jpg
            link_son = soup.find("a", text="Sample")['href']
            
            # Print results only if title, price, and link are available
            if (title and link_parent):
                #print('-------------')
                #print(title)
                #print(link_parent)
                #print(link_son)

                # Create Dictionary
                url_dict = {}
                url_dict["title"] = title
                url_dict["img_url"] = link_son
                hemisphere_image_urls.append(url_dict)

        except AttributeError as e:
                #print(e)
                pass

    browser.quit()
    #print (hemisphere_image_urls)


    # ## Final Result Dictionary

    # Store data in a dictionary
    scraping_results = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "mars_facts_html": mars_facts_html,
            "hemisphere_image_urls": hemisphere_image_urls
            }
    return scraping_results