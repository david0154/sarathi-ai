# data/ingest/03_social_public_data_ingest.py
# Collect PUBLICLY AVAILABLE social and news data for Sarathi AI
#
# ⚠️ IMPORTANT PRIVACY NOTICE:
# - Only public posts via official APIs are collected
# - No private profiles, no face data, no biometric data
# - No scraping personal data without Terms of Service compliance
# - Follows PDPB (India Personal Data Protection Bill) guidelines

import json, os, requests, time
from pathlib import Path
from datetime import datetime

RAW = Path('data/raw/social')
RAW.mkdir(parents=True, exist_ok=True)


# 1. Reddit India public posts (no auth needed for public posts)
def fetch_reddit_india(subreddits=None, limit=100):
    """Fetch public posts from India-related subreddits via Reddit JSON API."""
    if subreddits is None:
        subreddits = ['india', 'kolkata', 'IndiaTech', 'indiatourism', 'IndianFood']
    headers = {'User-Agent': 'SarathiAI/1.0 (educational research)'}
    all_posts = []
    for sub in subreddits:
        url = f'https://www.reddit.com/r/{sub}/hot.json?limit={limit}'
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            posts = data.get('data', {}).get('children', [])
            for p in posts:
                post = p.get('data', {})
                all_posts.append({
                    'subreddit': sub,
                    'title': post.get('title', ''),
                    'text': post.get('selftext', '')[:500],
                    'score': post.get('score', 0),
                    'url': post.get('url', ''),
                    'created': datetime.fromtimestamp(post.get('created_utc', 0)).isoformat()
                })
            print(f'  Reddit r/{sub}: {len(posts)} posts')
            time.sleep(1)
        except Exception as e:
            print(f'  Reddit r/{sub} failed: {e}')
    with open(str(RAW / 'reddit_india_public.json'), 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(all_posts)} Reddit public posts')
    return all_posts


# 2. GDELT news events for India
def fetch_gdelt_india():
    """Fetch recent India news events from GDELT open dataset."""
    # GDELT provides open global news event data, no auth required
    url = 'https://api.gdeltproject.org/api/v2/doc/doc?query=India&mode=artlist&maxrecords=50&format=json'
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        articles = data.get('articles', [])
        with open(str(RAW / 'gdelt_india_news.json'), 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f'Saved {len(articles)} GDELT India news articles')
        return articles
    except Exception as e:
        print(f'GDELT failed: {e}')
        return []


# 3. Wikipedia public figures born in India
def fetch_wikipedia_indian_people():
    """Fetch list of notable Indian public figures from Wikipedia API."""
    import wikipedia
    people_pages = [
        'Mahatma Gandhi', 'Rabindranath Tagore', 'A.P.J. Abdul Kalam',
        'Jawaharlal Nehru', 'Subhas Chandra Bose', 'Swami Vivekananda',
        'Narendra Modi', 'Amartya Sen', 'Ratan Tata', 'Azim Premji'
    ]
    people_data = []
    for name in people_pages:
        try:
            page = wikipedia.page(name, auto_suggest=False)
            people_data.append({
                'name': name,
                'summary': wikipedia.summary(name, sentences=5),
                'url': page.url
            })
            print(f'  Wikipedia person: {name}')
            time.sleep(0.5)
        except Exception as e:
            print(f'  Failed: {name} — {e}')
    with open(str(RAW / 'notable_indians_wikipedia.json'), 'w', encoding='utf-8') as f:
        json.dump(people_data, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(people_data)} notable Indian public figures')
    return people_data


# 4. AI4Bharat public Indian language data (HuggingFace)
def fetch_ai4bharat_samples():
    """Load sample of AI4Bharat public Indian language corpus."""
    try:
        from datasets import load_dataset
        # Bengali corpus
        print('Loading AI4Bharat IndicCorp Bengali sample...')
        ds = load_dataset('ai4bharat/IndicCorpV2', 'indiccorp_v2',
                          data_dir='data/ben_Beng', split='train', streaming=True)
        samples = []
        for i, item in enumerate(ds):
            if i >= 500:
                break
            samples.append(item)
        with open(str(RAW / 'ai4bharat_bengali_samples.json'), 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        print(f'Saved {len(samples)} AI4Bharat Bengali samples')
    except Exception as e:
        print(f'AI4Bharat load failed: {e}')


if __name__ == '__main__':
    print('\n📡 Collecting public social and news data for Sarathi AI...')
    print('(Only publicly available, ToS-compliant data)\n')
    fetch_reddit_india()
    fetch_gdelt_india()
    fetch_wikipedia_indian_people()
    fetch_ai4bharat_samples()
    print('\n✅ Public social data collection complete!')
