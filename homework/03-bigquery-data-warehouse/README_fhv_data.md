
**Create an external table using the fhv 2019 data.**

```sql
CREATE OR REPLACE EXTERNAL TABLE `bq-data-warehouse-413819.fhv_hw.fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://fhv-data-gt/fhv/fhv_tripdata_2019-*.csv.gz']
);
```


**Create a table in BQ using the fhv 2019 data (do not partition or cluster this table).**

```sql

CREATE OR REPLACE TABLE `bq-data-warehouse-413819.fhv_hw.fhv_nonpartitioned_tripdata`
AS SELECT * FROM `bq-data-warehouse-413819.fhv_hw.fhv_tripdata`;
```


## Question 1:
What is the count for fhv vehicle records for year 2019?

### Answer
```sql
SELECT count(*) FROM `bq-data-warehouse-413819.fhv_hw.fhv_nonpartitioned_tripdata`;

```
**43,244,696**

## Question 2:
Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.  

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
### Answer
```sql
-- External Table - 0 B
SELECT COUNT(DISTINCT(dispatching_base_num)) FROM `bq-data-warehouse-413819.fhv_hw.fhv_tripdata`;

-- Non-partitioned Table - 336.71 MB
SELECT COUNT(DISTINCT(dispatching_base_num)) FROM `bq-data-warehouse-413819.fhv_hw.fhv_nonpartitioned_tripdata`;
```

**0 MB for the External Table and 317.94MB for the BQ Table**
( As instructed - choosing closest matching value )


## Question 3:
How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
### Answer
```sql
SELECT COUNT(*) FROM `bq-data-warehouse-413819.fhv_hw.fhv_nonpartitioned_tripdata` fnt
WHERE fnt.DOlocationID IS NULL 
AND fnt.PUlocationID IS NULL;
```

**717,748**

## Question 4:
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number??
### Answer
**Partition by pickup_datetime Cluster on affiliated_base_number**

## Question 5:
1. Implement the optimized solution you chose for question 4. 
```sql
CREATE OR REPLACE TABLE `bq-data-warehouse-413819.fhv_hw.fhv_partitioned_tripdata`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS (
  SELECT * FROM `bq-data-warehouse-413819.fhv_hw.fhv_tripdata`
);
```

2. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).  

```sql
SELECT DISTINCT(affiliated_base_number) FROM  `bq-data-warehouse-413819.fhv_hw.fhv_nonpartitioned_tripdata`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
```

3. Use the BQ table you created earlier in your from clause and note the estimated bytes.  
   `This query will process 647.87 MB when run.`

4. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed.  
```sql
SELECT DISTINCT(affiliated_base_number) FROM  `bq-data-warehouse-413819.fhv_hw.fhv_partitioned_tripdata`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
```

`This query will process 23.05 MB when run.`  
**What are these values? Choose the answer which most closely matches.**


### Answer

**647.87 MB for non-partitioned table and 23.06 MB for the partitioned table**

## Question 6:
Where is the data stored in the External Table you created?
### Answer
**GCP Bucket**

## Question 7:
It is best practice in Big Query to always cluster your data:
### Answer
**False**