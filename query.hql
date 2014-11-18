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
