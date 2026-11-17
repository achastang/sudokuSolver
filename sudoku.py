import copy
import time

class SudokuBoard:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solved_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.options = {}
        self.counts = {}
        for i in range(1, 10):
            self.counts[i] = 0

    def fill(self, nums):
        for i in range(81):
            num = int(nums[i])
            row = i // 9
            col = i % 9
            self.grid[row][col] = num
            self.solved_grid[row][col] = num
            if num != 0:
                self.counts[num] += 1
        
        self.fill_options()

    def fill_options(self):
        self.options = {}
        start = time.time()
        for i in range(9):
            for j in range(9):
                if self.solved_grid[i][j] == 0:
                    self.options[(i, j)] = self.get_options(i, j)
        end = time.time()
        total_time = (end - start) * 1000
        print(f"Time taken to fill in options: {total_time} ms")

    def update_options(self, row, col, num):
        for j in range(9):
            if (row, j) in self.options and num in self.options[(row, j)]:
                self.options[(row, j)].remove(num)
                if len(self.options[(row, j)]) == 0:
                    self.options.pop((row, j))

        for i in range(9):
            if (i, col) in self.options and num in self.options[(i, col)]:
                self.options[(i, col)].remove(num)
                if len(self.options[(i, col)]) == 0:
                    self.options.pop((i, col))

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i, j) in self.options and num in self.options[(i, j)]:
                    self.options[(i, j)].remove(num)
                    if len(self.options[(i, j)]) == 0:
                        self.options.pop((i, j))

    def get_options(self, row, col):
        not_allowed = set()
        for i in range(9):
            if self.solved_grid[row][i] != 0:
                not_allowed.add(self.solved_grid[row][i])
        
        for j in range(9):
            if self.solved_grid[j][col] != 0:
                not_allowed.add(self.solved_grid[j][col])

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                not_allowed.add(self.solved_grid[i][j])

        options_list = []
        for i in range(1,10):
            if i not in not_allowed:
                options_list.append(i)

        return options_list

    def is_solvable(self):
        for option in self.options.values():
            if len(option) == 0:
                return False

        for i in range(9):
            seen = set()
            for j in range(9):
                num = self.solved_grid[i][j]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)

        for j in range(9):
            seen = set()
            for i in range(9):
                num = self.solved_grid[i][j]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = set()
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        num = self.solved_grid[i][j]
                        if num != 0:
                            if num in seen:
                                return False
                            seen.add(num)

        return True
    
    def is_solved(self):
        for num in range(1, 10):
            if self.counts[num] != 9:
                return False
            
        for i in range(9):
            seen = set()
            for j in range(9):
                num = self.solved_grid[i][j]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
            if len(seen) != 9:
                return False

        for j in range(9):
            seen = set()
            for i in range(9):
                num = self.solved_grid[i][j]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
            if len(seen) != 9:
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = set()
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        num = self.solved_grid[i][j]
                        if num != 0:
                            if num in seen:
                                return False
                            seen.add(num)
                if len(seen) != 9:
                    return False

        return True
    
    def solve(self):
        while not self.is_solved():
            updated = False
            for (i, j), option in list(self.options.items()):
                if len(option) == 1:
                    self.solved_grid[i][j] = option[0]
                    self.counts[option[0]] += 1
                    self.options.pop((i, j))
                    self.update_options(i, j, option[0])
                    updated = True

            if not updated:
                if self.hidden_single():
                    updated = True

            if not updated:
                self.backtrack()

    def hidden_single(self):
        made_changes = False
        updates = {}

        for row in range(9):
            positions = {num: [] for num in range(1, 10)}
            for col in range(9):
                if (row, col) in self.options:
                    for num in self.options[(row, col)]:
                        positions[num].append((row, col))
            for num, cells in positions.items():
                if len(cells) == 1:
                    i, j = cells[0]
                    if (i, j) not in updates:
                        updates[(i, j)] = num

        for col in range(9):
            positions = {num: [] for num in range(1, 10)}
            for row in range(9):
                if (row, col) in self.options:
                    for num in self.options[(row, col)]:
                        positions[num].append((row, col))
            for num, cells in positions.items():
                if len(cells) == 1:
                    i, j = cells[0]
                    if (i, j) not in updates:
                        updates[(i, j)] = num

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                positions = {num: [] for num in range(1, 10)}
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        if (i, j) in self.options:
                            for num in self.options[(i, j)]:
                                positions[num].append((i, j))
                for num, cells in positions.items():
                    if len(cells) == 1:
                        i, j = cells[0]
                        if (i, j) not in updates:
                            updates[(i, j)] = num

        for (i, j), num in updates.items():
            if (i, j) in self.options:
                self.solved_grid[i][j] = num
                self.counts[num] += 1
                self.options.pop((i, j), None)
                self.update_options(i, j, num)
                made_changes = True

        return made_changes

    def backtrack(self):
        if self.is_solved():
            return True

        min_options = 10
        best_cell = None
        for (i, j), options in self.options.items():
            if len(options) == 0:
                return False
            if len(options) < min_options:
                min_options = len(options)
                best_cell = (i, j, options)
        
        if best_cell is None:
            return False
        i, j, options = best_cell

        for num in options:
            saved_grid = copy.deepcopy(self.solved_grid)
            saved_options = copy.deepcopy(self.options)
            saved_counts = self.counts.copy()

            self.solved_grid[i][j] = num
            self.counts[num] += 1
            self.options.pop((i, j), None)
            self.update_options(i, j, num)

            if self.is_solvable():
                while True:
                    updated = False
                    for (row, col), opts in list(self.options.items()):
                        if len(opts) == 1:
                            self.solved_grid[row][col] = opts[0]
                            self.counts[opts[0]] += 1
                            self.options.pop((row, col), None)
                            self.update_options(row, col, opts[0])
                            updated = True
                    if not updated and self.hidden_single():
                        updated = True
                    if not updated:
                        break
                    if self.is_solved():
                        return True
                if self.backtrack():
                    return True

            self.solved_grid = saved_grid
            self.options = saved_options
            self.counts = saved_counts

        return False

    def reveal_position(self, row, col):
        self.grid[row][col] = self.solved_grid[row][col]
        print(f"Number revealed at ({row}, {col}) is {self.solved_grid[row][col]}")

    def display(self, solution=False):
        if solution == False:
            display_grid = self.grid
        else:
            display_grid = self.solved_grid
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            row = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row += "| "
                val = display_grid[i][j]
                if val != 0:
                    row += str(val)  
                else:
                    row += "."
                row += " "
            print(row)

if __name__ == "__main__":
    while True:
        values = input("Type a list of 81 numbers for your board row by row no spaces, put 0s for blanks")
        if len(values) != 81:
            print("Error: You must enter exactly 81 digits.")
            continue

        if not values.isdigit():
            print("Error: The input must only contain digits.")
            continue
        board = SudokuBoard()
        board.fill(values)
        print("Your inputted board:")
        board.display()
        if board.is_solvable():
            print("This board is solvable")
        else:
            print("This board is unsolvable")
            continue
        
        start_time = time.time()
        board.solve()
        end_time = time.time()

        elapsed_time = (end_time - start_time) * 1000
        print(f"Solved in {elapsed_time:.3f} ms")
        while True:
            print("Choose an option: ")
            print("1. Reveal a single position")
            print("2. Reveal the entire solution")
            print("3. Exit")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == "1":
                try:
                    row = int(input("Enter the row (0-8): "))
                    col = int(input("Enter the column (0-8): "))
                    if 0 <= row < 9 and 0 <= col < 9:
                        board.reveal_position(row, col)
                        board.display()
                    else:
                        print("Invalid row or column. Try again.")
                except ValueError:
                    print("Invalid input. Please enter integers for row and column.")
            
            elif choice == "2":
                board.display(solution=True)
                break

            elif choice == "3":
                print("Exiting.")
                break

            else:
                print("Invalid choice. Please select 1, 2, or 3.")

        another_game = input("Do you want to do another one? (yes/no): ")
        if another_game != "yes":
            break