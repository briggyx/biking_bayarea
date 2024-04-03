def citybikes_parsing(api_results, blank_df):
    '''Takes an iterable API result and blank dataframe that you want to fill out. Currently it's designed for a very specific use-case but can be generalized.'''
    filled_df = blank_df.copy()
    
    for x in range(555):
        filled_df.loc[x, 'name'] = api_results['network']['stations'][x]['name']
        filled_df.loc[x, 'id'] = api_results['network']['stations'][x]['id']
        filled_df.loc[x, 'timestamp'] = api_results['network']['stations'][x]['timestamp']
        filled_df.loc[x, 'longitude'] = api_results['network']['stations'][x]['longitude']
        filled_df.loc[x, 'latitude'] = api_results['network']['stations'][x]['latitude']
        filled_df.loc[x, 'slots'] = api_results['network']['stations'][x]['extra'].get('slots', None)
        filled_df.loc[x, 'free_bikes'] = api_results['network']['stations'][x]['free_bikes']
        filled_df.loc[x, 'empty_slots'] = api_results['network']['stations'][x].get('empty_slots', None)
        filled_df.loc[x, 'has_ebikes'] = api_results['network']['stations'][x]['extra'].get('has_ebikes', None)
        filled_df.loc[x, 'payment'] = api_results['network']['stations'][x]['extra'].get('payment', None)
        filled_df.loc[x, 'renting'] = api_results['network']['stations'][x]['extra'].get('renting', None)
        filled_df.loc[x, 'returning'] = api_results['network']['stations'][x]['extra'].get('returning', None)
        filled_df.loc[x, 'ebikes'] = api_results['network']['stations'][x]['extra'].get('ebikes', None)

    return filled_df
