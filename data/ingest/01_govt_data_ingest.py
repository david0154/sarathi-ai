# data/ingest/01_govt_data_ingest.py
# Download and process Government of India datasets for Sarathi AI RAG

import os, requests, json, csv
from pathlib import Path

RAW = Path('data/raw')
RAW.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: str, label: str):
    """Download a file from URL to dest path."""
    try:
        print(f'Downloading {label}...')
        r = requests.get(url, timeout=30, headers={'User-Agent': 'SarathiAI/1.0 (research)'})
        r.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(r.content)
        print(f'  Saved: {dest} ({os.path.getsize(dest):,} bytes)')
        return True
    except Exception as e:
        print(f'  Failed: {label} — {e}')
        return False


def fetch_ogd_india(resource_id: str, dest: str, label: str, limit=1000):
    """Fetch dataset from data.gov.in OGD API."""
    url = f'https://api.data.gov.in/resource/{resource_id}?api-key=579b464db66ec23bdd000001cdd3946e44ce4aae38d975ea6dfed0b&format=json&limit={limit}'
    try:
        print(f'Fetching OGD: {label}...')
        r = requests.get(url, timeout=30)
        data = r.json()
        with open(dest, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'  Saved: {dest}')
    except Exception as e:
        print(f'  Failed: {label} — {e}')


if __name__ == '__main__':
    # 1. IPC PDF
    download_file(
        'https://legislative.gov.in/sites/default/files/A1860-45.pdf',
        str(RAW / 'ipc.pdf'),
        'Indian Penal Code PDF'
    )

    # 2. Bhagavad Gita text
    download_file(
        'https://www.gutenberg.org/files/54868/54868-0.txt',
        str(RAW / 'gita.txt'),
        'Bhagavad Gita (Gutenberg)'
    )

    # 3. India Tourism Statistics 2022 PDF
    download_file(
        'https://static.pib.gov.in/WriteReadData/userfiles/IndiaTourismStatistics2022English.pdf',
        str(RAW / 'india_tourism_stats_2022.pdf'),
        'India Tourism Statistics 2022'
    )

    # 4. MOSPI Dataset Compendium 2024
    download_file(
        'https://mospi.gov.in/sites/default/files/publication_reports/Compendium_of_Datasets_and_Registries_in_India_2024_0.pdf',
        str(RAW / 'mospi_compendium_2024.pdf'),
        'MOSPI Dataset Compendium 2024'
    )

    # 5. Wikipedia pages
    import wikipedia
    wikipedia.set_lang('en')
    pages = [
        'Kolkata', 'West Bengal', 'India', 'Tourism in India',
        'Kolkata tourism', 'Victoria Memorial Kolkata',
        'Howrah Bridge', 'Dakshineswar Temple',
        'Indian Penal Code', 'Constitution of India',
        'Bhagavad Gita', 'Hinduism', 'Islam in India',
        'Christianity in India', 'Heritage sites in India',
        'Archaeological Survey of India'
    ]
    wiki_texts = []
    for title in pages:
        try:
            content = wikipedia.page(title, auto_suggest=False).content
            wiki_texts.append(f'# {title}\n\n{content}')
            print(f'  Wikipedia: {title} ({len(content):,} chars)')
        except Exception as e:
            print(f'  Wikipedia failed: {title} — {e}')

    with open(str(RAW / 'wiki_india.txt'), 'w', encoding='utf-8') as f:
        f.write('\n\n---\n\n'.join(wiki_texts))
    print(f'  Saved wiki_india.txt ({len(wiki_texts)} pages)')

    print('\n✅ Government data download complete!')
