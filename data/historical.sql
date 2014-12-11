CREATE TABLE eod (
   symbol TEXT NOT NULL,
   ts INTEGER NOT NULL,
   open REAL NOT NULL,
   close REAL NOT NULL,
   high REAL NOT NULL,
   low REAL,
   volume INTEGER NOT NULL,
   UNIQUE (symbol, ts)
);
