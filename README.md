# Grab Scraper
## _Code Explanation and Documentation_

This code retrieves the latitude and longitude of restaurants listed on https://food.grab.com/sg/en/restaurants using Selenium WebDriver and selenium-wire library. The code scrolls down the webpage to load all the restaurants and captures the POST request and response to obtain restaurant data in JSON format. The obtained data is then processed to extract the latitude and longitude values of each restaurant and save it in a dictionary. The dictionary is then written to a JSON file named "restaurants.json".

Here is a brief explanation of the code:

1] import required libraries:
- json: for encoding and decoding JSON data
- time: for adding delay in the script
- seleniumwire.webdriver: for controlling a web browser using Selenium with the ability to intercept network requests made by the browser
- selenium.webdriver.common.by.By: for locating elements on the webpage using different types of selectors.

2] Open the website on Chrome browser using Selenium WebDriver.<br>
3] Maximize the browser window for better visibility.<br>
4] Define a function named "write_json" to write new data to a JSON file.<br>
5] Define a function named "scroll_down" to scroll down the webpage and extract restaurant data.<br>
6] In the "scroll_down" function:
- Create an empty list named "post_data" to store the JSON data of restaurants.
- Find the height of the webpage and enter a loop that scrolls down the webpage and captures POST requests until there are no more restaurants to load.
- For each POST request made by the webpage, the code checks if it is a restaurant search request.
- If it is a restaurant search request, the code decodes the response and converts it to a JSON object.
- The JSON object is then processed to extract the latitude and longitude values of each restaurant and save it in a dictionary named "d".
- After all the restaurants have been processed, the "d" dictionary is written to a JSON file using the "write_json" function.
- Also, we have added method 'write_to_csv' to convert json to csv by means of converting the dict into dataframe of required format and dumping it into csv file. You can fin dthe csv file by the name of 'Final_data.csv' in the same directory.

7] Call the "scroll_down" function once.<br>
8] Close the browser.

## Installation

Grab Scraper requires [Python](https://python.org/) 3 to run.

Install the dependencies and start the server.

```sh
pip3 install -r requirements.txt
```

```sh
cd GrabScraper
python3 grabscraper.py
```
