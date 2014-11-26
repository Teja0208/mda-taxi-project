-- http://www.orzota.com/hive-tutorial-for-beginners/

hadoop fs -mkdir input
hadoop fs -put ~/nyu/taxis/trip_data_1.csv

--

CREATE TABLE IF NOT EXISTS trip_data_1 ( -- must be same name as CSV file
medallion STRING,
hack_license STRING,
vendor_id STRING,
rate_code STRING,
store_and_fwd_flag STRING,
pickup_datetime STRING,
dropoff_datetime STRING,
passenger_count INT,
trip_time_in_secs INT,
trip_distance FLOAT,
pickup_longitude DOUBLE,
pickup_latitude DOUBLE,
dropoff_longitude DOUBLE,
dropoff_latitude DOUBLE)
COMMENT 'Trip Data Table'
ROW FORMAT DELIMITED  
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE
LOCATION '/Users/dgopstein/nyu/taxis/hive/trip_data/' ; -- In order to JOIN tables they must live in separate directories

LOAD DATA INPATH '/Users/dgopstein/nyu/taxis/hive/trip_data_1.csv' OVERWRITE INTO TABLE trip_data_1;

----

CREATE TABLE IF NOT EXISTS trip_fare_1 (
medallion STRING,
hack_license STRING,
vendor_id STRING,
pickup_datetime STRING,
payment_type STRING,
fare_amount FLOAT,
surcharge FLOAT,
mta_tax FLOAT,
tip_amount FLOAT,
tolls_amount FLOAT,
total_amount FLOAT)
COMMENT 'Trip Fare Table'
ROW FORMAT DELIMITED  
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE
LOCATION '/Users/dgopstein/nyu/taxis/hive/trip_fare/' ;

LOAD DATA INPATH '/Users/dgopstein/nyu/taxis/hive/trip_fare_1.csv' OVERWRITE INTO TABLE trip_fare_1;

----

-- ALTER TABLE trip_data_1 CHANGE passenger_count passenger_count INT;

SELECT * FROM trip_data_1 limit 10;

-- See different statistics of taxis trips grouped by passenger_count
SELECT passenger_count, count(passenger_count) as count, avg(trip_time_in_secs) as avg_time, avg(trip_distance) as avg_dist FROM trip_data_1 GROUP BY passenger_count ORDER BY passenger_count;

-- See if tips are correlated with passenger_count
SELECT td.passenger_count, count(td.passenger_count), avg(tf.tip_amount) FROM trip_data_1 td JOIN trip_fare_1 tf ON td.hack_license=tf.hack_license AND td.pickup_datetime=tf.pickup_datetime GROUP BY passenger_count ORDER BY passenger_count;

0   166 1.6542168798777892
1   10471906    1.2879084829806073
2   1986256 1.2387547047146819
3   597527  1.1261642546760466
4   281002  1.0406808826767322
5   920062  1.2635443237227921
6   520079  1.2580999014543226
9   1   0.0
208 1   0.0
255 1   1.0
Time taken: 249.995 seconds, Fetched: 10 row(s)

------

-- See if tips are correlated with passenger_count: as percentage of fare
SELECT td.passenger_count, count(td.passenger_count), avg(tf.tip_amount/tf.fare_amount) FROM trip_data_1 td JOIN trip_fare_1 tf ON td.hack_license=tf.hack_license AND td.pickup_datetime=tf.pickup_datetime GROUP BY passenger_count ORDER BY passenger_count;

0   166 0.036892946395799674
1   10471906    0.10885568875697478
2   1986256 0.10022989513737218
3   597527  0.09499373876451458
4   281002  0.08576389484282076
5   920062  0.10582323146577562
6   520079  0.10591563506694424
9   1   0.0
208 1   0.0
255 1   0.125
Time taken: 259.604 seconds, Fetched: 10 row(s)


-- See if tips are correlated with passenger_count: as percentage of fare, only using credit cards
SELECT td.passenger_count, count(td.passenger_count), avg(tf.tip_amount/tf.fare_amount) FROM trip_data_1 td JOIN trip_fare_1 tf ON td.hack_license=tf.hack_license AND td.pickup_datetime=tf.pickup_datetime WHERE payment_type = 'CRD' GROUP BY passenger_count ORDER BY passenger_count;
0   140 0.04374449358359104
1   5596098 0.20346669270791154
2   982731  0.20242352657446547
3   280622  0.20210735556068354
4   118894  0.20217453635643462
5   488683  0.19897383077828493
6   276877  0.1986082919383359
255 1   0.125

-- See if tips are correlated with passenger_count: as percentage of fare, grouped by payment_type
SELECT payment_type, td.passenger_count, count(td.passenger_count), concat(format_number(100 * avg(tf.tip_amount/tf.fare_amount), 2), '%') FROM trip_data_1 td JOIN trip_fare_1 tf ON td.hack_license=tf.hack_license AND td.pickup_datetime=tf.pickup_datetime GROUP BY passenger_count, payment_type ORDER BY payment_type, passenger_count;
CRD 0   140 4.37%
CRD 1   5596098 20.35%
CRD 2   982731  20.24%
CRD 3   280622  20.21%
CRD 4   118894  20.22%
CRD 5   488683  19.90%
CRD 6   276877  19.86%
CRD 255 1   12.50%
CSH 0   21  0.00%
CSH 1   4832696 0.00%
CSH 2   999493  0.00%
CSH 3   315590  0.00%
CSH 4   161176  0.00%
CSH 5   430793  0.00%
CSH 6   242793  0.00%
CSH 9   1   0.00%
CSH 208 1   0.00%
DIS 0   1   0.00%
DIS 1   9738    0.24%
DIS 2   984 0.09%
DIS 3   261 0.00%
DIS 4   180 0.09%
DIS 5   7   0.00%
NOC 0   4   0.00%
NOC 1   28749   0.07%
NOC 2   2515    0.11%
NOC 3   865 0.00%
NOC 4   632 4.97%
NOC 5   18  0.00%
UNK 1   4625    22.18%
UNK 2   533 22.76%
UNK 3   189 21.58%
UNK 4   120 22.30%
UNK 5   561 22.85%
UNK 6   409 22.85%
Time taken: 277.312 seconds, Fetched: 35 row(s)

-- One block radius around MSG
-- top: 40.752552, -73.994297
-- bottom: 40.748878, -73.993428
-- right: 40.749919, -73.990231
-- left: 40.750732, -73.995960

-- How many people are dropped off at MSG/Penn Station on Knicks game day and non Knicks game day. (Was there another event on the 14th that wasn't the Knics?)
SET window=0.005;
SELECT count(*) FROM trip_data_1 WHERE dropoff_latitude > 40.750556 - ${hiveconf:window} AND dropoff_latitude < 40.750556 + ${hiveconf:window} AND dropoff_longitude > -73.993611 - ${hiveconf:window} AND dropoff_longitude < -73.993611 + ${hiveconf:window} AND dropoff_datetime > '2013-01-07 19:00:00' AND dropoff_datetime < '2013-01-07 19:30:00';
891

SELECT count(*) FROM trip_data_1 WHERE dropoff_latitude > 40.750556 - ${hiveconf:window} AND dropoff_latitude < 40.750556 + ${hiveconf:window} AND dropoff_longitude > -73.993611 - ${hiveconf:window} AND dropoff_longitude < -73.993611 + ${hiveconf:window} AND dropoff_datetime > '2013-01-14 19:00:00' AND dropoff_datetime < '2013-01-14 19:30:00';
565


--------

-- How many Manhattan taxis drive to JFK

-- left: 40.646292, -73.799394
-- top: 40.652837, -73.785017

SELECT count(*) FROM trip_data_1 WHERE dropoff_latitude < 40.652837 AND dropoff_longitude > -73.799394;
367120

---------

-- Average distance each cabbie drives

INSERT OVERWRITE LOCAL DIRECTORY '/Users/dgopstein/nyu/taxis/hive/output' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' SELECT hack_license, count(*), avg(trip_distance) FROM trip_data_1 GROUP BY hack_license;

--
-- Lazy cabbie: 0A22C2D7A7AF74AE37381D399F6315EC
