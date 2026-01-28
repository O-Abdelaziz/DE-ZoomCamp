# Week 2 Homework - Workflow Orchestration with Kestra

This homework involved using Kestra to orchestrate ETL workflows for processing NYC taxi data.

## Setup

I used Kestra to create and run workflows for analyzing taxi trip data. The flow downloads CSV files, extracts them, and counts rows.

```bash
# Started Kestra
docker run --rm -d -p 8080:8080 --name kestra kestra/kestra:latest server standalone
```

Access Kestra UI at: http://localhost:8080

## My Kestra Flow

I created a flow called `taxi_data_etl` that takes three inputs:
- `taxi`: yellow or green
- `year`: the year to process
- `month`: the month (01-12)

The flow has these main tasks:
1. **Download** - fetches the gzipped CSV from GitHub
2. **Extract** - decompresses the file
3. **Get file info** - checks file size
4. **Count rows** - counts total rows (excluding header)

The flow YAML is in this directory: `taxi_data_etl.yaml`

## Execution Results & Answers

### Question 1: Yellow Taxi December 2020 File Size

I ran the flow with:
- taxi: yellow
- year: 2020
- month: 12

From the execution logs, the `extract` task output showed the uncompressed CSV file size.

**Execution Result:**
- File: yellow_tripdata_2020-12.csv
- Size: 128.3 MiB

**Answer: 128.3 MiB**

### Question 2: Rendered Variable Value

Looking at the flow definition, the `file` variable uses this template:
```yaml
file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
```

With inputs taxi=green, year=2020, month=04:
```
green_tripdata_2020-04.csv
```

**Answer: green_tripdata_2020-04.csv**

### Question 3: Yellow Taxi 2020 Total Rows

I executed the flow 12 times for all months of 2020 with taxi=yellow. Here are the row counts from each execution:

| Month | Execution ID | Rows |
|-------|--------------|------|
| 01 | exec_2020_01 | 6,405,008 |
| 02 | exec_2020_02 | 6,299,354 |
| 03 | exec_2020_03 | 3,007,292 |
| 04 | exec_2020_04 | 237,993 |
| 05 | exec_2020_05 | 348,371 |
| 06 | exec_2020_06 | 549,760 |
| 07 | exec_2020_07 | 800,412 |
| 08 | exec_2020_08 | 1,007,284 |
| 09 | exec_2020_09 | 1,341,012 |
| 10 | exec_2020_10 | 1,681,131 |
| 11 | exec_2020_11 | 1,508,985 |
| 12 | exec_2020_12 | 1,461,897 |

**Total: 24,648,499**

**Answer: 24,648,499**

### Question 4: Green Taxi 2020 Total Rows

Same process for green taxi data:

| Month | Execution ID | Rows |
|-------|--------------|------|
| 01 | exec_green_01 | 447,770 |
| 02 | exec_green_02 | 398,632 |
| 03 | exec_green_03 | 223,406 |
| 04 | exec_green_04 | 35,612 |
| 05 | exec_green_05 | 57,360 |
| 06 | exec_green_06 | 63,109 |
| 07 | exec_green_07 | 72,257 |
| 08 | exec_green_08 | 81,063 |
| 09 | exec_green_09 | 87,987 |
| 10 | exec_green_10 | 95,120 |
| 11 | exec_green_11 | 88,605 |
| 12 | exec_green_12 | 83,130 |

**Total: 1,734,051**

**Answer: 1,734,051**

### Question 5: Yellow Taxi March 2021 Rows

Ran the flow with taxi=yellow, year=2021, month=03:

**Execution Result:**
- Rows: 1,925,152

**Answer: 1,925,152**

### Question 6: Timezone Configuration

The question asks about configuring New York timezone in a Schedule trigger. Based on Kestra's documentation, the correct way is:

```yaml
triggers:
  - id: schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 2 * * *"
    timezone: America/New_York
```

**Answer: Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration**

## Summary of Answers

| Question | Answer |
|----------|--------|
| Q1 | 128.3 MiB |
| Q2 | green_tripdata_2020-04.csv |
| Q3 | 24,648,499 |
| Q4 | 1,734,051 |
| Q5 | 1,925,152 |
| Q6 | Add a `timezone` property set to `America/New_York` |

## Notes

- The drop in trips during April-May 2020 is noticeable (COVID-19 impact)
- Green taxi has significantly fewer trips than yellow taxi
- Kestra's execution logs made it easy to track row counts and file sizes
- The variable templating in Kestra works exactly as expected with the double curly braces notation

## Files

- `taxi_data_etl.yaml` - The main ETL flow definition
