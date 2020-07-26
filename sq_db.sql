CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
login text NOT NULL,
password_hash text NOT NULL,
registration_date text NOT NULL
);
CREATE TABLE IF NOT EXISTS posts (
post_id integer PRIMARY KEY AUTOINCREMENT,
author_id text NOT NULL,
title text NOT NULL,
body text NOT NULL,
create_date text NOT NULL
);