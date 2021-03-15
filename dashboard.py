"""Main module for the Streamlit app"""
import requests
from requests.exceptions import HTTPError
import streamlit as st
import json
import random
import numpy as np 
import pandas as pd

NAGER_API_BASE = 'https://date.nager.at/api/v2'


@st.cache
def load_country_codes():
    """Loads country codes available from the Nager.Date API

    Returns:
        A list of country codes. Each country code is
        a two character string.

    Raises:
        requests.exceptions.RequestException: If the
            request to the Nager.Date API fails.
    """

    url = '/'.join([NAGER_API_BASE, 'AvailableCountries'])
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    #### TODO - Process the response ####

    country_codes = json.loads(response.text)
    
    #  return key value for each coutry 
    return [code['key'] for code in country_codes]
   
  
    #####################################
    
    # return country_codes

def salutation():
    # was able to generate ip address but unvalid ones
    random_ip = '.'.join(map(str,(random.randint(0,255) for _ in range(4))))

    salutation_url = 'https://fourtonfish.com/hellosalut/{random_ip}'
    
    try:
        response = requests.get(salutation_url)
        response.raise_for_status()
    
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print(f'this error occurred: {e}')
    
    languages = json.loads(response.text)

    return [lan['Hello'] for lan in languages]

@st.cache 
def chart():
    
    # still trying to figure out how to pass the year here 
    holiday_url = 'https://date.nager.at/Api/v2/PublicHolidays/{year}/{country_code}'

    try:
        response = requests.get(holiday_url)
        response.raise_for_status()
    
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print(f'this error occurred: {e}')
    
    holiday = json.loads(response.text)
    
    # convert public holiday json data as a dataframe
    df = pd.json_normalize(holiday)

    num_of_holidays = df.groupby('date')['name'].count()

    return num_of_holidays


def main():
    
    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code', country_codes)

    # show country code
    st.markdown('You selected country code -', country_code)

    # plot line chart
    st.subheader('Here are the holidays:')
    st.line_chart(chart,country_code)

    # show salutation 
    language = salutation()
    st.markdown(language)


if __name__ == '__main__':
    main()

