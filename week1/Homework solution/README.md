# Week 1 Homework - Docker & SQL

Here's how I approached the homework for Module 1. The main goal was to work with Docker containers, load NYC taxi data into PostgreSQL, and run some SQL queries to answer specific questions.

## My Setup

I used Docker Compose to spin up two containers - one for PostgreSQL and another for pgAdmin (though I mostly just used Python to run queries directly). 

To get everything running:

```bash
# Start the containers
docker-compose up -d

# Set up a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the packages I needed
pip install pandas sqlalchemy pyarrow psycopg2-binary
```

Then I downloaded the data files:
```bash
curl -O https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
curl -L -O https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

After that, I ran my scripts to load the data and execute the queries:
```bash
python load_data.py
python run_queries.py
```

## The Questions & My Answers

### Question 1: What's the pip version in python:3.13?

This one was straightforward - just needed to run the python:3.13 Docker image and check pip:
```bash
docker run --rm --entrypoint bash python:3.13 -c "pip --version"
```

**My answer: 25.3**

### Question 2: Docker networking

The question was about how pgadmin should connect to postgres when both are running in docker-compose. The key thing I learned here is that containers in the same Docker network use service names as hostnames, and they communicate via internal ports (not the ones mapped to the host).

So even though postgres is accessible from my machine on port 5433, from pgadmin's perspective it's just `db:5432`.

**My answer: db:5432** (postgres:5432 also works since that's the container name)

### Question 3: How many short trips?

I needed to count trips in November 2025 where the distance was 1 mile or less.

```sql
SELECT COUNT(*) 
FROM green_tripdata
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

**My answer: 8,007**

### Question 4: Which day had the longest trip?

For this one, I filtered out obviously wrong data (anything >= 100 miles seemed like errors), then grouped by date to find which day had the longest trip.

```sql
SELECT DATE(lpep_pickup_datetime) as pickup_day, 
       MAX(trip_distance) as max_distance
FROM green_tripdata
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;
```

**My answer: 2025-11-14**

### Question 5: Which zone had the highest total on Nov 18?

This required joining with the zone lookup table to get zone names, then summing up total_amount for each pickup zone on that specific date.

```sql
SELECT z."Zone", 
       SUM(g.total_amount) as total_sum
FROM green_tripdata g
JOIN taxi_zone_lookup z ON g."PULocationID" = z."LocationID"
WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_sum DESC
LIMIT 1;
```

**My answer: East Harlem North**

### Question 6: Largest tip from East Harlem North

For this I needed to filter pickups from East Harlem North, then find which dropoff zone got the biggest tip. Required joining the zone table twice.

```sql
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
LIMIT 1;
```

**My answer: Yorkville West**

### Question 7: Terraform commands

This was about knowing the basic Terraform workflow:
- `terraform init` to download providers and set up the backend
- `terraform apply -auto-approve` to apply changes without confirmation
- `terraform destroy` to tear everything down

**My answer: terraform init, terraform apply -auto-approve, terraform destroy**

## Notes

The dataset had 46,912 trips total and 265 zones. One thing I noticed - the column names in the parquet file use mixed case (like `PULocationID`), so I had to quote them in SQL to avoid case sensitivity issues.

PostgreSQL is accessible at `localhost:5433` and pgAdmin runs at `http://localhost:8080` if you want to browse the data manually.
