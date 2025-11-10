import random
from collections import defaultdict

ALL_HANDS = [
    'AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s',
    'A4s', 'A3s', 'A2s', 'KKo', 'QKo', 'JKo', 'TKo', '9Ko', '8Ko', '7Ko',
    '6Ko', '5Ko', '4Ko', '3Ko', '2Ko', 'QQ', 'JJo', 'TTo', '99', '88',
    '77', '66', '55', '44', '33', '22'
]

equity_table = {
    'AA': 0.85,     # Пара тузов ~ 85% эквити на префлопе
    'KK': 0.80,     # Пара королей ~ 80%
    'QQ': 0.75,     # Пара дам ~ 75%
    'AKs': 0.65,    # Тузы-короли одномастные ~ 65%
    'AQs': 0.60,    # Тузы-дамы одномастные ~ 60%
    'JJ': 0.65,     # Пара валетов ~ 65%
    'TT': 0.60,     # Пара десяток ~ 60%
    'AJs': 0.55,    # Тузы-валеты одномастные ~ 55%
}

def generate_random_hand():
    """Генерация случайной стартовой руки"""
    return random.choice(ALL_HANDS)

# Функция оценки вероятности победы руки на пре-флопе
def calculate_equity(hand):
    # Здесь используется таблица заранее просчитанных значений эквити
    return equity_table.get(hand, 0)

# Основные этапы расчета оптимального диапазона
def gto_range_calculation(num_players=6, stack_size=100):
    # Создаем словарь для хранения результатов симуляций
    results = defaultdict(int)
    
    for _ in range(10000):  # Количество итераций
        hand = generate_random_hand()  # Генерируем случайную руку
        
        # Рассчитываем ожидаемое значение выигрыша для этой руки
        expected_value = calculate_equity(hand)
        
        # Если рука приносит положительный EV, добавляем её в диапазон
        if expected_value > 0:
            results[hand] += 1
            
    # Преобразуем результаты в процентный диапазон
    total_hands = sum(results.values())
    optimal_range = {k: v / total_hands * 100 for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True)}