InfluxDB databases configuration:

``> CREATE DATABASE vcsa_rest``<br/>
``> CREATE DATABASE vcsa_telegraf``<br/>
``> CREATE USER admin WITH PASSWORD 's3x1gr4f' WITH ALL PRIVILEGES``<br/>
``> CREATE USER telegraf WITH PASSWORD 't3l3gr4f'``<br/>
``> CREATE USER pollerpy WITH PASSWORD 'p0ll3rpy'``<br/>
``> GRANT ALL ON vcsa_telegraf TO telegraf``<br/>
``> GRANT ALL ON vcsa_rest TO pollerpy``<br/>
``> CREATE RETENTION POLICY "four_months" ON "vcsa_telegraf" DURATION 16w REPLICATION 1``<br/>
``> CREATE RETENTION POLICY "four_months" ON "vcsa_rest" DURATION 16w REPLICATION 1``<br/>
``> DROP RETENTION POLICY autogen ON vcsa_telegraf``<br/>
``> DROP RETENTION POLICY autogen ON vcsa_rest``<br/>
