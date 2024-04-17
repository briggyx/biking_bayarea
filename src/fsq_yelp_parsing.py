import requests
import pandas as pd

def get_fsq_places(citybikes_df, url, params, headers):
    citybikes_df = citybikes_df.copy()
    params = params.copy()
    headers = headers.copy()

    cols = ["reference_bike_stn", "fsq_id", "cat_id", "cat_name", "lat", "long", "name", "street_address", "zip", "locality", "distance"]
    fsq_df = pd.DataFrame(columns=cols)

    for index, row in citybikes_df.iterrows():
        lat = row['latitude']
        long = row['longitude']
        bike_stn_id = row['id']
        params['ll'] = f'{lat},{long}'
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            fsq_df = fsq_parsing(data, fsq_df, bike_stn_id)
        else:
            pass

    return fsq_df


def fsq_parsing(api_results, blank_df, bike_stn_id):
    filled_df = blank_df.copy()
    for place in api_results['results']:
        i = len(filled_df)
        filled_df.loc[i] = [
            bike_stn_id,
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




def combine_yelp_fsq(fsq_df, yelp_df):
    combined_df = pd.concat([fsq_df, yelp_df], ignore_index=True)
    return combined_df




def find_repeat_venues(combined_df):
    grouped_by_bikestn = combined_df.groupby('reference_bike_stn')
    repeat_venues = []

    for reference_bike_stn, group_index in grouped_by_bikestn.groups.items():
        # print("Reference Bike Station:", reference_bike_stn)
        df = combined_df.loc[group_index]
        
        # Initialize a dictionary to store the counts of (name, long, lat) tuples
        name_counts = {}
        
        # Iterate over rows in the group
        for row in df.itertuples():
            name = row.name
            long = row.long
            lat = row.lat 
            
            # Update the count for the current (name, long, lat) tuple
            venue_tuple = (name, long, lat)
            if venue_tuple in name_counts:
                name_counts[venue_tuple] += 1
            else:
                name_counts[venue_tuple] = 1
        
        # Check for repeated venues and append to repeat_venues list
        for venue_tuple, count in name_counts.items():
            if count > 1:
                # print(venue_tuple, ":", count)
                repeat_venues.append((reference_bike_stn, venue_tuple[0], venue_tuple[1], venue_tuple[2], count))

    # Return repeat_venues after processing all groups
    return repeat_venues
