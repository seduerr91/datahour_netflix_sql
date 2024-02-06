.PHONY: help clean
.DEFAULT_GOAL := help

install: # make a virtual environment & install dependencies
	python3 -m venv env; source env/bin/activate
	pip3 install -r service/requirements.txt

ingest: # download, prepare, and ingest dataset into databases
	rm -rf service/data/databases/spider
	rm -f service/data/databases/netflix.db
	cd service; python3 data/ingest.py

run: # run code locally
	clear
	cd service; python3 main.py

query: # run a sample query 
	clear
	python3 service/queries/query.py

validation: # validate all test queries
	clear
	python3 service/queries/validation_queries.py
