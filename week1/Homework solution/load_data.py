#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine
import argparse

def load_data(host='localhost', port=5433, user='postgres', password='postgres', db='ny_taxi'):
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    print(f"Connecting to {db} database...")
    engine = create_engine(connection_string)
    
    print("Loading green taxi data...")
    df = pd.read_parquet('green_tripdata_2025-11.parquet')
    print(f"Rows: {len(df)}")
    
    df.to_sql('green_tripdata', engine, if_exists='replace', index=False, chunksize=10000)
    print("Green taxi data loaded")
    
    print("Loading zone lookup...")
    zones = pd.read_csv('taxi_zone_lookup.csv')
    print(f"Zones: {len(zones)}")
    
    zones.to_sql('taxi_zone_lookup', engine, if_exists='replace', index=False)
    print("Zone lookup loaded")
    
    print(f"\nDate range: {df['lpep_pickup_datetime'].min()} to {df['lpep_pickup_datetime'].max()}")
    
    return engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load NYC taxi data into PostgreSQL')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=5433)
    parser.add_argument('--user', default='postgres')
    parser.add_argument('--password', default='postgres')
    parser.add_argument('--db', default='ny_taxi')
    
    args = parser.parse_args()
    
    try:
        load_data(args.host, args.port, args.user, args.password, args.db)
    except Exception as e:
        print(f"Error: {e}")
