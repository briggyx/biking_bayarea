import requests
import pandas as pd

def get_fsq_places(citybikes_df, url, params, headers):
    citybikes_df = citybikes_df.copy()
    params = params.copy()
    headers = headers.copy()

    cols = ["fsq_id", "cat_id", "cat_name", "lat", "long", "name", "street_address", "zip", "locality", "distance"]
    fsq_df = pd.DataFrame(columns=cols)

    for index, row in citybikes_df.iterrows():
        lat = row['latitude']
        long = row['longitude']
        params['ll'] = f'{lat},{long}'
        response = requests.get(url, params=params, headers=headers)  # Use requests.get for clarity
        if response.status_code == 200:  # Check if the request was successful
            data = response.json()
            fsq_df = fsq_parsing(data, fsq_df)
        else:
            pass
        # Remove break if you want to iterate over all rows in citybikes_df

    return fsq_df


def fsq_parsing(api_results, blank_df):
    filled_df = blank_df.copy()
    for place in api_results['businesses']:
        i = len(filled_df)
        # Simplified using direct assignment as index `i` will always refer to the next row
        filled_df.loc[i] = [
            place.get('fsq_id', None), place['categories'][0].get('id', None)
            if place['categories'] else None, place['categories'][0].get(
                'name', None) if place['categories'] else None,
            place['geocodes']['main'].get('latitude', None),
            place['geocodes']['main'].get('longitude', None),
            place.get('name', None), place['location'].get('address', None),
            place['location'].get('postcode', None),
            place['location'].get('locality', None),
            place.get('distance', None)
        ]
    return filled_df





def get_yelp_places(citybikes_df, url, params, headers):
    citybikes_df = citybikes_df.copy()
    params = params.copy()
    headers = headers.copy()

    cols = [
        "reference_bike_stn", "yelp_id", "cat_alias", "lat", "long", "name",
        "street_address", "zip", "city", "price", "rating", "review_count",
        "distance_from_bike_stn"
    ]
    yelp_df = pd.DataFrame(columns=cols)

    for index, row in citybikes_df.iterrows():
        lat = row['latitude']
        long = row['longitude']
        bike_stn_id = row['id']
        params['latitude'] = f'{lat}'
        params['longitude'] = f'{long}'
        response = requests.get(
            url, params=params,
            headers=headers)  
        if response.status_code == 200:
            data = response.json()
            yelp_df = yelp_parsing(data, yelp_df, bike_stn_id)
        else:
            pass

    return yelp_df





def yelp_parsing(api_results, blank_df, bike_stn_id):
    filled_df = blank_df.copy()
    for place in api_results['businesses']:
        i = len(filled_df)
        filled_df.loc[i] = [
            bike_stn_id,
            place.get('id', None), place['categories'][0].get('alias', None),
            place['coordinates'].get('latitude', None),
            place['coordinates'].get('longitude', None),
            place.get('name', None), place['location'].get('address1', None),
            place['location'].get('zip_code',
                                  None), place['location'].get('city', None),
            place.get('price', None),
            place.get('rating', None),
            place.get('review_count', None),
            place.get('distance', None)
        ]
    return filled_df
