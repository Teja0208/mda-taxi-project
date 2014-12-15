
create table teja.trip_data_2013 (
									medallion int, 
									hack_license int, 
									vendor_id string, 
									rate_code int, 
									store_and_fwd_flag string, 
									pickup_datetime timestamp, 
									dropoff_datetime timestamp, 
									passenger_count int, 
									trip_time_in_secs double, 
									trip_distance double, 
									pickup_longitude double, 
									pickup_latitude double, 
									dropoff_longitude double,
									dropoff_latitude double
								)  row format delimited fields terminated by ',';



create table teja.fare_data_2013 (
									medallion int, 
									hack_license int, 
									vendor_id string, 
									pickup_datetime timestamp, 
									payment_type string, 
									fare_amount double, 
									surcharge double, 
									mta_tax double, 
									tip_amount double,
									tolls_amount double,
									total_amount double 
								) row format delimited fields terminated by ',';


LOAD DATA LOCAL INPATH '/home/dg1937/trip_data_2013/' OVERWRITE INTO TABLE trip_data_2013;

LOAD DATA LOCAL INPATH '/home/dg1937/fare_data_2013/' OVERWRITE INTO TABLE fare_data_2013;



-- Impala

create table trip_data_2013 (medallion int, hack_license int, vendor_id string, rate_code int, store_and_fwd_flag string, pickup_datetime timestamp, dropoff_datetime timestamp, passenger_count int, trip_time_in_secs double, trip_distance double, pickup_longitude decimal(20,10), pickup_latitude decimal(20,10), dropoff_longitude decimal(20,10),dropoff_latitude decimal(20,10)) row format delimited fields terminated by ',';

create table taxi.fare_data_2013 (medallion int, hack_license int, vendor_id string, pickup_datetime timestamp, payment_type string, fare_amount double, surcharge double, mta_tax double, tip_amount double,tolls_amount double,total_amount double ) row format delimited fields terminated by ',';


LOAD DATA INPATH '/user/dg1937/impala_trip_data_2013/' OVERWRITE INTO TABLE taxi.trip_data_2013;


LOAD DATA INPATH '/user/dg1937/impala_fare_data_2013/' OVERWRITE INTO TABLE taxi.fare_data_2013;


create external table taxi.ext2_fare_data_2013 (medallion int, hack_license int, vendor_id string, pickup_datetime timestamp, payment_type string, fare_amount decimal(10,4), surcharge decimal(10,4), mta_tax decimal(10,4), tip_amount decimal(10,4),tolls_amount decimal(10,4),total_amount decimal(10,4)) row format delimited fields terminated by ',' location '/user/dg1937/impala_fare_data_2013/';


create external table taxi.ext_taxi_data_2013 (medallion int, hack_license int, vendor_id string, rate_code tinyint, store_and_fwd_flag string, pickup_datetime timestamp, dropoff_datetime timestamp, passenger_count smallint, trip_time_in_secs smallint, trip_distance smallint, pickup_longitude decimal(15,10), pickup_latitude decimal(15,10), dropoff_longitude decimal(15,10),dropoff_latitude decimal(15,10)) row format delimited fields terminated by ',' location '/user/dg1937/impala_taxi_data_2013/';




CREATE TABLE trips_2013 AS  
SELECT 	T1.medallion, 
		T1.hack_license, 
		T1.vendor_id, 
		T1.rate_code, 
		T1.store_and_fwd_flag, 
		T1.pickup_datetime, 
		T1.dropoff_datetime , 
		T1.passenger_count, 
		T1.trip_time_in_secs, 
		T1.trip_distance, 
		T1.pickup_longitude, 
		T1.pickup_latitude, 
		T1.dropoff_longitude, 
		T1.dropoff_latitude, 
		T2.payment_type, 
		T2.fare_amount, 
		T2.surcharge, 
		T2.mta_tax, 
		T2.tip_amount, 
		T2.tolls_amount, 
		T2.total_amount 
FROM taxi.trip_data AS T1 
INNER JOIN taxi.fare_data AS T2 
ON T1.medallion = T2.medallion 
AND T1.hack_license = T2.hack_license 
AND T1.pickup_datetime = T2.pickup_datetime;



CREATE TABLE taxi.trip_data AS ( SELECT CAST(medallion AS INT) medallion, CAST(hack_license AS INT) hack_license, CAST(vendor_id AS STRING) vendor_id, CAST(rate_code AS TINYINT) rate_code, CAST(store_and_fwd_flag AS STRING) store_and_fwd_flag, CAST(pickup_datetime AS TIMESTAMP) pickup_datetime, CAST(dropoff_datetime AS TIMESTAMP) dropoff_datetime , CAST(passenger_count AS SMALLINT) passenger_count, CAST(trip_time_in_secs AS SMALLINT) trip_time_in_secs, CAST(trip_distance AS SMALLINT) trip_distance, CAST(pickup_longitude AS DECIMAL(15,10)) pickup_longitude, CAST(pickup_latitude AS DECIMAL(15,10)) pickup_latitude, CAST(dropoff_longitude AS DECIMAL(15,10)) dropoff_longitude, CAST(dropoff_latitude AS DECIMAL(15,10)) dropoff_latitude FROM taxi.trip_data_2013;


CREATE TABLE trip_data AS SELECT * FROM trip_data_2013 WHERE medallion IS NOT NULL;

CREATE TABLE fare_data AS SELECT * FROM fare_data_2013 WHERE medallion IS NOT NULL;



CREATE TABLE teja.geocoded_test (
									longitude double, 
									latitude double, 
									boro_code tinyint, 
									nta_code string, 
									nta_name string
								) row format delimited fields terminated by ',';


LOAD DATA LOCAL INPATH '/home/dg1937/GeoCoded_longlat/' OVERWRITE INTO TABLE geocoded_test;


INSERT OVERWRITE DIRECTORY '/home/dg1937/trips_nta_data_dir/' SELECT * FROM teja.trips_nta_data;




CREATE EXTERNAL TABLE teja.pickups_count_nta (
												nta_code string, 
												nta_name string, 
												num_pickups int) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n' 
LOCATION '/user/dg1937/pickups_count_nta/';


CREATE EXTERNAL TABLE teja.dropoffs_count_nta (
												nta_code string, 
												nta_name string, 
												num_dropoffs int) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n' 
LOCATION '/user/dg1937/dropoffs_count_nta/';


CREATE EXTERNAL TABLE teja.pickup_dropoff_count_nta (
														p_nta_code string, 
														p_nta_name string, 
														d_nta_code string, 
														d_nta_name string, 
														num_trips int) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n' 
LOCATION '/user/dg1937/pickup_dropoff_count_nta/';


INSERT INTO TABLE pickups_count_nta 
SELECT 	p_nta_code as nta_code, 
		COLLECT_SET(p_nta_name)[0] as nta_name,
		count(*) as num_pickups 
FROM trips_nta_final 
GROUP BY p_nta_code 
ORDER BY num_pickups;


INSERT INTO TABLE dropoffs_count_nta 
SELECT 	d_nta_code as nta_code, 
		COLLECT_SET(d_nta_name)[0] as nta_name,
		count(*) as num_pickups 
FROM trips_nta_final 
GROUP BY d_nta_code 
ORDER BY num_pickups;


INSERT INTO TABLE pickup_dropoff_count_nta 
SELECT 	p_nta_code, 
		COLLECT_SET(p_nta_name)[0] as p_nta_name, 
		d_nta_code, COLLECT_SET(d_nta_name)[0] as d_nta_name, 
		count(*) as num_trips 
FROM trips_nta_final 
GROUP BY p_nta_code, d_nta_code 
ORDER BY p_nta_name, num_trips;





CREATE EXTERNAL TABLE teja.nta_pickups_dropoffs_count (
														nta_code string, 
														nta_name string, 
														num_pickups int, 
														num_dropoffs int) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n' 
LOCATION '/user/dg1937/nta_pickups_dropoffs_count/';


INSERT INTO TABLE teja.nta_pickups_dropoffs_count 
SELECT 	t1.nta_code, 
		t1.nta_name, 
		t1.num_pickups, 
		t2.num_dropoffs 
FROM  teja.pickups_count_nta as t1 
INNER JOIN teja.dropoffs_count_nta t2 
ON t1.nta_code = t2.nta_code;



select * from pickup_dropoff_count_nta;



-- Day of week

SELECT pickup_datetime, from_unixtime(unix_timestamp(pickup_datetime),'EEEE') from trip_data;




SELECT 	AVG(trip_distance) avg_distance, 
		AVG(trip_time_in_secs) avg_time, 
		COUNT(*) trips FROM trip_data;

-- Reuslt :   8.3051372 	811.9999	173179759


SELECT 	FLOOR(((tip_amount) / (fare_amount)) * 100) tip_pct,
  		count(*) trips
FROM fare_data
WHERE payment_type='CRD' 
and fare_amount > 0.00
GROUP BY 1
ORDER BY 1;

---------------------------------------------------------------------------------------------------------
-- pickups and dropoffs aggregated to neighborhood and day of week


CREATE TABLE TEST1 AS 
SELECT 	p_nta_code ,COLLECT_SET(p_nta_name)[0] AS  p_nta_name, 
		from_unixtime(unix_timestamp(pickup_datetime),'EEEE') AS day, 
		count(*) AS num_pickups 
FROM trips_nta_final 
GROUP BY 	p_nta_code ,  
			from_unixtime(unix_timestamp(pickup_datetime),'EEEE') ;

58.146 seconds , map : 134 , reduce : 34

--
CREATE TABLE TEST2 AS 
SELECT 	d_nta_code, COLLECT_SET(d_nta_name)[0] AS d_nta_name, 
		from_unixtime(unix_timestamp(dropoff_datetime),'EEEE') AS day, 
		count(*) AS num_dropoffs 
FROM trips_nta_final 
GROUP BY 	d_nta_code ,  
			from_unixtime(unix_timestamp(dropoff_datetime),'EEEE');

58.991 seconds , map : 134 , reduce : 34

--

CREATE EXTERNAl TABLE nta_day_of_week_pickups_dropoffs 
					(	nta_code string, 
						nta_name string, 
						day string,
						num_pickups int ,
						num_dropoffs int
					) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','  
LINES TERMINATED BY '\n' 
LOCATION '/user/dg1937/nta_day_of_week_pickups_dropoffs/';


INSERT INTO TABLE nta_day_of_week_pickups_dropoffs 
SELECT 	t1.p_nta_code AS nta_code,
		t1.p_nta_name AS nta_name,
		t1.day AS day , 
		t1.num_pickups AS num_pickups, 
		t2.num_dropoffs AS num_dropoffs
FROM TEST1 t1 
INNER JOIN TEST2 t2 
ON t1.p_nta_code = t2.d_nta_code 
AND t1.day = t2.day;

37.266 seconds , map : 25 , reduce : 0


-- merge files in hdfs and otuput as single file to local file system

hdfs dfs -getmerge /user/dg1937/nta_day_of_week_pickups_dropoffs/ /home/dg1937/nta_day_of_week_pickups_dropoffs



-------------------------------------------------------------------------------------------------------------
-- Number of trips aggregated to month and day

CREATE EXTERNAl TABLE month_day_trips (
										month int, 
										day int, 
										trip_count int) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n' 
LOCATION '/user/dg1937/month_day_trips/';


INSERT INTO TABLE month_day_trips 
SELECT 	MONTH(pickup_datetime) AS month, 
		DAY(pickup_datetime) AS day, 
		count(*) AS trip_count 
FROM trips_nta_final 
GROUP BY MONTH(pickup_datetime), 
		DAY(pickup_datetime);

61.27 seconds , map : 134 , reduce : 34


hdfs dfs -getmerge /user/dg1937/month_day_trips/ /home/dg1937/month_day_trips

-----------------------------------------------------------------

-- Number of trips aggregating to Day of week

CREATE EXTERNAL TABLE day_of_week_trips_speed (day_of_week string, hour int,num_trips int)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/day_of_week_trips_speed/';

INSERT INTO TABLE day_of_week_trips 
SELECT 	from_unixtime(unix_timestamp(pickup_datetime),'EEEE') AS day, 
		HOUR(pickup_datetime) AS hour, 
		count(*) AS num_trips 
FROM trips_nta_final  
GROUP BY from_unixtime(unix_timestamp(pickup_datetime),'EEEE'),
		HOUR(pickup_datetime);

67.129 seconds , map : 134, reduce : 34


hdfs dfs -getmerge /user/dg1937/day_of_week_trips_speed/ /home/dg1937/day_of_week_trips_speed



---------------------------------

CREATE EXTERNAL TABLE day_of_week_hour_trips (day_of_week string, hour int, num_trips int, avg_speed double )
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/day_of_week_hour_trips/';



INSERT INTO TABLE test_dan

select t.a,t.b,t.c,t.d,count(*) as count1 from (
  select floor( float(pickup_longitude)* 1000) as a, floor( float(pickup_latitude)*1000) as b, floor( float(dropoff_longitude)*1000) as c, floor( float(dropoff_latitude)*1000) as d from trip_data
) t
group by t.a,t.b,t.c,t.d
order by count1 desc
limit 100;


CREATE EXTERNAL TABLE test_dan (pickup_longitude double, pickup_latitude double , dropoff_longitude double, dropoff_latitude double, count int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/test_dan/';



hdfs dfs -getmerge /user/dg1937/test_dan/ /home/dg1937/test_dan



-----------------------

CREATE EXTERNAL TABLE nta_hour_pickups_dropoffs (nta_code string,nta_name string,hout int,pickups int,dropoffs int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/nta_hour_pickups_dropoffs/';




CREATE TABLE nta_hour_pickups (nta_code string,nta_name string,hour int,count int);

INSERT INTO TABLE nta_hour_pickups SELECT p_nta_code,COLLECT_SET(p_nta_name)[0] p_nta_name,HOUR(pickup_datetime),count(*) FROM trips_nta_final GROUP BY p_nta_code,HOUR(pickup_datetime);



CREATE TABLE nta_hour_dropoffs (nta_code string,nta_name string,hour int,count int);

INSERT INTO TABLE nta_hour_dropoffs SELECT d_nta_code,COLLECT_SET(d_nta_name)[0] d_nta_name,HOUR(dropoff_datetime),count(*) FROM trips_nta_final GROUP BY d_nta_code,HOUR(dropoff_datetime);


INSERT INTO TABLE nta_hour_pickups_dropoffs SELECT T1.*,T2.count FROM  nta_hour_pickups T1 INNER JOIN nta_hour_dropoffs T2 ON T1.nta_code = T2.nta_code AND T1.hour = T2.hour;


hdfs dfs -getmerge /user/dg1937/nta_hour_pickups_dropoffs/ /home/dg1937/nta_hour_pickups_dropoffs;





SELECT 	t.p_nta_code,count(*) as pickups, 
		avg(t.p_tip_per) as p_tip_percentage 
FROM
(SELECT p_nta_code, 
		round(((tip_amount/fare_amount)*100),2) as p_tip_per 
FROM trips_nta_final 
WHERE payment_type = 'CRD' 
AND fare_amount > 0) t
GROUP BY t.p_nta_code;




CREATE TABLE TEST70 AS 
SELECT 	p_nta_code, 
		count(*) as pickups,
		round((avg(tip_amount/fare_amount))*100,2) as p_tip_per 
FROM trips_nta_final 
WHERE payment_type = 'CRD' 
AND fare_amount > 0 and trip_distance > 0
GROUP BY p_nta_code;


CREATE TABLE TEST71 AS 
SELECT d_nta_code, count(*) as dropoffs,
		round((avg(tip_amount/fare_amount))*100,2) as d_tip_per 
FROM trips_nta_final 
WHERE payment_type = 'CRD' 
AND fare_amount > 0 
AND trip_distance > 0
GROUP BY d_nta_code;


CREATE TABLE TEST73 AS
SELECT 	t1.p_nta_code,
		t1.pickups,
		t1.p_tip_per,
		t2.dropoffs,
		t2.d_tip_per 
FROM TEST70 t1 
INNER JOIN TEST71 t2 
ON t1.p_nta_code = t2.d_nta_code;


CREATE EXTERNAL TABLE nta_tip_percentage (nta_code string,pickups int,p_tip_per double,dropoffs int, d_tip_per double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/nta_tip_percentage/';


INSERT INTO TABLE nta_tip_percentage SELECT * FROM test73;




CREATE EXTERNAL TABLE nta_p_tip_per (nta_code string, picups int,p_tip_per double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/nta_p_tip_per/';


CREATE EXTERNAL TABLE nta_d_tip_per (nta_code string, dropoffs int,d_tip_per double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/nta_d_tip_per/';


INSERT INTO TABLE nta_p_tip_per SELECT * FROM test50;

INSERT INTO TABLE nta_d_tip_per SELECT * FROM test51;






IMPALA:

CREATE TABLE test10 AS 
SELECT FLOOR((T.tip_amount / T.fare_amount) * 100) as tip_pct,count(*) FROM 
( SELECT tip_amount,fare_amount from trips_nta_final where payment_type='CRD' and fare_amount > 0 ) T 
GROUP BY tip_pct order by tip_pct limit 51;

HIVE :

CREATE EXTERNAL TABLE tip_pct_trips (tip_pct int, trips int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/tip_pct_trips/';

INSERT INTO TABLE tip_pct_trips SELECT * FROM test10;

--------------------------

CREATE TABLE test20 AS 
SELECT T.p_nta_code,T.tip_pct,count(*) FROM 
( SELECT p_nta_code,FLOOR((tip_amount / fare_amount) * 100) tip_pct from trips_nta_final where payment_type='CRD' and fare_amount > 0 AND trip_distance > 0 AND trip_distance < 50  AND tip_amount <= 200) T 
GROUP BY p_nta_code,tip_pct order by p_nta_code,tip_pct;


CREATE TABLE test21 AS
SELECT * FROM test20 WHERE tip_pct < 51 ORDER BY p_nta_code,tip_pct;




CREATE TABLE test22 AS 
SELECT T.d_nta_code,T.tip_pct,count(*) FROM 
( SELECT d_nta_code,FLOOR((tip_amount / fare_amount) * 100) tip_pct from trips_nta_final where payment_type='CRD' and fare_amount > 0 AND trip_distance > 0 AND trip_distance < 50  AND tip_amount <= 200 ) T 
GROUP BY d_nta_code,tip_pct order by d_nta_code,tip_pct;


CREATE TABLE test23 AS
SELECT * FROM test22 WHERE tip_pct < 51 ORDER BY d_nta_code,tip_pct;


CREATE TABLE test24 AS 
SELECT T1.p_nta_code,T1.tip_pct as p_tip_pct,T1.`_c2` as pickups,T2.tip_pct as d_tip_pct ,T2.`_c2` as dropoffs  FROM test21 T1 INNER JOIN test23 T2 ON T1.p_nta_code = T2.d_nta_code AND T1.tip_pct = T2.tip_pct;


CREATE TABLE test25 AS SELECT t1.p_nta_code,t2.nta_name,t1.p_tip_pct,t1.pickups,t1.d_tip_pct,t1.dropoffs FROM test24 t1 INNER JOIN pickups_count_nta t2 ON t1.p_nta_code = t2.nta_code; 


CREATE EXTERNAL TABLE tip_pct_nta (nta_code string,nta_name string,p_tip_pct int, pickups int, d_tip_pct int,dropoffs int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/tip_pct_nta/';

INSERT INTO TABLE tip_pct_nta SELECT * FROM test25;

----------------

CREATE TABLE test26 as
SELECT T.p_nta_code, ROUND(AVG(T.tip_amount),2)  as avg_tip FROM 
(SELECT p_nta_code, tip_amount FROM trips_nta_final WHERE payment_type='CRD' and fare_amount > 0 AND trip_distance > 0 AND trip_distance < 50 AND trip_distance > 0 AND trip_distance < 50  AND tip_amount <= 200) T
GROUP BY T.p_nta_code;




CREATE TABLE test27 as
SELECT T.d_nta_code, ROUND(AVG(T.tip_amount),2)  as avg_tip FROM 
(SELECT d_nta_code, tip_amount FROM trips_nta_final WHERE payment_type='CRD' and fare_amount > 0 AND trip_distance > 0 AND trip_distance < 50 AND trip_distance > 0 AND trip_distance < 50  AND tip_amount <= 200) T
GROUP BY T.d_nta_code;


CREATE TABLE test28 as
SELECT t1.p_nta_code,t1.avg_tip as p_avg_tip,t2.avg_tip as d_avg_tip FROM test26 t1 INNER JOIN test27 t2 ON t1.p_nta_code = t2.d_nta_code;


CREATE TABLE test29 as
SELECT t1.p_nta_code,t2.nta_name,t1.p_avg_tip as p_avg_tip,t1.d_avg_tip as d_avg_tip FROM test28 t1 INNER JOIN pickups_count_nta t2 ON t1.p_nta_code = t2.nta_code;


CREATE EXTERNAL TABLE tip_avg_nta (nta_code string, nta_name string, p_avg_tip double , d_avg_tip double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/tip_avg_nta/';


INSERT INTO TABLE tip_avg_nta SELECT * FROM test29;q




---------------

CREATE TABLE test30 as
SELECT t1.p_nta_code,round(AVG(t1.trip_distance),2),count(*) as count1 FROM
(SELECT p_nta_code,trip_distance FROM trips_nta_final WHERE payment_type = 'CRD' AND fare_amount > 0 AND trip_distance > 0 AND trip_distance < 50 ) t1
GROUP BY t1.p_nta_code;



CREATE TABLE test31 as
SELECT t1.d_nta_code,round(AVG(t1.trip_distance),2),count(*) as count1 FROM
(SELECT d_nta_code,trip_distance FROM trips_nta_final WHERE payment_type = 'CRD' AND fare_amount > 0  AND trip_distance > 0 AND trip_distance < 50 ) t1
GROUP BY t1.d_nta_code;


CREATE TABLE test32 as
SELECT t1.p_nta_code, t1.`_c1` as pickup_dist,t2.`_c1` as dropoff_dist,t1.count1 as count1, t2.count1 as count2 FROM test30 t1 INNER JOIN test31 t2 ON t1.p_nta_code = t2.d_nta_code;




CREATE EXTERNAL TABLE avg_trip_dist_crd (nta_code string, p_avg_dist double , d_avg_dist double , pickups int, dropoffs int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/avg_trip_dist_crd/';

INSERT INTO TABLE avg_trip_dist_crd FROM SELECT * FROM test32;



---------------------------

CREATE TABLE TEST33 AS 
SELECT T.p_nta_code,round(avg(T.trip_distance),2) as p_avg_dist, count(*) as pickups FROM
(SELECT p_nta_code,trip_distance FROM trips_nta_final WHERE fare_amount > 0 AND trip_distance > 0 AND trip_distance < 50 ) T
GROUP BY T.p_nta_code;



CREATE TABLE TEST34 AS 
SELECT T.d_nta_code,round(avg(T.trip_distance),2) as d_avg_dist, count(*) as dropoffs FROM
(SELECT d_nta_code,trip_distance FROM trips_nta_final WHERE fare_amount > 0 AND trip_distance > 0 AND trip_distance < 50 ) T
GROUP BY T.d_nta_code;


CREATE TABLE TEST35 AS
SELECT t1.p_nta_code,t1.p_avg_dist,t1.pickups,t2.d_avg_dist,t2.dropoffs FROM TEST33 t1 INNER JOIN TEST34 t2 ON t1.p_nta_code = t2.d_nta_code;



CREATE EXTERNAL TABLE avg_distance (nta_code string, p_avg_dist double ,pickups int,d_avg_dist double, dropoffs int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' LOCATION '/user/dg1937/avg_distance/';


INSERT INTO TABLE avg_distance SELECT * FROM TEST35;
