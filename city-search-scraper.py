import requests
import pandas as pd
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()

category = input('Category: ')
location = input('Location: ')

def scrape():
    item_list = []
    n = 1
    isNext = True
    while isNext:
        print(f'Page {n}')
        headers = {
            'User-Agent': ua
        }
        try:
            response = requests.get(f'https://api.citygridmedia.com/content/places/v2/search/where?what={category}&where={location}&publisher=citysearch&format=json&placement=loki&page={n}&rpp=100', headers=headers)
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
    print(df)
    df.to_csv('data.csv')

scrape()