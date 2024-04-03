







def fsq_parsing(api_results, blank_df):

    '''Takes an iterable API result and blank dataframe that you want to fill out. Currently it's designed for a very specific use-case but can be generalized.'''
    filled_df = blank_df.copy()
    i = 0
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