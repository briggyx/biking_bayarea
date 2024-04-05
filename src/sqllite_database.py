import pandas as pd
import sqlite3
import re


def populate_citybikes_sqllite(con, cur, citybikes_df):
    for index, row in citybikes_df.iterrows():

        data_tuple = (row['name'], row['id'], row['timestamp'],
                      row['longitude'], row['latitude'], row['slots'],
                      row['free_bikes'], row['empty_slots'], row['has_ebikes'],
                      row['ebikes'], re.sub(r'\[|\]', '', str(row['payment'])),
                      row['renting'], row['returning'])

        cur.execute(
            """
            INSERT INTO citybikes (name, id, timestamp, longitude, latitude, slots, free_bikes, empty_slots, has_ebikes, ebikes, payment, renting, is_returning) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)

    con.commit()




def populate_fsq_sqllite(con, cur, fsq_df):
    for index, row in fsq_df.iterrows():

        data_tuple = (row['reference_bike_stn'], row['fsq_id'], row['cat_id'],
                      row['cat_name'], row['lat'], row['long'], row['name'],
                      row['street_address'], row['zip'], row['locality'],
                      row['distance'])

        cur.execute(
            """
            INSERT INTO fsq (reference_bike_stn, fsq_id, cat_id, cat_name, lat, long, name, street_address, zip, locality, distance) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)

    con.commit()




def populate_yelp_sqllite(con, cur, yelp_df):
    for index, row in yelp_df.iterrows():

        data_tuple = (row['reference_bike_stn'], row['yelp_id'],
                      row['cat_alias'], row['lat'], row['long'], row['name'],
                      row['street_address'], row['zip'], row['city'],
                      row['price'], row['rating'], row['review_count'], row['distance_from_bike_stn'])

        cur.execute(
            """
            INSERT INTO yelp (reference_bike_stn, yelp_id, cat_alias, lat, long, name, street_address, zip, city, price, rating, review_count, distance_from_bike_stn) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)

    con.commit()
