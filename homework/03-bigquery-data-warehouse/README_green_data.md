# SETUP
**Create an external table using the Green Taxi Trip Records Data for 2022.
**

```sql
CREATE OR REPLACE EXTERNAL TABLE `mage-de-zoomcamp.green.green_data`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://mage-zoomcamp-rekt/green/green_tripdata_2022-*.parquet']
);
```

**Create a table in BQ using the Green Taxi Trip Records for 2022 (do not partition or cluster this table)**

```sql
CREATE OR REPLACE TABLE `mage-de-zoomcamp.green.green_nonpartitioned_tripdata`
AS SELECT * FROM `mage-de-zoomcamp.green.green_data`;
```

## Question 1:
What is count of records for the 2022 Green Taxi Data??

### Answer
```sql
SELECT count(*) FROM `bq-data-warehouse-413819.fhv_hw.fhv_nonpartitioned_tripdata`;

```
**840,402**


## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
### Answer
```sql
-- External Table - 0 B
SELECT COUNT(DISTINCT(PULocationID)) FROM `mage-de-zoomcamp.green.green_data`;

-- Non-partitioned Table - 6.41 MB
SELECT COUNT(DISTINCT(PULocationID)) FROM `mage-de-zoomcamp.green.green_nonpartitioned_tripdata`;
```
**0 MB for the External Table and 6.41MB for the Materialized Table**


## Question 3:
How many records have a fare_amount of 0?

### Answer
```sql
SELECT COUNT(*) FROM `mage-de-zoomcamp.green.green_nonpartitioned_tripdata` gnt
WHERE gnt.fare_amount = 0;
```

**1,622**

## Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

```sql
CREATE OR REPLACE TABLE `mage-de-zoomcamp.green.green_partitioned_tripdata`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS (
  SELECT * FROM `mage-de-zoomcamp.green.green_data`
);
```

### Answer
**Partition by lpep_pickup_datetime Cluster on PUlocationID**


## Question 5:
1. Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime  06/01/2022 and 06/30/2022 

2. Use the materialized table you created earlier in your from clause and note the estimated bytes.
   ```sql
   SELECT DISTINCT(PULocationID) FROM `mage-de-zoomcamp.green.green_nonpartitioned_tripdata`
   WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
   ```

   `This query will process 12.82 MB when run.`

3. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed.  

   ```sql
   SELECT DISTINCT(PULocationID) FROM `mage-de-zoomcamp.green.green_partitioned_tripdata`
   WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
   ```

`This query will process 1.12 MB when run.`

### Answer
**12.82 MB for non-partitioned table and 1.12 MB for the partitioned table.**

## Question 6:
Where is the data stored in the External Table you created?
### Answer
**GCP Bucket**

## Question 7:
It is best practice in Big Query to always cluster your data:
### Answer
**False**
