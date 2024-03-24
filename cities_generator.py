import random

# Функция для генерации случайных координат и веса груза
def generate_random_city():
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    weight = random.randint(1, 10)
    return x, y, weight

# Функция для записи городов в файл
def write_cities_to_file(file_path, num_cities):
    with open(file_path, 'w') as file:
        for _ in range(num_cities):
            x, y, weight = generate_random_city()
            file.write(f"{x} {y} {weight}\n")

# Генерация и запись 30 случайных городов в файл
write_cities_to_file('cities_small.txt', 8)