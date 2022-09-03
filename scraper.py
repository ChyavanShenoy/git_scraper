import sqlite3
import requests
import json
from git import Repo

# Connect to the database
conn = sqlite3.connect('data.db')

# Create a cursor
c = conn.cursor()
repo_list = []


def check_if_repo_in_db(repo_name):
    # check if repo name in user_repo table
    c.execute("SELECT * FROM user_repos WHERE repo_name=:rn", {
        'rn': repo_name})
    if c.fetchone() is not None:
        return True
    else:
        return False


def scraper(git_username):
    # Get the data from the website
    source = requests.get(
        F"https://api.github.com/users/{git_username}/repos", params={"per_page": 100})
    repos_json = (json.loads(source.content))
    # print(repos_json)
    for repo in repos_json:
        repo_name = repo['name'].replace("'", "")
        repo_url = repo['html_url'].replace("'", "")
        repo_description = repo['description']
        if repo_description is None:
            repo_description = "No data"
        # Check for repo in database
        if not check_if_repo_in_db(repo_name):
            c.execute("INSERT INTO user_repos VALUES (:un, :rn, :ru, :rd)", {
                'un': git_username, 'rn': repo_name, 'ru': repo_url, 'rd': repo_description})
            conn.commit()


def clone_all_repos(git_username, path):
    c.execute("SELECT * FROM user_repos WHERE username=:un", {
        'un': git_username})
    repos = c.fetchall()
    for repo in repos:
        repo_name = repo[1]
        repo_url = repo[2]
        print(F"Cloning {repo_name}...")
        Repo.clone_from(repo_url, F"{path}/{repo_name}")
        print(F"Cloned {repo_name}!")
        return


def get_repo_names(git_username):
    c.execute("SELECT * FROM user_repos")
    repos = c.fetchall()
    print('The following repos are available:')
    print('-----------------------------------')
    for repo in repos:
        repo_list.append(repo[1])
    for repo in repo_list:
        print(repo_list.index(repo) + 1, repo)


# get_repo_names('ChyavanShenoy')

def clone_selected_repos(git_username, path, repo_indexes):
    for index in repo_indexes:
        c.execute("SELECT * FROM user_repos WHERE repo_name=:rn AND username=:un", {
            'rn': repo_list[index - 1], 'un': git_username})
        repo = c.fetchone()
        repo_name = repo[1]
        repo_url = repo[2]
        print(F"Cloning {repo_name}...")
        Repo.clone_from(repo_url, F"{path}/{repo_name}")
        print(F"Cloned {repo_name}!")
        return


def close():
    conn.close()
