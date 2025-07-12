First effort to review newly-released EUA documents (Source: search for `eua` at https://phmpt.org) 

1. Download the CSV from this repository
2. Visit https://mroswell.github.io/eua-review
3. Upload the csv file that has used AI to tag the first 7 pages of each document
4. Click on a tag name or bar to access the files that were given those tags.

#### Notes on using Datasette to view CSV files on the virtual machine


$ ```cd ~```

$ ```source datasette-env/bin/activate```

$ ```datasette pd-eua-data.db --host 0.0.0.0 --port 8001 --setting max_returned_rows 1000 --setting sql_time_limit_ms 30000 --setting facet_time_limit_ms 15000 --setting facet_suggest_time_limit_ms 150 --setting max_csv_mb 100 --setting cache_size_kb 64000```
