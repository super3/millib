drop table btc_log;
CREATE TABLE IF NOT EXISTS btc_log(
   id INT INTEGER PRIMARY KEY,
   '24h_avg' REAL NOT NULL,
   ask REAL NOT NULL,
   bid REAL NOT NULL,
   last REAL NOT NULL,
   total_vol REAL NOT NULL,
   ts INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS btc_log_ts ON btc_log (ts);
