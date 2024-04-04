import requests

def get_fsq_places(citybikes_df, url, params, headers):
    citybikes_df = citybikes_df.copy()
    params = params.copy()
    headers = headers.copy()

    cols = ["fsq_id", "cat_id", "cat_name", "lat", "long", "name", "street_address", "zip", "locality", "distance"]
    fsq_df = pd.DataFrame(columns=cols)

    i = 0 
    for index, row in citybikes_df.iterrows():
        if i == 1:
            return fsq_parsing
        else:
            lat = row['latitude']
            long = row['longitude']
            params['ll'] = f'{lat},{long}'
            response = requests.request("GET", url, params=params, headers=headers)
            data = response.json()
            fsq_parsing(data, fsq_df)
            i += 1



def fsq_parsing(api_results, blank_df):

    '''Takes an iterable API result and blank dataframe that you want to fill out. Currently it's designed for a very specific use-case but can be generalized.'''
    filled_df = blank_df.copy()
    i = len(blank_df)
    for place in api_results['results']:
        # fsq_id
        filled_df.loc[i, 'fsq_id'] = place.get('fsq_id', None)
        # cat_id
        filled_df.loc[i, 'cat_id'] = place['categories'][0].get('id', None)
        # cat_name
        filled_df.loc[i, 'cat_name'] = place['categories'][0].get('name', None)
        # lat
        filled_df.loc[i, 'lat'] = place['geocodes']['main'].get('latitude', None)
        # long
        filled_df.loc[i, 'long'] = place['geocodes']['main'].get('longitude', None)
        # name
        filled_df.loc[i, 'name'] = place.get('name', None)
        # street address
        filled_df.loc[i, 'street_address'] = place['location'].get('address', None)
        # zip
        filled_df.loc[i, 'zip'] = place['location'].get('postcode', None)
        # locality
        filled_df.loc[i, 'locality'] = place['location'].get('locality', None)
        # distance from bike station
        filled_df.loc[i, 'distance'] = place.get('distance', None)
        i += 1
    return filled_df