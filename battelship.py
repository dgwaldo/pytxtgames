
from random import randint

class ShotFiredReport:
    is_hit: bool
    was_guessed: bool

    def __init__(self, hit: int):
        self.is_hit = hit
        self.was_guessed = True

class Ship:
    size: int
    name: str
    positions: list
    hit_cnt: int

    def __init__(self, size: int, name: str):
        self.size = size
        self.name = name
        self.positions = []
        self.hit_cnt = 0

    @property
    def is_sunk(self):
        return self.hit_cnt >= self.size

    def check_for_hit_damage(self, shell_hit) -> bool:
        hit = any(p == shell_hit for p in self.positions)
        if(hit):
            self.hit_cnt += 1
            return True
        return False
    
    def printPosition(self):
        print(self.positions)

class Board:

    # 10 Rows
    rowDefs: list
    # A-I Cols
    colDefs: list
    # Board Position Dictionary
    cells: dict

    def __init__(self):
        self.colDefs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        self.rowDefs = [i for i in range(1, 11)]
        self.cells = {}
        self.__generate_board_matrix()

    def updateCell(self, cellAddress: str, cellInfo: dict):
        self.cells[cellAddress] = cellInfo

    def positionShips(self, ships: list[Ship]):
        all_ships_placed = False
        while not all_ships_placed:
            ship = next(s for s in ships if not s.positions)
            seed_pos = self.__generate_random_position()
            if(10 - seed_pos[0] > ship.size):  # Should fit in the row
                self.__set_ship_positions_by_row(ship, seed_pos[0])
            elif(10 - seed_pos[1] > ship.size):  # Should fit in the column
                self.__set_ship_positions_by_col(ship, seed_pos[1])
            
            has_overlapping_placement = any(bool(set(ship.positions) & set(s.positions)) for s in ships if s.name != ship.name)

            if(has_overlapping_placement):
                ship.positions = []

            all_ships_placed = all(len(s.positions) == s.size for s in ships)

    def generate_board_position(self) -> list[int]:
        col_pos = randint(0, 9)
        row_pos = randint(0, 9)
        return f'{self.colDefs[col_pos]}{self.rowDefs[row_pos]}'

    def print_board(self, title:str):
        print(f'\t   -------     {title}     -------')
        col_prt_str = str(self.colDefs).replace('[', '  ').replace(']', '')
        print(f' \t{col_prt_str}')
        for i in range (1, 11): ## Run down the column printing each row
            row = i
            row_cols = [f'{self.colDefs[i-1]}{row}' for i in range(1,11)]
            row_arr =['x' if (self.cells[pos] and self.cells[pos].is_hit) else 'o' for pos in row_cols]
            print(f'{i}\t {row_arr}')
        print()

    def __generate_random_position(self) -> list[int]:
        col_pos = randint(0, 9)
        row_pos = randint(0, 9)
        return [col_pos, row_pos]

    def __set_ship_positions_by_row(self, ship, start_idx):
        for col in range(start_idx, start_idx + ship.size):
            cell = self.__get_cell_pos_from_col_row(col, start_idx)
            ship.positions.append(cell)

    def __set_ship_positions_by_col(self, ship, start_idx):
        for row in range(start_idx, start_idx + ship.size):
            cell = self.__get_cell_pos_from_col_row(start_idx, row)
            ship.positions.append(cell)

    def __get_cell_pos_from_col_row(self, col: int, row: int,) -> str:
        return f'{self.colDefs[col]}{self.rowDefs[row]}'

    def __generate_board_matrix(self):
        for r in self.rowDefs:
            for c in self.colDefs:
                self.cells[f'{c}{r}'] = {}

class BattleShipConsole:
    ships: list
    board: Board

    def __init__(self):
        self.board = Board()
        self.ships = [
            Ship(size=5, name="Aircraft Carrier"),
            Ship(size=4, name="Battleship"),
            Ship(size=3, name="Cruiser"),
            Ship(size=3, name="Submarine"),
            Ship(size=2, name="Destroyer"),
        ]

class BattleShipGameEngine:

    p1: BattleShipConsole
    p2: BattleShipConsole

    def __init__(self):
        self.p1 = BattleShipConsole()
        self.p2 = BattleShipConsole()

    def play(self):
        p1_win = False
        p2_win = False
        # Position both players ships
        self.p1.board.positionShips(self.p1.ships)
        self.p2.board.positionShips(self.p2.ships)

        while not p1_win or p2_win:
            # Human Player Interaction
            p1_target = input("Target enemy ship postion: ")
            self.target_enemy_ships(self.p2, str(p1_target).lower())

            #Computer Randomly Firing
            p2_target = self.p2.board.generate_board_position()
            self.target_enemy_ships(self.p1, p2_target, is_computer=True)

            # Print Human Players Hits against Computer
            self.p2.board.print_board('Enemy Ship Damage')

             # Print Computer Hits against Human Player
            self.p1.board.print_board('Your Damage')

            # Check for Exit Condition
            p1_win = all(s.is_sunk for s in self.p2.ships)
            p2_win = all(s.is_sunk for s in self.p1.ships)

        if(p1_win):
            print("Congratulations the battle has been won the enemy fleet is destroyed!")

        if(p2_win):
            print("A computer beat you. Sad!")

    def target_enemy_ships(self, enemy: BattleShipConsole(),  target, is_computer : bool = False):
        was_hit = any(hit for hit in [s.check_for_hit_damage(target) for s in enemy.ships])
        enemy.board.updateCell(target, ShotFiredReport(hit=was_hit))
        if(is_computer):
            print(f"The enemy fired back, your ship at {target} has been hit") if was_hit else print("Enemy fire lands in the ocean with a splash")
        else:
            print("Enemy ship hit") if was_hit else print("Your fire misses the enemy ships, whales beware.")

new_game = BattleShipGameEngine()

new_game.play()
