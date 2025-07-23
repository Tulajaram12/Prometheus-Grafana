HOW TO SETUP INFRASTRUCTURE AND RUN INFRASTRUCTURE

SETUP OF INFRASTRUCTURE IN PROMETHEUS

Installing Prometheus
1) follow this url to install the Prometheus i.e https://www.cherryservers.com/blog/install-prometheus-ubuntu

Installing Grafana
2) follow this url to install the Grafana i.e https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-grafana-on-ubuntu-22-04

Installing Prometheus Node Exporter
3) follow this url to install the node exporter https://www.devopstricks.in/installing-node-exporter-on-ubuntu/

Installing Mysql database on the server
4) https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04

Installing Mysql exporter
Used Both urls to install and troubleshoot mysqld-exporter
5) https://installati.one/install-prometheus-mysqld-exporter-ubuntu-22-04/
6) https://www.devopsschool.com/blog/install-and-configure-prometheus-mysql-exporter/

Installing log collector fluent-bit
7) snap install fluent-bit

Configure the fluent-bit with the below file
8)sudo mkdir /etc/fluent 
9)sudo vi /etc/fluent-bit/fluent-bit.conf

[SERVICE]
    Flush        1
    Daemon       Off
    Log_Level    info
    Parsers_File parsers.conf

[INPUT]
    Name   tail
    Path   /var/log/flask_app.log
    Tag    flask_app

[INPUT]
    Name   tail
    Path   /var/log/syslog
    Tag    system_logs

[INPUT]
    Name   tail
    Path   /var/log/nginx/access.log
    Tag    access_logs

[OUTPUT]
    Name   loki
    Match  *
    Host   localhost
    Port   3100
    Labels job=fluentbit,source=$TAG


Installing loki 
Create the below directories
9)  sudo mkdir /etc/loki
10) sudo mkdir /etc/loki/boltdb-cache
11) sudo mkdir /etc/loki/chunks
12) sudo mkdir /etc/loki/compactor
13) sudo mkdir /etc/loki/index
14) sudo mkdir /etc/loki/loki-local-config.yaml
15) sudo mkdir /etc/loki/wal

change the ownership by below command
16) sudo chown -R /etc/loki

Now add the following configuration in /etc/loki/loki-local-config.yaml
17) vi /etc/loki/loki-local-config.yaml

auth_enabled: false

server:
  http_listen_port: 3100
  http_listen_address: 0.0.0.0
  grpc_listen_port: 9095

ingester:
  wal:
    enabled: true
    dir: /etc/loki/wal
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 5m
  chunk_retain_period: 30s
  max_transfer_retries: 0

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  max_streams_per_user: 100000

schema_config:
  configs:
    - from: 2022-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /etc/loki/index
    cache_location: /etc/loki/boltdb-cache
    shared_store: filesystem
  filesystem:
    directory: /etc/loki/chunks

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: true
  retention_period: 168h

compactor:
  working_directory: /etc/loki/compactor
  shared_store: filesystem


Install docker on the server
18) sudo apt install docker.io -y

Now Run the loki by using below docker command
19)  docker run -d --name=loki -p 3100:3100   -v /etc/loki:/etc/loki   grafana/loki:2.9.0   -config.file=/etc/loki/loki-local-config.yaml

Also configure the targets in /etc/prometheus/prometheus.yml
Add the Ports i.e 9090, 3000 in the security groups

Now Run the prometheus server, grafana server
20) Prometheus  http://IP:9090
21) Grafana     http://IP:3000


Now login Grafana Import the dasboards like nodeexporter, mysqldexporter, loki,  and add the datasources i.e prometheus and loki 



RUNNING THE INFRASTRUCTURE in MY SERVER

  1) sudo su - root
  2) cd PrometheusRequestApp
     Run the Python flaskapp
  3) nohup python3 app.py >/dev/null 2>&1 &
  4) sudo systemctl restart prometheus
  5) sudo systemctl restart grafana-server
  6) sudo systemctl restart prometheus-node-exporter
  7) sudo systemctl restart prometheus-mysqld-exporter


 




