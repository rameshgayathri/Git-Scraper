# GitScraper

## Overview
This Python script allows you to scrape information about GitHub topics and their top repositories. It utilizes the BeautifulSoup library for web scraping and Pandas for data manipulation. The script fetches data from the GitHub Topics page and extracts details such as topic titles, descriptions, URLs, and the top repositories within each topic.

## Requirements
Make sure you have the following Python libraries installed:
- BeautifulSoup
- requests
- pandas

You can install them using:
```bash
pip install beautifulsoup4 requests pandas
```

## How to Use
1. Run the script `main.py`.
2. The script will fetch a list of GitHub topics, and for each topic, it will gather information about the top repositories.
3. The data will be saved in the `data` directory as CSV files.

## Functions

 `scrape_topics()`
- Fetches a list of GitHub topics along with their titles, descriptions, and URLs.

 `get_topic_page(topic_url)`
- Fetches the HTML content of a specific GitHub topic page.

 `get_repo_info(h1_tag, star_tag)`
- Extracts information about a GitHub repository from HTML tags, including username, repository name, stars, and repository URL.

 `get_topic_repos(topic_doc)`
- Retrieves information about the top repositories within a GitHub topic.

 `scrape_topic(topic_url, path)`
- Scrapes information about the top repositories for a specific GitHub topic and saves it as a CSV file.

`scrape_topics_repos()`
- Main function that orchestrates the entire scraping process.
- Creates a 'data' directory to store CSV files.
- Iterates through each GitHub topic, scrapes top repositories, and saves the data.

## File Structure
- `main.py`: Main script file.
- `data/`: Directory to store CSV files with scraped data.

## Usage
```bash
python main.py
```

## Note
- The script checks if the data directory exists and skips scraping for a topic if the CSV file already exists.

Feel free to customize the script according to your needs and make sure to adhere to GitHub's [Terms of Service](https://docs.github.com/en/github/site-policy/github-terms-of-service). Happy coding!
