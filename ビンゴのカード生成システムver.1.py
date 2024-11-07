import tkinter as tk
import random

class BingoCard:
    def __init__(self):
        self.card = self.generate_card()
        self.selected_numbers = set()

    def generate_card(self):
        card = []
        numbers = list(range(1, 76))  # ビンゴの数字は1から75まで
        random.shuffle(numbers)

        # ビンゴカードを生成（5x5のグリッド）
        for i in range(5):
            row = numbers[i*15:(i+1)*15][:5]  # 各列に15の数字から5を選ぶ
            card.append(sorted(row))
        card[2][2] = 'FREE'  # 中央のセルは「フリー」
        return card

    def mark_number(self, number):
        if number in self.selected_numbers:
            return False
        self.selected_numbers.add(number)
        return True

    def check_bingo(self):
        # ビンゴの成立チェック
        rows = [all(num in self.selected_numbers or num == 'FREE' for num in row) for row in self.card]
        cols = [all(self.card[row][col] in self.selected_numbers or self.card[row][col] == 'FREE' for row in range(5)) for col in range(5)]
        diag1 = all(self.card[i][i] in self.selected_numbers or self.card[i][i] == 'FREE' for i in range(5))
        diag2 = all(self.card[i][4-i] in self.selected_numbers or self.card[i][4-i] == 'FREE' for i in range(5))
        return any(rows) or any(cols) or diag1 or diag2

    def check_reach(self):
        # リーチの判定（未選択のセルが1つだけ残っている場合）
        def count_unmarked_and_check(line):
            unmarked_count = 0
            for num in line:
                if num not in self.selected_numbers and num != 'FREE':
                    unmarked_count += 1
            return unmarked_count == 1  # 未選択のセルが1つだけのときリーチ

        rows = [count_unmarked_and_check(row) for row in self.card]
        cols = [count_unmarked_and_check([self.card[row][col] for row in range(5)]) for col in range(5)]
        diag1 = count_unmarked_and_check([self.card[i][i] for i in range(5)])
        diag2 = count_unmarked_and_check([self.card[i][4-i] for i in range(5)])
        return any(rows) or any(cols) or diag1 or diag2

class BingoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Card Generator")
        self.bingo_card = BingoCard()

        self.buttons = []
        for i in range(5):
            row_buttons = []
            for j in range(5):
                btn = tk.Button(root, text=self.bingo_card.card[i][j], font=('Arial', 20), width=4, height=2,
                                command=lambda x=self.bingo_card.card[i][j]: self.select_number(x))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.result_label = tk.Label(root, text="", font=('Arial', 16))
        self.result_label.grid(row=6, column=0, columnspan=5)

    def select_number(self, number):
        if self.bingo_card.mark_number(number):
            for i in range(5):
                for j in range(5):
                    if self.bingo_card.card[i][j] == number:
                        self.buttons[i][j].config(bg='lightgreen')
            if self.bingo_card.check_bingo():
                self.result_label.config(text="BINGO!")
            elif self.bingo_card.check_reach():
                self.result_label.config(text="リーチ！")
            else:
                self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = BingoApp(root)
    root.mainloop()
