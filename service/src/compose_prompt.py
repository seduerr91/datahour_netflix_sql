from nltk.tokenize import word_tokenize
from nltk import pos_tag
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

VECTOR_DATABASE_LOCATION = "data/databases/spider"

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_database = Chroma(persist_directory=VECTOR_DATABASE_LOCATION, embedding_function=embedding_function)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def mask_human_question(question):
    tokens = word_tokenize(question)
    pos_tags = pos_tag(tokens)
    
    masked_question = []
    for word, tag in pos_tags:
        if tag.startswith('NN'): masked_question.append('<mask>')
        elif is_number(word): masked_question.append('<unk>')
        else: masked_question.append(word)
    return ' '.join(masked_question)


def compose_prompt(question: str) -> str:
    schema = "CREATE TABLE \"Netflix\" (\n\tuuid VARCHAR NOT NULL, \n\tweek DATE, \n\tcategory VARCHAR, \n\tweekly_rank INTEGER, \n\tshow_title VARCHAR, \n\tseason_title VARCHAR, \n\tweekly_hours_viewed INTEGER, \n\truntime FLOAT, \n\tweekly_views INTEGER, \n\tcumulative_weeks_in_top_10 INTEGER, \n\tis_staggered_launch BOOLEAN, \n\tepisode_launch_detail TEXT, \n\tPRIMARY KEY (uuid)\n)"
    masked_human_question = mask_human_question(question)
    similar_query_context = vector_database.similarity_search(query=masked_human_question, k=5)
    related_queries = "\n".join([Document.metadata['Pairs'] for Document in similar_query_context])
    prompt = f"""
#### Generate a sqlite conform query only and with no explanation\n
/* Schema & Types: {schema}*/
/* Some example questions and corresponding SQL queries are provided based on similar problems:\n
{related_queries}\n
/* Answer the following: {question} */\n
    """
    return prompt