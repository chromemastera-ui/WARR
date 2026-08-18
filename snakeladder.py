"""
insta - manish_aheibam
"""

import random
import tkinter as tk
from tkinter import messagebox



BOARD_SIZE = 10          
CELL_PIXELS = 60         
PLAYER_COLORS = ["#e63946", "#2a9d8f"]   


LADDERS = {
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    78: 98,
    87: 94,
}

SNAKES = {
    16: 6,
    46: 25,
    49: 11,
    62: 19,
    64: 60,
    74: 53,
    89: 68,
    92: 88,
    95: 75,
    99: 80,
}


def cell_to_xy(position):
    """
    Convert a board position (1-100) into (row, col) grid coordinates
    for a boustrophedon (zig-zag) 10x10 board, where position 1 is at
    the bottom-left and 100 is at the top-left/right depending on row
    parity, matching a real Snake & Ladder board layout.

    Returns (row, col) where row 0 is the BOTTOM row and row 9 is the
    TOP row; col 0..9 is left to right.
    """
    position -= 1 
    row = position // BOARD_SIZE
    col = position % BOARD_SIZE
    if row % 2 == 1:
       
        col = BOARD_SIZE - 1 - col
    return row, col


def cell_center_pixels(position, canvas_height):
    """Return (x, y) pixel center of a board cell on the canvas."""
    row, col = cell_to_xy(position)
    x = col * CELL_PIXELS + CELL_PIXELS // 2
   
    y = canvas_height - (row * CELL_PIXELS + CELL_PIXELS // 2)
    return x, y



class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 0  


class SnakeAndLadderGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake and Ladder - 2 Player")
        self.resizable(False, False)

        self.board_pixels = BOARD_SIZE * CELL_PIXELS
        self.players = [Player("Player 1", PLAYER_COLORS[0]), Player("Player 2", PLAYER_COLORS[1])]
        self.current_player_index = 0
        self.game_over = False

        self._build_ui()
        self._draw_board()
        self._draw_players()
        self._update_status()


    def _build_ui(self):
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack()

      
        self.canvas = tk.Canvas(
            main_frame, width=self.board_pixels, height=self.board_pixels, bg="#f1faee"
        )
        self.canvas.grid(row=0, column=0, rowspan=6, padx=(0, 15))

      
        info_frame = tk.Frame(main_frame)
        info_frame.grid(row=0, column=1, sticky="n")

        self.status_var = tk.StringVar()
        tk.Label(
            info_frame, textvariable=self.status_var, font=("Segoe UI", 13, "bold"),
            wraplength=220, justify="left"
        ).pack(pady=(0, 10), anchor="w")

        self.p1_pos_var = tk.StringVar(value="Player 1: square 0")
        self.p2_pos_var = tk.StringVar(value="Player 2: square 0")

        tk.Label(info_frame, textvariable=self.p1_pos_var, fg=PLAYER_COLORS[0],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=2)
        tk.Label(info_frame, textvariable=self.p2_pos_var, fg=PLAYER_COLORS[1],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=2)

        self.dice_var = tk.StringVar(value="🎲 —")
        tk.Label(info_frame, textvariable=self.dice_var, font=("Segoe UI", 28)).pack(pady=15)

        self.roll_btn = tk.Button(
            info_frame, text="Roll Dice", font=("Segoe UI", 12, "bold"),
            bg="#457b9d", fg="white", padx=10, pady=6, command=self.roll_dice
        )
        self.roll_btn.pack(pady=5, fill="x")

        restart_btn = tk.Button(
            info_frame, text="Restart Game", font=("Segoe UI", 10),
            command=self.restart_game
        )
        restart_btn.pack(pady=(5, 15), fill="x")

        tk.Label(info_frame, text="Log:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        log_frame = tk.Frame(info_frame)
        log_frame.pack(fill="both", expand=True)

        self.log_box = tk.Listbox(log_frame, width=30, height=14, font=("Consolas", 9))
        scrollbar = tk.Scrollbar(log_frame, command=self.log_box.yview)
        self.log_box.config(yscrollcommand=scrollbar.set)
        self.log_box.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

  

    def _draw_board(self):
        for pos in range(1, 101):
            row, col = cell_to_xy(pos)
            x0 = col * CELL_PIXELS
            y0 = self.board_pixels - (row + 1) * CELL_PIXELS
            x1 = x0 + CELL_PIXELS
            y1 = y0 + CELL_PIXELS

     
            fill = "#ffffff" if (row + col) % 2 == 0 else "#e9f5f2"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#cccccc")
            self.canvas.create_text(
                x0 + 6, y1 - 6, text=str(pos), anchor="sw",
                font=("Segoe UI", 7), fill="#555555"
            )

      
        for bottom, top in LADDERS.items():
            x0, y0 = cell_center_pixels(bottom, self.board_pixels)
            x1, y1 = cell_center_pixels(top, self.board_pixels)
            self.canvas.create_line(x0, y0, x1, y1, fill="#2a9d8f", width=4, arrow=tk.LAST)

        for head, tail in SNAKES.items():
            x0, y0 = cell_center_pixels(head, self.board_pixels)
            x1, y1 = cell_center_pixels(tail, self.board_pixels)
            self.canvas.create_line(
                x0, y0, x1, y1, fill="#e63946", width=3, dash=(4, 2), arrow=tk.LAST
            )

    def _draw_players(self):
        """(Re)draw player tokens at their current positions."""
        self.canvas.delete("player_token")
        for i, player in enumerate(self.players):
            pos = max(player.position, 1)
            x, y = cell_center_pixels(pos, self.board_pixels)
            
            offset = -10 if i == 0 else 10
            self.canvas.create_oval(
                x + offset - 8, y - 8, x + offset + 8, y + 8,
                fill=player.color, outline="black", tags=("player_token", f"token_{i}")
            )

    def _token_offset(self, index):
        return -10 if index == 0 else 10

    def _draw_single_token(self, index, position):
        """Redraw just one player's token at a given board position (for animation)."""
        player_index = index
        pos = max(position, 1)
        x, y = cell_center_pixels(pos, self.board_pixels)
        offset = self._token_offset(player_index)
        self.canvas.delete(f"token_{player_index}")
        self.canvas.create_oval(
            x + offset - 8, y - 8, x + offset + 8, y + 8,
            fill=self.players[player_index].color, outline="black",
            tags=("player_token", f"token_{player_index}")
        )

    def _animate_move(self, player_index, path, on_complete, step_delay=220):
        """
        Move a token one square at a time along `path` (a list of board
        positions to visit in order), then call on_complete() when done.
        """
        if not path:
            on_complete()
            return

        next_pos = path[0]
        remaining = path[1:]
        self._draw_single_token(player_index, next_pos)

        if remaining:
            self.after(step_delay, lambda: self._animate_move(player_index, remaining, on_complete, step_delay))
        else:
            self.after(step_delay, on_complete)

   

    def _current_player(self):
        return self.players[self.current_player_index]

    def _update_status(self):
        if self.game_over:
            return
        player = self._current_player()
        self.status_var.set(f"{player.name}'s turn\nClick 'Roll Dice' to play.")

    def _log(self, message):
        self.log_box.insert(tk.END, message)
        self.log_box.see(tk.END)

    def roll_dice(self):
        if self.game_over:
            return

        self.roll_btn.config(state="disabled")
        player = self._current_player()
        player_index = self.current_player_index
        roll = random.randint(1, 6)
        self.dice_var.set(f"🎲 {roll}")

        start_pos = player.position
        target = start_pos + roll

        if target > 100:
            self._log(f"{player.name} rolled {roll} -> needs exact number, stays at {start_pos}.")
            self._end_turn(gave_extra_turn=False)
            return

        self._log(f"{player.name} rolled {roll} -> moving {start_pos} to {target}...")

       
        step_path = list(range(start_pos + 1, target + 1)) if start_pos < target else []

        def after_normal_move():
            player.position = target
            self._handle_landing(player, player_index, target, roll)

        self._animate_move(player_index, step_path, after_normal_move)

    def _handle_landing(self, player, player_index, target, roll):
        """Called after the token finishes walking to `target`. Checks for
        ladders/snakes and animates the extra slide if needed."""
        final_pos = target

        if target in LADDERS:
            final_pos = LADDERS[target]
            self._log(f"  🪜 Ladder! Climbing from {target} to {final_pos}.")
            slide_path = list(range(target + 1, final_pos + 1))
        elif target in SNAKES:
            final_pos = SNAKES[target]
            self._log(f"  🐍 Snake! Sliding from {target} down to {final_pos}.")
            slide_path = list(range(target - 1, final_pos - 1, -1))
        else:
            slide_path = []

        def finish():
            player.position = final_pos
            self._draw_single_token(player_index, final_pos)

            if final_pos == 100:
                self._log(f"🏆 {player.name} WINS!")
                self.status_var.set(f"🏆 {player.name} wins the game!")
                self.game_over = True
                self.roll_btn.config(state="disabled")
                messagebox.showinfo("Game Over", f"{player.name} wins the game!")
                return

            self._end_turn(gave_extra_turn=(roll == 6))

        if slide_path:
            
            self._animate_move(player_index, slide_path, finish, step_delay=120)
        else:
            finish()

    def _end_turn(self, gave_extra_turn):
        self.p1_pos_var.set(f"Player 1: square {self.players[0].position}")
        self.p2_pos_var.set(f"Player 2: square {self.players[1].position}")

        if gave_extra_turn:
            self._log(f"  Rolled a 6 -> {self._current_player().name} goes again!")
        else:
            self.current_player_index = 1 - self.current_player_index

        self._update_status()
        self.roll_btn.config(state="normal")

    def restart_game(self):
        for player in self.players:
            player.position = 0
        self.current_player_index = 0
        self.game_over = False
        self.dice_var.set("🎲 —")
        self.log_box.delete(0, tk.END)
        self.p1_pos_var.set("Player 1: square 0")
        self.p2_pos_var.set("Player 2: square 0")
        self.roll_btn.config(state="normal")
        self._draw_players()
        self._update_status()
        self._log("Game restarted.")


if __name__ == "__main__":
    game = SnakeAndLadderGame()
    game.mainloop()