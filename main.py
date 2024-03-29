from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

def get_topic_titles(parsed_doc):
    title_selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = parsed_doc.find_all('p',{'class':title_selection_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

def get_topic_descs(parsed_doc):
    desc_selection_class = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = parsed_doc.find_all('p',{'class':desc_selection_class})
    topic_descs = []
    for desc in topic_desc_tags:
        topic_descs.append(desc.text.strip())
    return topic_descs

def get_topic_urls(parsed_doc):
    link_selection_class = 'no-underline flex-1 d-flex flex-column'
    topic_link_tags= parsed_doc.find_all('a',{'class':link_selection_class})
    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url+tag['href'])
    return topic_urls

def scrape_topics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topics_url))
    parsed_doc = BeautifulSoup(response.text, 'html.parser')
    topics_dict = {
    'title': get_topic_titles(parsed_doc),
    'description': get_topic_descs(parsed_doc),
    'url': get_topic_urls(parsed_doc)
    }

    return pd.DataFrame(topics_dict)

#Getting top 25 page
def get_topic_page(topic_url):
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def parse_star_count(stars):
    stars = stars.strip()
    if stars[-1] == 'k':
        return int(float(stars[:-1])*1000)
    return int(stars)

def get_repo_info(h1_tag, star_tag):
    # returns all the required info about a repository
    a_tags = h1_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    base_url = 'https://github.com'
    repo_url = base_url + (a_tags[1]['href'])
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, stars, repo_url

def get_topic_repos(topic_doc):
    repo_tags = topic_doc.find_all('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})
    star_tags = topic_doc.find_all('span', {'id':'repo-stars-counter-star'})

    topic_repos_dict = {'username': [], 'repo_name': [], 'stars': [], 'repo_url': []}

    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])

    return pd.DataFrame(topic_repos_dict)

def scrape_topic(topic_url, path):
    if os.path.exists(path):
        print(f'The file {path} already exists. Skipping...')
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path, index=None)        

def scrape_topics_repos():
    print('Scraping list of topics')
    topics_df =  scrape_topics()

    os.makedirs('data', exist_ok=True)
    for index, row in topics_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['title']))
        scrape_topic(row['url'], 'data/{}.csv'.format(row['title']))

    
if __name__ == "__main__":
    scrape_topics_repos()
