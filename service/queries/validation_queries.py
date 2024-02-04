import requests
import time

import pandas as pd
netflix = pd.read_csv('service/data/datasets/netflix.csv', sep=',', )

questions = [
    #In the Netflix data,  For column 'week'
    'In the Netflix data, What is the earliest week?',
    'In the Netflix data, What is the latest week?',
    'In the Netflix data, How many unique weeks are there?',
    #In the Netflix data,  For column 'category'
    'In the Netflix data, What are the unique categories available?',
    'In the Netflix data, How many times is Films (English) listed?',
    'In the Netflix data, How many categories have films listed?',
    #In the Netflix data,  For column 'weekly_rank'
    'In the Netflix data, What is the highest weekly rank?',
    'In the Netflix data, What is the lowest weekly rank?',
    'In the Netflix data, What is the average weekly rank?',
    #In the Netflix data,  For column 'show_title'
    'In the Netflix data, What are the titles of the top 3 ranked shows?',
    'In the Netflix data, How many shows are listed?',
    'In the Netflix data, Does Leo appear in the dataset?',
    #In the Netflix data,  For column 'season_title'
    'In the Netflix data, Are there any non-null season titles?',
    'In the Netflix data, How many unique season titles are there?',
    'In the Netflix data, List all unique season titles.',
    #In the Netflix data,  For column 'weekly_hours_viewed'
    'In the Netflix data, What is the highest number of weekly hours viewed?',
    'In the Netflix data, What is the lowest number of weekly hours viewed?',
    'In the Netflix data, What is the total number of weekly hours viewed?',
    #In the Netflix data,  For column 'runtime'
    'In the Netflix data, What is the longest runtime?',
    'In the Netflix data, What is the shortest runtime?',
    'In the Netflix data, What is the average runtime?',
    #In the Netflix data,  For column 'weekly_views'
    'In the Netflix data, What is the highest number of weekly views?',
    'In the Netflix data, What is the lowest number of weekly views?',
    'In the Netflix data, What is the average number of weekly views?',
    #In the Netflix data,  For column 'cumulative_weeks_in_top_10'
    'In the Netflix data, What is the longest time a show has been in the top 10?',
    'In the Netflix data, What is the shortest time a show has been in the top 10?',
    'In the Netflix data, What is the average time shows have been in the top 10?',
    #In the Netflix data,  For column 'is_staggered_launch'
    'In the Netflix data, Are there any shows with a staggered launch?',
    'In the Netflix data, How many shows have a non-staggered launch?',
    'In the Netflix data, How many shows have a staggered launch?',
    #In the Netflix data,  For column 'episode_launch_details'
    'In the Netflix data, Do any shows have launch details?',
    'In the Netflix data, How many shows have launch details specified?',
    'In the Netflix data, List all the unique episode launch details.'
]

solutions = [
    # Answers for 'week'
    netflix['week'].min(),
    netflix['week'].max(),
    netflix['week'].nunique(),
    # Answers for 'category'
    netflix['category'].unique(),
    netflix[netflix['category'] == 'Films (English)'].shape[0],
    netflix['category'].nunique(),
    # Answers for 'weekly_rank'
    netflix['weekly_rank'].max(),
    netflix['weekly_rank'].min(),
    netflix['weekly_rank'].mean(),
    # Answers for 'show_title'
    netflix.sort_values(by='weekly_rank').head(3)['show_title'],
    netflix['show_title'].nunique(),
    'Leo' in netflix['show_title'].values,
    # Answers for 'season_title'
    netflix['season_title'].notnull().any(),
    netflix['season_title'].nunique(),
    netflix['season_title'].unique(),
    # Answers for 'weekly_hours_viewed'
    netflix['weekly_hours_viewed'].max(),
    netflix['weekly_hours_viewed'].min(),
    netflix['weekly_hours_viewed'].sum(),
    # Answers for 'runtime'
    netflix['runtime'].max(),
    netflix['runtime'].min(),
    netflix['runtime'].mean(),
    # Answers for 'weekly_views'
    netflix['weekly_views'].max(),
    netflix['weekly_views'].min(),
    netflix['weekly_views'].mean(),
    # Answers for 'cumulative_weeks_in_top_10'
    netflix['cumulative_weeks_in_top_10'].max(),
    netflix['cumulative_weeks_in_top_10'].min(),
    netflix['cumulative_weeks_in_top_10'].mean(),
    # Answers for 'is_staggered_launch'
    netflix['is_staggered_launch'].any(),
    netflix[netflix['is_staggered_launch'] == False].shape[0],
    netflix[netflix['is_staggered_launch'] == True].shape[0],
    # Answers for 'episode_launch_details'
    netflix['episode_launch_details'].notnull().any(),
    netflix['episode_launch_details'].notnull().sum(),
    netflix['episode_launch_details'].unique()
]

api_endpoint = 'http://localhost:8010/question'

stats = {
    'total_questions': len(questions),
    'correct_answers': 0,
    'incorrect_answers': 0,
    'response_times': []
}

for question, expected_solution in zip(questions, solutions):
    payload = {'question': question}
    start_time = time.time()
    response = requests.post(url=api_endpoint, json=payload)
    response_time = time.time() - start_time
    stats['response_times'].append(response_time)

    if response.status_code == 200 and 'query_result' in response.json():
        try: 
            answer = response.json()['query_result'][1][0][0]
        except IndexError:
            answer = response.json()['query_result']
        print(40* "#", "\n") 
        print(f'Question: {question}')
        print(f"Answer & Expected Solution: {answer}, {expected_solution}\n")
        try:
            if answer == expected_solution:
                stats['correct_answers'] += 1
            else:
                stats['incorrect_answers'] += 1
        except ValueError: pass
    else:
        print(f"Error for question '{question}': {response.text}")

average_response_time = sum(stats['response_times']) / len(stats['response_times'])
print(f"Total Questions: {stats['total_questions']}")
print(f"Correct Answers: {stats['correct_answers']}")
print(f"Incorrect Answers: {stats['incorrect_answers']}")
print(f"Average Response Time: {average_response_time:.4f} seconds")

if stats['correct_answers'] != stats['total_questions']:
    print("Not all questions were answered correctly, please review the responses.")