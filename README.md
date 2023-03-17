# Blockchain ETL

### 1. Create - `.env`

### 2. Install all dependencies

```bash
make setup
```

### 3. Build Timescale-db and Redis

```bash
docker compose up -d
```

### 4. Init database table ([schema](https://github.com/WaterSo0910/ethereum-tsdb/blob/main/schema/evm.sql))

### 4. Run ETL

```bash
mkdir -p logs
./etl dump2 \
    --chain=ethereum \
    --lag=10 \
    --max-workers=4 \
    --block-batch-size=10 \
    --start-block=16848698 \
    --batch-size=50 \
    --provider-uri="http://127.0.0.1:8545" \
    --target-db-url="postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME" \
    --target-db-schema="ethereum" \
    --enable-enrich \
    --entity-types="block,transaction,receipt,log,token_transfer,trace,contract" \
    --last-synced-block-file=.priv/ethereum/stream-tsdb-lsf.txt \
    >> ./logs/eth.dump.log 2>&1
```
