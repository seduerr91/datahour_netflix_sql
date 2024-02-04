from ingestion.prepare_netflix_data import prepare_netflix_data
from ingestion.prepare_spider_data import prepare_spider_data
from ingestion.prepare_nltk import download_nltk_packages

SQL_NETFLIX_DATA = "data/datasets/netflix.csv"
VECTOR_SPIDER_DATA = "data/datasets/spider.tsv"
SQL_DATABASE_LOCATION = "data/databases/netflix.db"
VECTOR_DATABASE_LOCATION = "data/databases/spider" 

if __name__ == '__main__':
    
    prepare_netflix_data(
        data_location = SQL_NETFLIX_DATA,
        database_location = SQL_DATABASE_LOCATION
    )
    
    prepare_spider_data(
        data_location = VECTOR_SPIDER_DATA,
        database_location = VECTOR_DATABASE_LOCATION
    )
    
    download_nltk_packages()
