####

% ```
gcloud compute instances create datasette-vm \
    --zone=us-east1-b \
    --machine-type=e2-highmem-4 \
    --boot-disk-size=50GB \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server,https-server
    ```

% ```gcloud compute firewall-rules create allow-datasette \
    --allow tcp:8001 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server```
    
% `gcloud compute scp pd-eua-data.db datasette-vm:~/pd-eua-data.db --zone=us-east1-b`

#### login to virtual machine
% `gcloud compute ssh datasette-vm --zone=us-east1-b`

#### Notes on using Datasette to view CSV files on the virtual machine



$ ```cd ~```

$ ```source datasette-env/bin/activate```

$ ```datasette pd-eua-data.db --host 0.0.0.0 --port 8001 --setting max_returned_rows 1000 --setting sql_time_limit_ms 30000 --setting facet_time_limit_ms 15000 --setting facet_suggest_time_limit_ms 150 --setting max_csv_mb 100 --setting cache_size_kb 64000```
