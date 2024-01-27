### Module 1 Homework

### Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


### Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

# Q1 ANSWER
`--rm`

### Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0

# Q2 ANSWER
`docker run -it --entrypoint /bin/bash python:3.9`
0.42.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


### Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612
- 15859
- 89009
  
# Q3 Answer
```sql
SELECT
	COUNT(1)
FROM green_taxi_data g
WHERE 
	CAST(g.lpep_pickup_datetime AS DATE) = '2019-09-18' AND
	CAST(g.lpep_dropoff_datetime AS DATE) = '2019-09-18'
```

`15612`

### Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

# Q4 Answer
```sql

SELECT
	CAST(g.lpep_pickup_datetime AS DATE),
	SUM(g.trip_distance) td
FROM green_taxi_data g
GROUP BY 1
ORDER BY td DESC;
```

`2019-09-26`

### Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

# Q5 Answer
```sql
SELECT
	CAST(g.lpep_pickup_datetime AS DATE),
	z."Borough",
	SUM(g.total_amount) AS gc
FROM green_taxi_data g
JOIN zones z
ON 
	g."PULocationID" = z."LocationID"
WHERE 
	CAST(g.lpep_pickup_datetime AS DATE) = '2019-09-18' AND 
	z."Borough" != 'Unknown'
GROUP BY 1, 2
HAVING SUM(g.total_amount) > 50000
ORDER BY gc DESC;
```

`"Brooklyn" "Manhattan" "Queens"`

### Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

# Q6 Answer
```sql
WITH SeptemberPickups AS (
    SELECT
        g.lpep_dropoff_datetime,
        g."PULocationID",
        g."DOLocationID",
        g.tip_amount,
        z."Zone" AS "PickupZone"
    FROM
        green_taxi_data g
    JOIN
        zones z ON g."PULocationID" = z."LocationID"
    WHERE
		CAST(g.lpep_pickup_datetime AS DATE) >= '2019-09-01' AND
		CAST(g.lpep_dropoff_datetime AS DATE) < '2019-10-01' AND
        z."Zone" = 'Astoria'
)
SELECT
    z."Zone" AS "DropoffZone"
FROM
    SeptemberPickups s
JOIN
    zones z ON s."DOLocationID" = z."LocationID"
WHERE
    s.tip_amount = (
        SELECT
            MAX("tip_amount")
        FROM
            SeptemberPickups
    );
```

`JFK Airport`

### Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


### Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

# Q7 Answer
```

Terraform used the selected providers to generate the following execution plan. Resource actions are
indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "bigquery_dataset_hw_1"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "EU"
      + project                    = "terraform-demo-412515"
      + self_link                  = (known after apply)
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EU"
      + name                        = "terraform-demo-412515-data-lake-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }
          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 2s [id=projects/terraform-demo-412515/datasets/bigquery_dataset_hw_1]
google_storage_bucket.data-lake-bucket: Creation complete after 3s [id=terraform-demo-412515-data-lake-bucket]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

### Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET
