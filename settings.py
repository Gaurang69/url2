#!/usr/bin/python3
DEBUG = True
DATABASE = "urlshort.db"
FOOBAR = "PONG"
DEFAULT_SCHEMA = '''
CREATE TABLE IF NOT EXISTS pastes (id INT PRIMARY KEY, paste_url TEXT NOT NULL, target TEXT NOT NULL, method_id INT NOT NULL, ip TEXT NOT NULL, timestamp TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS methods (id INT PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS access (id INT PRIMARY KEY NOT NULL, paste_id TEXT NOT NULL, ip TEXT NOT NULL, user_agent TEXT NOT NULL);
'''
