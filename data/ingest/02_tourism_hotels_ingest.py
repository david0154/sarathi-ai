# data/ingest/02_tourism_hotels_ingest.py
# Collect hotel, tourism, and travel data for Sarathi AI

import json, os, requests
from pathlib import Path

RAW = Path('data/raw')
RAW.mkdir(parents=True, exist_ok=True)


# --- Static curated Kolkata Hotels dataset (official classified hotels) ---
KOLKATA_HOTELS = [
    {'name': 'The Oberoi Grand', 'category': '5-star', 'address': '15 Jawaharlal Nehru Road, Kolkata', 'lat': 22.5574, 'lng': 88.3506, 'price_range': '₹10000-₹25000', 'phone': '+91 33 2249 2323', 'source': 'Ministry of Tourism classified'},
    {'name': 'ITC Royal Bengal', 'category': '5-star', 'address': 'Plot No 1, JBS Haldane Avenue, Kolkata', 'lat': 22.5175, 'lng': 88.3637, 'price_range': '₹9000-₹20000', 'phone': '+91 33 4455 8000', 'source': 'Ministry of Tourism classified'},
    {'name': 'Taj Bengal', 'category': '5-star', 'address': '34B Belvedere Road, Alipore, Kolkata', 'lat': 22.5373, 'lng': 88.3334, 'price_range': '₹8000-₹18000', 'phone': '+91 33 6612 3939', 'source': 'Ministry of Tourism classified'},
    {'name': 'Hyatt Regency Kolkata', 'category': '5-star', 'address': 'JA-1 Sector III, Salt Lake, Kolkata', 'lat': 22.5758, 'lng': 88.4177, 'price_range': '₹7000-₹15000', 'phone': '+91 33 2335 1234', 'source': 'Ministry of Tourism classified'},
    {'name': 'The LaLiT Great Eastern Kolkata', 'category': '5-star', 'address': '1-3 Old Court House Street, Kolkata', 'lat': 22.5637, 'lng': 88.3498, 'price_range': '₹6000-₹14000', 'phone': '+91 33 4444 7777', 'source': 'Ministry of Tourism classified'},
    {'name': 'Hotel Hindustan International', 'category': '4-star', 'address': '235/1 AJC Bose Road, Kolkata', 'lat': 22.5473, 'lng': 88.3597, 'price_range': '₹3500-₹8000', 'phone': '+91 33 2223 4394', 'source': 'Ministry of Tourism classified'},
    {'name': 'Novotel Kolkata Hotel and Residences', 'category': '4-star', 'address': 'CB 218 A, New Town, Kolkata', 'lat': 22.5804, 'lng': 88.4636, 'price_range': '₹4000-₹9000', 'phone': '+91 33 6626 7777', 'source': 'Ministry of Tourism classified'},
    {'name': 'Swissotel Kolkata', 'category': '4-star', 'address': 'New Town Action Area II, Kolkata', 'lat': 22.5733, 'lng': 88.4654, 'price_range': '₹5000-₹11000', 'phone': '+91 33 6650 0000', 'source': 'Ministry of Tourism classified'},
    {'name': 'Lytton Hotel', 'category': '3-star', 'address': '14 Sudder Street, Kolkata', 'lat': 22.5518, 'lng': 88.3539, 'price_range': '₹1800-₹4000', 'phone': '+91 33 2249 1872', 'source': 'Ministry of Tourism classified'},
    {'name': 'Broadway Hotel', 'category': '2-star', 'address': '27A Ganesh Chandra Avenue, Kolkata', 'lat': 22.5699, 'lng': 88.3529, 'price_range': '₹800-₹2000', 'phone': '+91 33 2236 5930', 'source': 'Official hotel listing'},
    {'name': 'Hotel Centrum', 'category': '2-star', 'address': '21A Marquis Street, Kolkata', 'lat': 22.5559, 'lng': 88.3545, 'price_range': '₹900-₹2200', 'phone': '+91 33 2252 0820', 'source': 'Official hotel listing'},
    {'name': 'Floatel Kolkata', 'category': '3-star', 'address': 'Millennium Park, Strand Road, Kolkata', 'lat': 22.5643, 'lng': 88.3382, 'price_range': '₹3000-₹6000', 'phone': '+91 33 2248 0001', 'source': 'West Bengal Tourism'},
]

with open(str(RAW / 'kolkata_hotels.json'), 'w', encoding='utf-8') as f:
    json.dump(KOLKATA_HOTELS, f, ensure_ascii=False, indent=2)
print(f'Saved {len(KOLKATA_HOTELS)} Kolkata hotels')


# --- Tourist Places ---
TOURIST_PLACES = [
    # Kolkata
    {'name': 'Victoria Memorial', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Heritage Monument', 'lat': 22.5448, 'lng': 88.3426, 'entry_fee': '₹30 Indians, ₹500 foreigners', 'timing': '10:00 AM - 5:00 PM (closed Monday)', 'source': 'ASI official'},
    {'name': 'Howrah Bridge (Rabindra Setu)', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Landmark', 'lat': 22.5851, 'lng': 88.3468, 'entry_fee': 'Free', 'timing': '24 hours', 'source': 'KMC official'},
    {'name': 'Dakshineswar Temple', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Temple', 'lat': 22.6551, 'lng': 88.3578, 'entry_fee': 'Free', 'timing': '6:00 AM - 12:30 PM, 3:00 PM - 8:30 PM', 'source': 'West Bengal Tourism'},
    {'name': 'Kalighat Temple', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Temple', 'lat': 22.5199, 'lng': 88.3432, 'entry_fee': 'Free', 'timing': '5:00 AM - 10:00 PM', 'source': 'West Bengal Tourism'},
    {'name': 'Indian Museum', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Museum', 'lat': 22.5579, 'lng': 88.3518, 'entry_fee': '₹20 Indians, ₹500 foreigners', 'timing': '10:00 AM - 5:00 PM (closed Monday)', 'source': 'Indian Museum official'},
    {'name': 'Birla Planetarium', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Science/Education', 'lat': 22.5495, 'lng': 88.3513, 'entry_fee': '₹60-₹80', 'timing': '12:00 PM - 7:00 PM', 'source': 'Official'},
    {'name': 'College Street (Boi Para)', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Cultural/Shopping', 'lat': 22.5757, 'lng': 88.3636, 'entry_fee': 'Free', 'timing': '9:00 AM - 8:00 PM', 'source': 'West Bengal Tourism'},
    {'name': 'Park Street', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Food/Nightlife', 'lat': 22.5518, 'lng': 88.3541, 'entry_fee': 'Free', 'timing': 'All day', 'source': 'KMC official'},
    {'name': 'Sundarbans National Park', 'city': 'South 24 Parganas', 'state': 'West Bengal', 'category': 'Nature/Wildlife', 'lat': 21.9497, 'lng': 88.8978, 'entry_fee': '₹60 Indians, ₹1500 foreigners', 'timing': 'October to March best season', 'source': 'West Bengal Forest Dept'},
    {'name': 'Marble Palace', 'city': 'Kolkata', 'state': 'West Bengal', 'category': 'Heritage Mansion', 'lat': 22.5873, 'lng': 88.3563, 'entry_fee': 'Free (permission needed)', 'timing': '10:00 AM - 4:00 PM (closed Mon/Thu)', 'source': 'West Bengal Tourism'},
    # India Major
    {'name': 'Taj Mahal', 'city': 'Agra', 'state': 'Uttar Pradesh', 'category': 'UNESCO World Heritage', 'lat': 27.1751, 'lng': 78.0421, 'entry_fee': '₹50 Indians, ₹1100 foreigners', 'timing': 'Sunrise to Sunset (closed Friday)', 'source': 'ASI official'},
    {'name': 'Red Fort', 'city': 'Delhi', 'state': 'Delhi', 'category': 'UNESCO World Heritage', 'lat': 28.6562, 'lng': 77.2410, 'entry_fee': '₹35 Indians, ₹500 foreigners', 'timing': '9:30 AM - 4:30 PM (closed Monday)', 'source': 'ASI official'},
    {'name': 'Jaipur City Palace', 'city': 'Jaipur', 'state': 'Rajasthan', 'category': 'Heritage Palace', 'lat': 26.9258, 'lng': 75.8237, 'entry_fee': '₹200 Indians, ₹700 foreigners', 'timing': '9:30 AM - 5:00 PM', 'source': 'Rajasthan Tourism'},
    {'name': 'Gateway of India', 'city': 'Mumbai', 'state': 'Maharashtra', 'category': 'Landmark', 'lat': 18.9220, 'lng': 72.8347, 'entry_fee': 'Free', 'timing': '24 hours', 'source': 'Maharashtra Tourism'},
    {'name': 'Golden Temple', 'city': 'Amritsar', 'state': 'Punjab', 'category': 'Religious Site', 'lat': 31.6200, 'lng': 74.8765, 'entry_fee': 'Free', 'timing': '4:00 AM - 11:00 PM', 'source': 'SGPC official'},
]

with open(str(RAW / 'tourist_places.json'), 'w', encoding='utf-8') as f:
    json.dump(TOURIST_PLACES, f, ensure_ascii=False, indent=2)
print(f'Saved {len(TOURIST_PLACES)} tourist places')


# --- Transport routes (Kolkata) ---
KOLKATA_ROUTES = [
    {'from': 'Kolkata Airport (NSCBI)', 'to': 'City Centre (Park Street)', 'mode': 'Metro', 'duration': '45 min', 'cost': '₹30', 'notes': 'Airport Metro Line to Noapara, change to Blue Line'},
    {'from': 'Kolkata Airport (NSCBI)', 'to': 'City Centre (Park Street)', 'mode': 'Taxi (Ola/Uber)', 'duration': '40-60 min', 'cost': '₹500-₹700', 'notes': 'Varies by traffic'},
    {'from': 'Howrah Station', 'to': 'Park Street', 'mode': 'Metro (Blue Line)', 'duration': '20 min', 'cost': '₹10', 'notes': 'Howrah Metro to Park Street station'},
    {'from': 'Kolkata', 'to': 'Sundarbans', 'mode': 'Train + Boat', 'duration': '3-4 hours', 'cost': '₹200-₹500', 'notes': 'Train to Canning then boat; book via WBTDC'},
    {'from': 'Kolkata', 'to': 'Darjeeling', 'mode': 'Train (NJP) + Toy Train', 'duration': '9-10 hours', 'cost': '₹300-₹1500', 'notes': 'Train to NJP, then toy train or taxi to Darjeeling'},
    {'from': 'Sealdah Station', 'to': 'Dakshineswar', 'mode': 'Train', 'duration': '40 min', 'cost': '₹5-₹10', 'notes': 'Circular Railway from Sealdah to Dakshineswar'},
]

with open(str(RAW / 'kolkata_routes.json'), 'w', encoding='utf-8') as f:
    json.dump(KOLKATA_ROUTES, f, ensure_ascii=False, indent=2)
print(f'Saved {len(KOLKATA_ROUTES)} Kolkata routes')

print('\n✅ Tourism and hotel data saved!')
