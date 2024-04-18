import pandas as pd

def citybikes_parsing(api_results, blank_df):
    '''Fills out a blank DataFrame with data from an iterable API result.
    
    Args:
        api_results (iterable): Iterable API result containing bike station data.
        blank_df (DataFrame): Blank DataFrame to be filled out with station data.
        
    Returns:
        DataFrame: Filled DataFrame with bike station data.
    '''
    filled_df = blank_df.copy()
    
    for x, station_data in enumerate(api_results['network']['stations'][:555]):
        filled_df.loc[x, 'name'] = station_data['name']
        filled_df.loc[x, 'id'] = station_data['id']
        filled_df.loc[x, 'timestamp'] = station_data['timestamp']
        filled_df.loc[x, 'longitude'] = station_data['longitude']
        filled_df.loc[x, 'latitude'] = station_data['latitude']
        filled_df.loc[x, 'slots'] = station_data['extra'].get('slots', None)
        filled_df.loc[x, 'free_bikes'] = station_data['free_bikes']
        filled_df.loc[x, 'empty_slots'] = station_data.get('empty_slots', None)
        filled_df.loc[x, 'has_ebikes'] = station_data['extra'].get('has_ebikes', None)
        filled_df.loc[x, 'payment'] = station_data['extra'].get('payment', None)
        filled_df.loc[x, 'renting'] = station_data['extra'].get('renting', None)
        filled_df.loc[x, 'returning'] = station_data['extra'].get('returning', None)
        filled_df.loc[x, 'ebikes'] = station_data['extra'].get('ebikes', None)

    return filled_df
