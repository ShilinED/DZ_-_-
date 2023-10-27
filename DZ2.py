import random # Импортируем модуль для генерации случайных чисел.

class Ship:# Описание класса корабля.
    def __init__(self, x, y, length=1, vertical=False):# Конструктор корабля, который принимает начальные координаты и длину корабля.
        if vertical:
            # Список позиций, которые занимает корабль на поле.
            self.positions = [(x, y+i) for i in range(length)]
        else:
            self.positions = [(x+i, y) for i in range(length)]
        self.hits = []

    def is_hit(self, x, y): # Метод, который проверяет, попали ли по кораблю.
        if (x, y) in self.positions and (x, y) not in self.hits:
            self.hits.append((x, y))
            return True
        return False

    def is_sunk(self):     # Метод, который проверяет, уничтожен ли корабль полностью.
        return set(self.hits) == set(self.positions)
# Описание класса игрового поля.
class Board:
    def __init__(self, size):# Конструктор игрового поля, который принимает размер поля.
        self.size = size
        self.field = [['О' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def add_ship(self, ship):  #добавление в поле корабля
        self.ships.append(ship)
        for (x, y) in ship.positions:
            self.field[y][x] = '■'

    def is_valid_ship_position(self, ship):    # Метод, который проверяет, может ли корабль быть размещен на поле в заданной позиции.
        for (x, y) in ship.positions:
            if x < 0 or y < 0 or x >= self.size or y >= self.size or self.field[y][x] == '■':
                return False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x+dx < self.size and 0 <= y+dy < self.size and self.field[y+dy][x+dx] == '■':
                        return False
        return True

    def attack(self, x, y):# Метод для атаки на заданные координаты.
        if self.field[y][x] == 'X' or self.field[y][x] == 'T':
            return None

        for ship in self.ships:
            if ship.is_hit(x, y):
                self.field[y][x] = 'X'
                if ship.is_sunk():
                    self.mark_surrounding_cells_sunk(ship)
                return True

        self.field[y][x] = 'T'
        return False

    def mark_surrounding_cells_sunk(self, ship):# Метод для отметки клеток вокруг уничтоженного корабля.
        for (x, y) in ship.positions:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.field[ny][nx] != 'X':
                        self.field[ny][nx] = 'T'

    def all_ships_sunk(self): # Метод, который проверяет, уничтожены ли все корабли на поле.
        return all(ship.is_sunk() for ship in self.ships)

    def __str__(self):# Метод для вывода поля в консоль.
        res = " | " + " | ".join(map(str, [i+1 for i in range(self.size)])) + "|\n"
        res += "-" * (4 * self.size + 3) + "\n"
        for i in range(self.size):
            res += f"{i + 1}| " + " | ".join(self.field[i]) + "|\n"
        return res

def play():# Основная функция игры.
    size = 6
    player_board = Board(size)
    computer_board = Board(size)


    def add_ships_to_board(board, lengths): # Добавляем карабли для ПК и меня
        for length in lengths:
            while True:
                vertical = random.choice([True, False])
                if vertical:
                    x, y = random.randint(0, size - 1), random.randint(0, size - 1 - length + 1)
                else:
                    x, y = random.randint(0, size - 1 - length + 1), random.randint(0, size - 1)
                ship = Ship(x, y, length, vertical)
                if board.is_valid_ship_position(ship):
                    board.add_ship(ship)
                    break

    ship_lengths = [3, 2, 2, 1, 1, 1, 1]
    add_ships_to_board(player_board, ship_lengths)
    add_ships_to_board(computer_board, ship_lengths)

    while not computer_board.all_ships_sunk() and not player_board.all_ships_sunk():  # Главный игровой цикл.
        print("Моя доска:")
        print(player_board)
        print("\nДоска компьютера:")
        print(" | " + " | ".join(map(str, [i + 1 for i in range(size)])) + " |")
        print("-" * (4 * size + 3))
        masked_computer_board = [['■' if cell == '■' else cell for cell in row] for row in computer_board.field]
        for i, row in enumerate(masked_computer_board):
            print(f"{i + 1}| " + " | ".join(row) + " |")
        print("\n")

        # Мой ход
        while True:
            try:
                x, y = map(int, input("Введите свой ход (формат x y):").split())
                if 1 <= x <= size and 1 <= y <= size:
                    result = computer_board.attack(x-1, y-1)
                    if result:
                        print("Вы подбили корабль!")
                    elif result is not None:
                        print("Ты промахнулся!")
                    else:
                        print("Вы уже стреляли в эту клетку!")
                    break
            except ValueError:
                print(f"Неверный ввод. Введите значения от 1 до {size}.")

        # Ход компьютера.
        while True:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            result = player_board.attack(x, y)
            if result is not None:
                if result:
                    print("Компьютер поразил ваш корабль!")
                else:
                    print("Компьютер промахнулся!")
                break

    # Объявляем победителя.
    if computer_board.all_ships_sunk():
        print("Ты победил!")
    else:
        print("Компьютер победил")

if __name__ == "__main__":
    play()
