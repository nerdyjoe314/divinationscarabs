import json
from pathlib import Path

# Union Weight as fallback
DEFAULT_WEIGHT = 4987
PRICE_FLOOR = 6

cardData = './data/cards.json'
cardPriceOverrides = './data/overrides.json'

def prepare_card_data():
    global DEFAULT_WEIGHT, PRICE_FLOOR, cardData, cardPriceOverrides
    
    with open(cardData, 'r') as file:
        allCards = json.load(file)
    with open(cardPriceOverrides, 'r') as file:
        cardPriceOverrides = json.load(file)

    clean_card_data = []

    for card in allCards:
        override = next((o for o in cardPriceOverrides if o['cardName'] == card['name']), None)

        if card.get('reward') == 'Disabled':
            continue

        if override:
            card['price'] = override['cardValue']
        elif card['price'] < PRICE_FLOOR:
            card['price'] = 0

        if 'drop' not in card:
            continue
        elif 'max_level' not in card['drop']:
            card['drop']['max_level'] = 100

        card.setdefault('weight', DEFAULT_WEIGHT)

        clean_card_data.append(card)

    with open("prices.json", "w") as file:
        json.dump(clean_card_data, file)
