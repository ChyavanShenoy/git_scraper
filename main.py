#! /usr/bin/env python3

import install_deps
import user_auth
from os import system, name
from logo import logo_art
import scraper

logged_in = False


def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def retry_login(username):
    login_success = True
    retry_count = 0
    while retry_count < 3:
        password = input('Password: ')
        login_success = user_auth.login(username, password)
        if login_success:
            logged_in = True
            print('Login successful!')
            user_auth.close()
            return
        else:
            retry_count += 1
            print('Incorrect username or password. Please try again.')
    user_auth.close()
    print('Too many failed login attempts. Exiting...')
    exit()


def main():
    print(logo_art)
    print('Welcome to the Scraper!')
    print('This program will scrape data from your GitHub profile, store it in a database, and then clone the repositories to your local machine as per your choice.')
    print('Please enter your GitHub username and password to continue.')
    git_username = input('Enter your GitHub username: ')
    if user_auth.check_user_exist(git_username):
        retry_login(username=git_username)
    else:
        print('Please enter your password to setup user on local machine.')
        user_auth.register(git_username, input('Enter your password: '))
        print('User setup successful!')
        print('Enter your password to login.')
        retry_login(username=git_username)
    while True:
        print('Enter your choice:')
        print('1. Scrape repo data from GitHub and update database.')
        print('2. Clone all repos from database to local machine.')
        print('3. Clone selected repos from database to local machine.')
        print('4. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            print('Scraping data...')
            scraper.scraper(git_username)
            print('Data scraped and stored successfully!')
        elif choice == '2':
            print('Enter the path to the directory where you want to clone the repos.')
            path = input('Enter path: ')
            scraper.clone_all_repos(git_username, path)
            print('Cloning successful!')
        elif choice == '3':
            print('Enter the path to the directory where you want to clone the repos.')
            path = input('Enter path: ')
            scraper.get_repo_names(git_username)
            print(
                'Enter the number next to the repos you want to clone separated by a space.')
            scraper.clone_selected_repos(
                git_username, path, input('Enter repo numbers: ').split())
            print('Cloning selected repos...')
            print('Cloning successful!')
        elif choice == '4':
            print('Exiting...')
            exit()


if __name__ == "__main__":
    install_deps.main()
    clear_screen()
    main()
    scraper.close()
