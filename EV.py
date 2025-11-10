import itertools
import random

# Определим доступные карты
CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['c', 'd', 'h', 's']  # чирва, бубна, пика, трефа

# Генератор уникальных карточных комбинаций
def create_deck(exclude_cards=None):
    deck = []
    exclude_cards = exclude_cards or set()
    for rank in CARDS:
        for suit in SUITS:
            card = f"{rank}{suit}"
            if card not in exclude_cards:
                deck.append(card)
    return deck

def evaluate_winner(hole_cards1, hole_cards2, board):
    from pokereval.card import Card
    from pokereval.hand_evaluator import HandEvaluator

    # Конвертируем строки карт в бинарные представления
    cards1 = [Card.string_to_binary(card) for card in hole_cards1]
    cards2 = [Card.string_to_binary(card) for card in hole_cards2]
    community_cards = [Card.string_to_binary(card) for card in board]

    # Оцениваем силу рук
    score1 = HandEvaluator.evaluate_hand(cards1, community_cards)
    score2 = HandEvaluator.evaluate_hand(cards2, community_cards)

    if score1 < score2:
        return 1  # Победила первая рука
    elif score1 > score2:
        return 2  # Победила вторая рука
    else:
        return 0  # Ничья
    
    
# Расчет эквити через Монте-Карло симуляцию
def monte_carlo_equity(my_hole_cards, opponent_range, board, iterations=10000):
    wins = ties = losses = 0
    my_hole_set = set(my_hole_cards + board)
    deck = create_deck(my_hole_set)

    for _ in range(iterations):
        random.shuffle(deck)
        remaining_cards = deck[len(board):]
        opponent_hole_cards = random.sample(remaining_cards, 2)
        winner = evaluate_winner(my_hole_cards, opponent_hole_cards, board)
        if winner == 1:
            wins += 1
        elif winner == 0:
            ties += 1
        else:
            losses += 1

    equity = (wins + ties / 2) / iterations
    return equity

# Пример использования
my_hole_cards = ["Ac", "Ad"]  # мои карманные карты
opponent_range = None  # Предполагаемый диапазон рук соперника
board = []              # Текущие общие карты на столе
iterations = 1000       # Число итераций для точности
result = monte_carlo_equity(my_hole_cards, opponent_range, board, iterations)
print(f"Эквити моей руки: {result:.2%}")
