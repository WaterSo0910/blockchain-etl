from sqlalchemy.sql import func

from sqlalchemy import (
    Table,
    Column,
    Integer,
    Date,
    DateTime,
    BigInteger,
    String,
    Numeric,
    MetaData,
    Boolean,
)

metadata = MetaData()

BLOCKS = Table(
    "blocks",
    metadata,
    Column("_st", Integer),
    Column("_st_day", Date),
    Column("blknum", BigInteger, primary_key=True),
    Column("blkhash", String),
    Column("tx_count", Integer),
    Column("blk_size", BigInteger),
    Column("stripped_size", BigInteger),
    Column("weight", BigInteger),
    Column("version", BigInteger),
    Column("nonce", String),
    Column("bits", String),
    Column("difficulty", Numeric(38)),
    Column("coinbase_param", String),
)

TRANSACTIONS = Table(
    "txs",
    metadata,
    Column("_st", Integer),
    Column("_st_day", Date),
    Column("blknum", BigInteger),
    Column("txhash", String, primary_key=True),
    Column("txpos", Integer),
    Column("iscoinbase", Boolean),
    Column("tx_in_cnt", Integer),
    Column("tx_in_value", BigInteger),
    Column("tx_out_cnt", Integer),
    Column("tx_out_value", BigInteger),
    Column("tx_size", BigInteger),
    Column("tx_vsize", BigInteger),
    Column("tx_weight", BigInteger),
    Column("tx_version", BigInteger),
    Column("tx_locktime", BigInteger),
    Column("tx_hex", String),
)

TRACES = Table(
    "traces",
    metadata,
    Column("_st", Integer),
    Column("_st_day", Date),
    Column("blknum", BigInteger),
    Column("txhash", String, primary_key=True),
    Column("txpos", Integer),
    Column("iscoinbase", Boolean),
    Column("isin", Boolean),
    Column("pxhash", String, primary_key=True),
    Column("tx_in_value", BigInteger),
    Column("tx_out_value", BigInteger),
    Column("vin_seq", BigInteger),
    Column("vin_idx", BigInteger),
    Column("vin_cnt", BigInteger),
    Column("vin_type", String),
    Column("vout_idx", BigInteger),
    Column("vout_cnt", BigInteger),
    Column("address", String),
    Column("value", BigInteger),
)

HISTORY_BALANCES = Table(
    "history_balances",
    metadata,
    Column("id", BigInteger),
    Column("address", String, primary_key=True),
    Column("blknum", BigInteger, primary_key=True),
    Column("out_blocks", BigInteger),
    Column("vin_blocks", BigInteger),
    Column("cnb_blocks", BigInteger),
    Column("out_txs", BigInteger),
    Column("vin_txs", BigInteger),
    Column("cnb_txs", BigInteger),
    Column("out_xfers", BigInteger),
    Column("vin_xfers", BigInteger),
    Column("cnb_xfers", BigInteger),
    Column("out_value", BigInteger),
    Column("vin_value", BigInteger),
    Column("cnb_value", BigInteger),
    Column("out_1th_st", Integer),
    Column("vin_1th_st", Integer),
    Column("cnb_1th_st", Integer),
    Column("out_nth_st", Integer),
    Column("vin_nth_st", Integer),
    Column("cnb_nth_st", Integer),
    Column("out_1th_blknum", Integer),
    Column("vin_1th_blknum", Integer),
    Column("cnb_1th_blknum", Integer),
    Column("out_nth_blknum", Integer),
    Column("vin_nth_blknum", Integer),
    Column("cnb_nth_blknum", Integer),
    Column("out_1th_st_day", Date),
    Column("vin_1th_st_day", Date),
    Column("cnb_1th_st_day", Date),
    Column("out_nth_st_day", Date),
    Column("vin_nth_st_day", Date),
    Column("cnb_nth_st_day", Date),
    Column("value", BigInteger),
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, server_default=func.current_timestamp()),
)


LATEST_BALANCES = Table(
    "latest_balances",
    metadata,
    Column("id", BigInteger),
    Column("address", String, primary_key=True),
    Column("blknum", BigInteger),
    Column("out_blocks", BigInteger),
    Column("vin_blocks", BigInteger),
    Column("cnb_blocks", BigInteger),
    Column("out_txs", BigInteger),
    Column("vin_txs", BigInteger),
    Column("cnb_txs", BigInteger),
    Column("out_xfers", BigInteger),
    Column("vin_xfers", BigInteger),
    Column("cnb_xfers", BigInteger),
    Column("out_value", BigInteger),
    Column("vin_value", BigInteger),
    Column("cnb_value", BigInteger),
    Column("out_1th_st", Integer),
    Column("vin_1th_st", Integer),
    Column("cnb_1th_st", Integer),
    Column("out_nth_st", Integer),
    Column("vin_nth_st", Integer),
    Column("cnb_nth_st", Integer),
    Column("out_1th_blknum", Integer),
    Column("vin_1th_blknum", Integer),
    Column("cnb_1th_blknum", Integer),
    Column("out_nth_blknum", Integer),
    Column("vin_nth_blknum", Integer),
    Column("cnb_nth_blknum", Integer),
    Column("out_1th_st_day", Date),
    Column("vin_1th_st_day", Date),
    Column("cnb_1th_st_day", Date),
    Column("out_nth_st_day", Date),
    Column("vin_nth_st_day", Date),
    Column("cnb_nth_st_day", Date),
    Column("value", BigInteger),
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, server_default=func.current_timestamp()),
)
