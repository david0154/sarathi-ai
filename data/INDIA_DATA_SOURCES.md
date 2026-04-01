# 🇮🇳 Sarathi AI — Complete India Data Sources

All data sources used to power Sarathi AI's knowledge base.
Organized by domain for RAG, fine-tuning, and structured DB layers.

---

## 1. 🏛️ Government & OGD (data.gov.in)

| Dataset | URL | Format |
|---|---|---|
| Open Government Data Platform India | https://data.gov.in | JSON/CSV/XML |
| India District List | https://data.gov.in/search?title=district | CSV |
| Census India 2011 | https://censusindia.gov.in/census.website/data/census-tables | CSV |
| Pin Code Directory | https://data.gov.in/catalog/all-india-pincode-directory | CSV |
| State-wise GDP Data | https://data.gov.in/search?title=gdp | CSV |
| Government Schemes | https://www.myscheme.gov.in | JSON |
| India Code (Laws) | https://www.indiacode.nic.in | PDF/HTML |
| IPC Full Text | https://legislative.gov.in/sites/default/files/A1860-45.pdf | PDF |
| Indian Constitution | https://legislative.gov.in/constitution-of-india | PDF |
| MOSPI Compendium 2024 | https://mospi.gov.in/sites/default/files/publication_reports/Compendium_of_Datasets_and_Registries_in_India_2024_0.pdf | PDF |

---

## 2. 🏨 Tourism, Hotels & Travel

| Dataset | URL | Format |
|---|---|---|
| Ministry of Tourism India | https://tourism.gov.in/market-research-and-statistics | PDF/Excel |
| India Tourism Statistics 2022 | https://static.pib.gov.in/WriteReadData/userfiles/IndiaTourismStatistics2022English.pdf | PDF |
| Ministry of Tourism Annual Reports | https://tourism.gov.in/media/annual-reports | PDF |
| Incredible India Official | https://www.incredibleindia.gov.in | HTML |
| West Bengal Tourism | https://www.wbtourism.gov.in | HTML |
| Beautiful Bengal | https://beautifulbengal.com | HTML |
| Kolkata Tourism Corp | https://www.kmda.org | HTML |
| Approved Hotels List | https://www.tourism.gov.in/classified-hotels | HTML/PDF |
| FHRAI Hotel Data | https://www.fhrai.com | HTML |
| Kolkata Approved Hotels Stats | https://www.indiastatdistrictlabour.com/westbengal/kolkata/tourism/approvedhotels | HTML |

---

## 3. 📍 Heritage, Monuments, Temples & Tourist Places

| Dataset | URL | Format |
|---|---|---|
| ASI (Archaeological Survey of India) | https://asi.nic.in/protected-monuments | HTML |
| UNESCO World Heritage India | https://whc.unesco.org/en/statesparties/in | HTML/JSON |
| National Museum India | https://nationalmuseum.gov.in | HTML |
| Open Beautify – India POI data | https://data.opendatasoft.com/explore/dataset/heritage-sites-in-india | GeoJSON |
| Wikidata India Places | https://www.wikidata.org/wiki/Q668 | JSON/SPARQL |
| OpenStreetMap India | https://download.geofabrik.de/asia/india.html | PBF/OSM |
| India GeoJSON States | https://github.com/geohacker/india | GeoJSON |

---

## 4. 🚆 Routes, Transport & Connectivity

| Dataset | URL | Format |
|---|---|---|
| Indian Railways Stations | https://data.gov.in/catalog/indian-railway-stations | CSV |
| Indian Railways Train Schedules | https://data.gov.in/catalog/indian-railway-train-schedule | CSV |
| National Highways | https://data.gov.in/catalog/national-highways | CSV |
| IRCTC (Rail API) | https://developers.irctc.co.in | REST API |
| Kolkata Metro Routes | https://www.kmrc.in/route-map.html | HTML |
| Kolkata Bus Routes (CSTC) | https://cstc.org.in | HTML |
| Airports India (AAI) | https://www.aai.aero/en/airports | HTML |
| KSRTC / State Bus | https://data.gov.in/search?title=bus | CSV |
| Google Maps API (Routes) | https://developers.google.com/maps | REST API |
| OpenRouteService (Free) | https://openrouteservice.org/dev/#/api-docs | REST API |

---

## 5. 🛕 Religion & Spiritual

| Dataset | URL | Format |
|---|---|---|
| Bhagavad Gita (Gutenberg) | https://www.gutenberg.org/files/54868/54868-0.txt | TXT |
| Quran English (Gutenberg) | https://www.gutenberg.org/ebooks/2800 | TXT |
| Bible KJV (Gutenberg) | https://www.gutenberg.org/ebooks/10 | TXT |
| Sacred Texts India | https://www.sacred-texts.com/hin | HTML |
| DSAL Digital South Asia | https://dsal.uchicago.edu | HTML |
| Ramayana (Gutenberg) | https://www.gutenberg.org/ebooks/24869 | TXT |

---

## 6. ⚖️ Law & Legal

| Dataset | URL | Format |
|---|---|---|
| India Code Portal (All Acts) | https://www.indiacode.nic.in | HTML/PDF |
| IPC 1860 | https://legislative.gov.in/sites/default/files/A1860-45.pdf | PDF |
| CrPC 1973 | https://legislative.gov.in | PDF |
| RTI Act 2005 | https://legislative.gov.in | PDF |
| Consumer Protection Act | https://legislative.gov.in | PDF |
| IT Act 2000 | https://legislative.gov.in | PDF |
| Supreme Court Judgments | https://main.sci.gov.in/judgments | HTML/PDF |
| High Court Records | https://ecourts.gov.in | HTML |

---

## 7. 🌐 Public Indian Web & Wikipedia

| Dataset | URL | Format |
|---|---|---|
| Wikipedia India (English) | https://en.wikipedia.org/wiki/India | API/HTML |
| Wikipedia Kolkata | https://en.wikipedia.org/wiki/Kolkata | API/HTML |
| Wikipedia West Bengal | https://en.wikipedia.org/wiki/West_Bengal | API/HTML |
| DBpedia India Data | https://dbpedia.org/page/India | RDF/SPARQL |
| CommonCrawl India subset | https://commoncrawl.org | WARC |
| IndicCorp V2 (AI4Bharat) | https://huggingface.co/datasets/ai4bharat/IndicCorpV2 | Parquet |
| Sangraha Dataset (AI4Bharat) | https://huggingface.co/datasets/ai4bharat/sangraha | Parquet |

---

## 8. 👥 Public Social & People Data (Publicly Available Only)

> ⚠️ IMPORTANT: Only publicly available, consent-compliant, privacy-safe data is used.
> No private profiles, no face data, no scraped personal data.
> All sources below are open datasets or public APIs with Terms of Service compliance.

| Dataset | URL | Format | Notes |
|---|---|---|---|
| Twitter/X Public API (India trends) | https://developer.twitter.com/en/docs | REST API | Rate-limited free tier, India-filtered |
| Reddit India Public Posts | https://www.reddit.com/r/india/.json | JSON | Public subreddit via API |
| Reddit Kolkata | https://www.reddit.com/r/kolkata/.json | JSON | Local public posts |
| Pushshift Reddit Archive | https://academictorrents.com/details/56aa49f9653ba545f48df2e33679f014d2829c10 | JSON | Historical public Reddit |
| GDELT India News | https://www.gdeltproject.org | CSV | Global news event data India |
| Common Crawl News (CC-News) | https://commoncrawl.org/the-data/get-started | WARC | Public news crawl |
| Indic Twitter Data (AI4Bharat) | https://huggingface.co/datasets/ai4bharat/indic-tweet | Parquet | Public tweets in Indian languages |
| Wikipedia People Born in India | https://en.wikipedia.org/w/api.php | API | Wikipedia open content |
| Wikidata Indian Public Figures | https://www.wikidata.org/wiki/Wikidata:WikiProject_India | SPARQL | Open structured data |
| IMDb India (Public Profiles) | https://www.imdb.com/india | HTML | Publicly listed actors/directors |
| LinkedIn Public Profiles (API) | https://developer.linkedin.com | REST API | Only public profiles via official API |

---

## 9. 🏙️ Kolkata-Specific Data

| Dataset | URL | Format |
|---|---|---|
| KMC (Kolkata Municipal Corp) | https://www.kmcgov.in | HTML |
| KMDA (Kolkata Metro Dev Auth) | https://www.kmda.org | HTML |
| West Bengal Pollution Board | https://wbpcb.gov.in | HTML |
| Kolkata Police (Public Info) | https://kolkatapolice.gov.in | HTML |
| Kolkata Port Authority | https://www.kolkataporttrust.gov.in | HTML |
| Kolkata Weather (IMD) | https://mausam.imd.gov.in | API/HTML |
| Air Quality Kolkata (CPCB) | https://cpcb.nic.in | API/HTML |
| WBTC Bus Routes Kolkata | https://www.wbtc.gov.in | HTML |

---

## ⚠️ Data Usage Policy

- All government data from data.gov.in / OGD is under National Data Sharing Policy (NDSP) — free to use.
- Wikipedia data is CC BY-SA licensed — attribution required.
- Gutenberg texts are public domain.
- Tourism PDFs are government publications — public use permitted.
- Social/public API data: always use official APIs, never scrape without ToS review.
- **No personal face data, private profiles, or biometric data is collected.**
- **No private social media data. Only public posts via official APIs.**
