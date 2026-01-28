#!/usr/bin/env python3

from sqlalchemy import create_engine, text
import argparse

def run_queries(host='localhost', port=5433, user='postgres', password='postgres', db='ny_taxi'):
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    print(f"Connecting to {db} database...\n")
    engine = create_engine(connection_string)
    
    queries = {
        "Question 3 - Short trips": """
            SELECT COUNT(*) as trip_count
            FROM green_tripdata
            WHERE lpep_pickup_datetime >= '2025-11-01' 
              AND lpep_pickup_datetime < '2025-12-01'
              AND trip_distance <= 1;
        """,
        
        "Question 4 - Longest trip by day": """
            SELECT DATE(lpep_pickup_datetime) as pickup_day, 
                   MAX(trip_distance) as max_distance
            FROM green_tripdata
            WHERE trip_distance < 100
            GROUP BY DATE(lpep_pickup_datetime)
            ORDER BY max_distance DESC
            LIMIT 1;
        """,
        
        "Question 5 - Biggest pickup zone": """
            SELECT z."Zone", 
                   SUM(g.total_amount) as total_sum
            FROM green_tripdata g
            JOIN taxi_zone_lookup z ON g."PULocationID" = z."LocationID"
            WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
            GROUP BY z."Zone"
            ORDER BY total_sum DESC
            LIMIT 5;
        """,
        
        "Question 6 - Largest tip": """
            SELECT do_zone."Zone" as dropoff_zone,
                   MAX(g.tip_amount) as max_tip
            FROM green_tripdata g
            JOIN taxi_zone_lookup pu_zone ON g."PULocationID" = pu_zone."LocationID"
            JOIN taxi_zone_lookup do_zone ON g."DOLocationID" = do_zone."LocationID"
            WHERE pu_zone."Zone" = 'East Harlem North'
              AND DATE(g.lpep_pickup_datetime) >= '2025-11-01'
              AND DATE(g.lpep_pickup_datetime) < '2025-12-01'
            GROUP BY do_zone."Zone"
            ORDER BY max_tip DESC
            LIMIT 5;
        """
    }
    
    with engine.connect() as conn:
        for title, query in queries.items():
            print(f"{title}")
            print("-" * 60)
            
            try:
                result = conn.execute(text(query))
                rows = result.fetchall()
                
                if rows:
                    print(f"{' | '.join(result.keys())}")
                    print("-" * 60)
                    
                    for row in rows:
                        print(f"{' | '.join(str(val) for val in row)}")
                else:
                    print("No results")
                    
            except Exception as e:
                print(f"Error: {e}")
            
            print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run homework queries')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=5433)
    parser.add_argument('--user', default='postgres')
    parser.add_argument('--password', default='postgres')
    parser.add_argument('--db', default='ny_taxi')
    
    args = parser.parse_args()
    
    try:
        run_queries(args.host, args.port, args.user, args.password, args.db)
    except Exception as e:
        print(f"Error: {e}")
