import requests
import pandas as pd
from latest_user_agents import get_random_user_agent
import streamlit as st
ua = get_random_user_agent()


def scrape():
    item_list = []
    n = 1
    isNext = True
    col1, col2 = st.columns(2)
    progress = col1.metric('Pages scraped', 0)
    x = 0
    while isNext:
        x = x + 1
        print(f'Page {n}')
        headers = {
            'User-Agent': ua
        }
        response = requests.get(f'https://api.citygridmedia.com/content/places/v2/search/where?what={category}&where={location}&publisher=citysearch&format=json&placement=loki&page={n}&rpp=100', headers=headers)
        progress.metric('Pages scraped', x)
        try:
            cards = response.json()
            for card in cards['results']['locations']:
                try:
                    name = card['name']
                except:
                    name = None
                try:
                    street = card['address']['street']
                except:
                    street = None
                try:
                    city = card['address']['city']
                except:
                    city = None
                try:
                    state = card['address']['state']
                except:
                    state = None
                try:
                    postal_code = card['address']['postal_code']
                except:
                    postal_code = None
                try:
                    phone = card['phone_number']
                except:
                    phone = None
                try:
                    rating = card['rating']
                except:
                    rating = None
                try:
                    profile = card['profile']
                except:
                    profile = None
                try:
                    review = card['user_review_count']
                except:
                    review = None
                try:
                    categories = card['sample_categories']
                except:
                    categories = None

                item = {
                    'Name':name,
                    'Phone':phone,
                    'Street':street,
                    'City': city,
                    'State': state,
                    'Postal code': postal_code,
                    'Rating': rating,
                    'Profile link': profile,
                    'Reviews': review,
                    'Category': categories
                }

                item_list.append(item)

            if cards['results']['last_hit'] < cards['results']['total_hits']:
                n = n + 1
            else:
                isNext = False
                break
        except:
            break

    df = pd.DataFrame(item_list)
    col2.metric('Total Data scraped', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='citysearch-data.csv',
    mime='text/csv',
    )

st.title('CITYSEARCH.COM SCRAPER 🏙️')
st.info('Citysearch helps you find local businesses in your city and neighborhood.')

box1, box2, box3 = st.columns(3)

popular_cities = box1.radio(
    "Popular Cities",
    ('Los Angeles, CA', 'San Francisco, CA', 'Atlanta, GA', 'Chicago, IL', 
    'Boston, MA', 'New York City, NY', 'Portland, OR', 'Philadelphia, PA','Austin, TX', 'Houston, TX', 'Seattle, WA'))
popular_category = box3.radio(
    'Popular Categories',
    ('Appliance Repair', 'HVAC', 'Restaurants', 'Automotive Repair', 'Hotels', 'Self-Storage','Dentists', 'Movie Theaters', 'Shopping',
    'Electricians', 'Night Life', 'Spa & Beauty', 'General Contractors', 'Plumbers', 'Veterinarians'
    )
    )

with box2.form('Scraper'):
    category = st.text_input('Category')
    location = st.text_input('Location')

    start = st.form_submit_button('Scrape')
    st.caption('Scroll down to view the data')

if start:
    scrape()
    st.balloons()
    st.success('Done')

