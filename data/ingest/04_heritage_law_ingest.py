# data/ingest/04_heritage_law_ingest.py
# Download heritage, law, and spiritual data for Sarathi AI RAG

import requests, os, json, time
from pathlib import Path

RAW = Path('data/raw')
RAW.mkdir(parents=True, exist_ok=True)


def download_gutenberg(book_id: int, dest: str, label: str):
    """Download a Project Gutenberg text file."""
    url = f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt'
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(dest, 'w', encoding='utf-8', errors='replace') as f:
            f.write(r.text)
        print(f'  Saved: {label} ({len(r.text):,} chars)')
    except Exception as e:
        print(f'  Failed: {label} — {e}')


if __name__ == '__main__':
    print('Downloading heritage and spiritual texts...')

    # Bhagavad Gita
    download_gutenberg(54868, str(RAW / 'gita.txt'), 'Bhagavad Gita')
    time.sleep(1)

    # Ramayana
    download_gutenberg(24869, str(RAW / 'ramayana.txt'), 'Ramayana (Griffith)')
    time.sleep(1)

    # Quran (English)
    download_gutenberg(2800, str(RAW / 'quran_english.txt'), 'Quran (English Translation)')
    time.sleep(1)

    # Bible KJV
    download_gutenberg(10, str(RAW / 'bible_kjv.txt'), 'Bible KJV')
    time.sleep(1)

    # Wikipedia religious + heritage pages
    import wikipedia
    pages = [
        'Hinduism', 'Islam in India', 'Christianity in India',
        'Sikhism', 'Buddhism in India', 'Jainism',
        'Archaeological Survey of India',
        'UNESCO World Heritage Sites in India',
        'List of heritage sites in Kolkata',
        'List of national parks of India'
    ]
    texts = []
    for title in pages:
        try:
            content = wikipedia.page(title, auto_suggest=False).content
            texts.append(f'# {title}\n\n{content}')
            print(f'  Wikipedia: {title}')
            time.sleep(0.5)
        except Exception as e:
            print(f'  Failed: {title} — {e}')

    with open(str(RAW / 'heritage_religion_wiki.txt'), 'w', encoding='utf-8') as f:
        f.write('\n\n---\n\n'.join(texts))
    print(f'Saved heritage_religion_wiki.txt ({len(texts)} pages)')

    # Indian Law Acts (India Code)
    law_pages = [
        'Indian Penal Code', 'Code of Criminal Procedure (India)',
        'Constitution of India', 'Right to Information Act',
        'Information Technology Act 2000 (India)',
        'Consumer Protection Act 2019'
    ]
    law_texts = []
    for title in law_pages:
        try:
            content = wikipedia.page(title, auto_suggest=False).content
            law_texts.append(f'# {title}\n\n{content}')
            print(f'  Wikipedia law: {title}')
            time.sleep(0.5)
        except Exception as e:
            print(f'  Failed: {title} — {e}')

    with open(str(RAW / 'indian_law_wiki.txt'), 'w', encoding='utf-8') as f:
        f.write('\n\n---\n\n'.join(law_texts))
    print(f'Saved indian_law_wiki.txt ({len(law_texts)} pages)')

    print('\n✅ Heritage and law data download complete!')
