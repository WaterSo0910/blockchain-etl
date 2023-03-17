# Blockchain ETL
### 1. Create - `.env`
```bash
DB_NAME=ethereumetl
DB_USER=otto
DB_PASSWORD=scan
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 2. Install all dependencies
```bash
make setup
```

### 3. Build Timescale-db and Redis
```bash
docker compose up -d
```

### 4. Init database table ([schema](http://140.113.216.115/blockchain/schema))
```
git clone http://140.113.216.115/blockchain/schema
pipenv install --dev --skip-lock
pipenv run python -s ./ethereum/evm.sql --chain ethereum
```

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
    --target-db-url="postgresql://otto:scan@127.0.0.1:5432/ethereumetl" \
    --target-db-schema="ethereum" \
    --enable-enrich \
    --entity-types="block,transaction,receipt,log,token_transfer,trace,contract" \
    --last-synced-block-file=.priv/ethereum/stream-tsdb-lsf.txt \
    >> ./logs/eth.dump.log 2>&1
```
