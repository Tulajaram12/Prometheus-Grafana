# HOW TO SETUP INFRASTRUCTURE AND RUN INFRASTRUCTURE

## SETUP OF INFRASTRUCTURE IN PROMETHEUS

---

### 📦 Installing Prometheus

Follow this URL to install Prometheus:  
👉 https://www.cherryservers.com/blog/install-prometheus-ubuntu

---

### 📊 Installing Grafana

Follow this URL to install Grafana:  
👉 https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-grafana-on-ubuntu-22-04

---

### 📈 Installing Prometheus Node Exporter

👉 https://www.devopstricks.in/installing-node-exporter-on-ubuntu/

---

### 🛢️ Installing MySQL Database

👉 https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04

---

### 📦 Installing MySQL Exporter

Use both URLs below to install and troubleshoot `mysqld-exporter`:  
- https://installati.one/install-prometheus-mysqld-exporter-ubuntu-22-04/  
- https://www.devopsschool.com/blog/install-and-configure-prometheus-mysql-exporter/

---

### 📥 Installing Log Collector Fluent-Bit

```bash
snap install fluent-bit

sudo mkdir /etc/fluent
sudo vi /etc/fluent-bit/fluent-bit.conf


[SERVICE]
    Flush        1
    Daemon       Off
    Log_Level    info
    Parsers_File parsers.conf

[INPUT]
    Name         tail
    Path         /var/log/flask_app.log
    Tag          flask_app

[INPUT]
    Name         tail
    Path         /var/log/syslog
    Tag          system_logs

[INPUT]
    Name         tail
    Path         /var/log/nginx/access.log
    Tag          access_logs

[OUTPUT]
    Name         loki
    Match        *
    Host         localhost
    Port         3100
    Labels       job=fluentbit,source=$TAG


📦 Installing Loki
Create directories:
``` bash
sudo mkdir -p /etc/loki/{boltdb-cache,chunks,compactor,index,wal}
touch /etc/loki/loki-local-config.yaml
sudo chown -R $USER:$USER /etc/loki


Create the config file /etc/loki/loki-local-config.yaml:

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

Run Loki using Docker:
```bash
sudo apt install docker.io -y
docker run -d --name=loki -p 3100:3100 -v /etc/loki:/etc/loki grafana/loki:2.9.0 -config.file=/etc/loki/loki-local-config.yaml



 Configure Prometheus
Edit /etc/prometheus/prometheus.yml to add targets like:
- job_name: 'node_exporter'
  static_configs:
    - targets: ['localhost:9100']


 Run Services
```bash
# Run the Flask app
cd PrometheusRequestApp
nohup python3 app.py >/dev/null 2>&1 &

# Restart Prometheus components
sudo systemctl restart prometheus
sudo systemctl restart grafana-server
sudo systemctl restart prometheus-node-exporter
sudo systemctl restart prometheus-mysqld-exporter


Access Services
Prometheus: http://your-server-ip:9090

Grafana: http://your-server-ip:3000

In Grafana:

Import dashboards for node exporter, MySQL exporter, and Loki

Add data sources: Prometheus and Loki
