FROM docker.io/minio/minio:latest

COPY --from=docker.io/minio/mc:latest /usr/bin/mc /usr/bin/mc
RUN mkdir -p /tempdata

# These files are accessed from the project root
# If this breaks, then you likely need to download and extract these files first
COPY datalake/order_products__train.csv /tempdata
COPY datalake/products.csv /tempdata

RUN mkdir /buckets
RUN minio server /buckets & \
    server_pid=$!; \
    until mc alias set local http://localhost:9000 minioadmin minioadmin; do \
        sleep 1; \
    done; \
    mc mb local/bucket; \
    cat /tempdata/order_products__train.csv | mc pipe local/bucket/order_products__train.csv; \
    cat /tempdata/products.csv | mc pipe local/bucket/products.csv; \
    kill $server_pid

CMD ["minio", "server", "/buckets", "--address", ":9000", "--console-address", ":9001"]