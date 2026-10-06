import tkinter as tk
from tkinter import ttk

# --- Configuration & Data ---
SUBJECTS = [
    "Data Structures",
    "DBMS",
    "Computer Networks",
    "Operating Systems"
]

N = len(SUBJECTS)

# Color palette (Modern dark theme)
COLOR_BG = "#0b1120"          # Deep background
COLOR_PANEL = "#1e293b"       # Card / Container background
COLOR_BORDER = "#334155"      # Subtle border
COLOR_TEXT_MAIN = "#f8fafc"   # High-contrast text
COLOR_TEXT_MUTED = "#94a3b8"  # Subtle text
COLOR_CELL_1 = "#1e293b"      # Checker pattern 1
COLOR_CELL_2 = "#273549"      # Checker pattern 2

COLOR_TRYING = "#f59e0b"      # Amber (probing slot)
COLOR_CONFLICT = "#ef4444"    # Red (conflict found)
COLOR_PLACED = "#10b981"      # Emerald green (safely placed)
COLOR_BACKTRACK = "#64748b"   # Slate gray (backtracking)
COLOR_ACCENT = "#38bdf8"      # Light sky blue accent


class ExamSchedulerVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Timetable Scheduler - N-Queens Backtracking Demo")
        
        # Responsive, compact window sizing that comfortably fits 1080p, 720p, and laptop screens
        self.root.geometry("960x650")
        self.root.minsize(880, 580)
        self.root.configure(bg=COLOR_BG)

        self.board = [-1] * N
        self.solutions = []
        self.history_steps = []
        self.current_step_idx = 0
        self.is_running = False
        self.speed_ms = 500

        self._precompute_trace()
        self._build_ui()
        self.root.update_idletasks()
        self.draw_board()

    def _precompute_trace(self):
        """Generates step-by-step trace of the backtracking algorithm."""
        board = [-1] * N
        self.history_steps = []
        self.solutions = []

        def is_safe(r, c):
            for i in range(r):
                if board[i] == c:
                    return False, f"Direct slot clash with '{SUBJECTS[i]}' (Slot {c+1})"
                if abs(board[i] - c) == abs(i - r):
                    return False, f"Diagonal constraint clash with '{SUBJECTS[i]}' (Slot {board[i]+1})"
            return True, "Safe assignment!"

        def backtrack(row):
            if row == N:
                sol = board.copy()
                self.solutions.append(sol)
                self.history_steps.append({
                    "type": "solution",
                    "row": None,
                    "col": None,
                    "board": sol,
                    "solution_index": len(self.solutions),
                    "msg": f" Found Valid Conflict-Free Timetable #{len(self.solutions)}!"
                })
                return

            for col in range(N):
                safe, reason = is_safe(row, col)

                # Probing step
                board[row] = col
                self.history_steps.append({
                    "type": "trying" if safe else "conflict",
                    "row": row,
                    "col": col,
                    "board": board.copy(),
                    "msg": f"Checking '{SUBJECTS[row]}' in Slot {col + 1} ... {reason}"
                })

                if safe:
                    self.history_steps.append({
                        "type": "placed",
                        "row": row,
                        "col": col,
                        "board": board.copy(),
                        "msg": f" Assigned '{SUBJECTS[row]}' -> Slot {col + 1}. Moving to next subject."
                    })
                    backtrack(row + 1)

                    # Backtracking
                    board[row] = -1
                    self.history_steps.append({
                        "type": "backtrack",
                        "row": row,
                        "col": col,
                        "board": board.copy(),
                        "msg": f" Backtracking: Resetting '{SUBJECTS[row]}' from Slot {col + 1}."
                    })
                else:
                    board[row] = -1

        backtrack(0)

    def _build_ui(self):
        # 1. Top Header
        top_frame = tk.Frame(self.root, bg=COLOR_BG)
        top_frame.pack(fill=tk.X, padx=20, pady=(12, 6))

        title = tk.Label(
            top_frame,
            text="Exam Timetable Scheduler",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            top_frame,
            text="N-Queens Backtracking search with conflict resolution and solution extraction",
            font=("Segoe UI", 9),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG
        )
        subtitle.pack(anchor="w")

        # 2. Main Middle Area (Board on Left, Solution Panel on Right)
        middle_frame = tk.Frame(self.root, bg=COLOR_BG)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=4)

        # Left Column: Canvas for Grid
        left_container = tk.Frame(middle_frame, bg=COLOR_PANEL, highlightthickness=1, highlightbackground=COLOR_BORDER)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        grid_title = tk.Label(
            left_container,
            text="LIVE SEARCH BOARD",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_PANEL,
            padx=10, pady=6
        )
        grid_title.pack(anchor="w")

        self.canvas = tk.Canvas(
            left_container,
            bg=COLOR_PANEL,
            bd=0,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.canvas.bind("<Configure>", lambda event: self.draw_board())

        # Right Column: Final Solution & Timetable Panel
        right_container = tk.Frame(middle_frame, bg=COLOR_PANEL, width=320, highlightthickness=1, highlightbackground=COLOR_BORDER)
        right_container.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        right_container.pack_propagate(False)

        sol_header = tk.Label(
            right_container,
            text="FINAL SCHEDULE / TIMETABLE",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_PLACED,
            bg=COLOR_PANEL,
            padx=12, pady=8
        )
        sol_header.pack(anchor="w")

        # Solution status banner
        self.sol_banner_var = tk.StringVar(value="⏳ Searching for solution...")
        self.sol_banner = tk.Label(
            right_container,
            textvariable=self.sol_banner_var,
            font=("Segoe UI", 10, "bold"),
            fg="#fbbf24",
            bg="#1e293b",
            padx=12, pady=4,
            anchor="w"
        )
        self.sol_banner.pack(fill=tk.X)

        # Solution Cards Frame
        self.sol_cards_frame = tk.Frame(right_container, bg=COLOR_PANEL, padx=12, pady=10)
        self.sol_cards_frame.pack(fill=tk.BOTH, expand=True)

        self.sol_rows = []
        for i, subj in enumerate(SUBJECTS):
            card = tk.Frame(self.sol_cards_frame, bg="#0f172a", bd=1, relief=tk.SOLID, padx=10, pady=8)
            card.pack(fill=tk.X, pady=4)

            s_lbl = tk.Label(card, text=subj, font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MAIN, bg="#0f172a", anchor="w")
            s_lbl.pack(side=tk.LEFT)

            slot_var = tk.StringVar(value="--")
            slot_lbl = tk.Label(card, textvariable=slot_var, font=("Consolas", 10, "bold"), fg=COLOR_TEXT_MUTED, bg="#0f172a")
            slot_lbl.pack(side=tk.RIGHT)

            self.sol_rows.append((card, slot_var, slot_lbl))

        # Solutions selector buttons (to toggle Solution 1, Solution 2, etc.)
        self.sol_nav_frame = tk.Frame(right_container, bg=COLOR_PANEL, padx=12, pady=8)
        self.sol_nav_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.total_sol_lbl = tk.Label(
            self.sol_nav_frame,
            text="Solutions Found: 0",
            font=("Segoe UI", 9),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_PANEL
        )
        self.total_sol_lbl.pack(side=tk.LEFT)

        # 3. Status Bar
        status_card = tk.Frame(self.root, bg="#111827", highlightthickness=1, highlightbackground=COLOR_BORDER)
        status_card.pack(fill=tk.X, padx=20, pady=(6, 6))

        self.status_var = tk.StringVar(value=" Ready! Click '▶ Start Animation' or use '⏭ Next Step'.")
        status_lbl = tk.Label(
            status_card,
            textvariable=self.status_var,
            font=("Consolas", 10, "bold"),
            fg="#38bdf8",
            bg="#111827",
            padx=10, pady=6,
            anchor="w"
        )
        status_lbl.pack(fill=tk.X)

        # 4. Controls & Legend Bar
        bottom_frame = tk.Frame(self.root, bg=COLOR_BG)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 12))

        btn_style = {
            "font": ("Segoe UI", 9, "bold"),
            "bd": 0,
            "padx": 12,
            "pady": 5,
            "cursor": "hand2"
        }

        self.btn_play = tk.Button(
            bottom_frame,
            text="▶ Start Animation",
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            command=self.toggle_play,
            **btn_style
        )
        self.btn_play.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_step = tk.Button(
            bottom_frame,
            text="⏭ Next Step",
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            command=self.step_forward,
            **btn_style
        )
        self.btn_step.pack(side=tk.LEFT, padx=6)

        self.btn_solution = tk.Button(
            bottom_frame,
            text="★ Jump to Solution",
            bg="#059669",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            command=self.jump_to_first_solution,
            **btn_style
        )
        self.btn_solution.pack(side=tk.LEFT, padx=6)

        self.btn_reset = tk.Button(
            bottom_frame,
            text="↺ Reset",
            bg="#475569",
            fg="white",
            activebackground="#64748b",
            activeforeground="white",
            command=self.reset,
            **btn_style
        )
        self.btn_reset.pack(side=tk.LEFT, padx=6)

        # Speed slider
        speed_box = tk.Frame(bottom_frame, bg=COLOR_BG)
        speed_box.pack(side=tk.RIGHT, padx=5)

        speed_lbl = tk.Label(speed_box, text="Speed:", font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_BG)
        speed_lbl.pack(side=tk.LEFT, padx=(0, 4))

        self.speed_slider = tk.Scale(
            speed_box,
            from_=100,
            to=1000,
            orient=tk.HORIZONTAL,
            showvalue=False,
            bg=COLOR_BG,
            fg=COLOR_TEXT_MAIN,
            troughcolor="#334155",
            highlightthickness=0,
            length=100,
            command=self.on_speed_change
        )
        self.speed_slider.set(self.speed_ms)
        self.speed_slider.pack(side=tk.LEFT)

        # Legend dots
        legend_frame = tk.Frame(bottom_frame, bg=COLOR_BG)
        legend_frame.pack(side=tk.RIGHT, padx=(0, 20))

        legends = [
            ("🟡 Testing", COLOR_TRYING),
            ("🔴 Conflict", COLOR_CONFLICT),
            ("🟢 Safe", COLOR_PLACED),
            ("⚪ Backtrack", COLOR_BACKTRACK),
        ]
        for text, color in legends:
            dot = tk.Label(legend_frame, text="●", fg=color, bg=COLOR_BG, font=("Segoe UI", 10))
            dot.pack(side=tk.LEFT, padx=(5, 1))
            lbl = tk.Label(legend_frame, text=text, fg=COLOR_TEXT_MUTED, bg=COLOR_BG, font=("Segoe UI", 8))
            lbl.pack(side=tk.LEFT, padx=(0, 6))

    def on_speed_change(self, val):
        self.speed_ms = int(val)

    def update_solution_display(self, sol, sol_num=1):
        """Displays the extracted timetable in the right panel cleanly."""
        self.sol_banner_var.set(f"✔ Solution #{sol_num} (Conflict Free)")
        self.sol_banner.config(fg="#10b981")
        self.total_sol_lbl.config(text=f"Solutions Found: {len(self.solutions)}")

        for i in range(N):
            slot_idx = sol[i]
            card, var, lbl = self.sol_rows[i]
            var.set(f"Slot {slot_idx + 1}")
            lbl.config(fg="#38bdf8")
            card.config(highlightbackground="#10b981", highlightthickness=1)

    def reset_solution_display(self):
        self.sol_banner_var.set("⏳ Searching for solution...")
        self.sol_banner.config(fg="#fbbf24")
        self.total_sol_lbl.config(text=f"Solutions: {len(self.solutions)} total")
        for card, var, lbl in self.sol_rows:
            var.set("--")
            lbl.config(fg=COLOR_TEXT_MUTED)
            card.config(highlightthickness=0)

    def draw_board(self, current_step=None):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 50 or height < 50:
            return

        # Adaptive layout: compute cell sizes automatically so it ALWAYS fits
        label_width = 150  # space reserved for subject titles
        top_offset = 36    # space reserved for column headers (Slot 1..N)
        bottom_offset = 20
        right_offset = 20

        avail_w = max(100, width - label_width - right_offset)
        avail_h = max(100, height - top_offset - bottom_offset)

        cell_size = max(35, min(avail_w // N, avail_h // N, 75))
        grid_w = cell_size * N
        grid_h = cell_size * N

        # Center grid inside canvas
        start_x = label_width + (avail_w - grid_w) // 2
        start_y = top_offset + (avail_h - grid_h) // 2

        # Draw Column Headers (Slots)
        for col in range(N):
            cx = start_x + col * cell_size + cell_size // 2
            cy = start_y - 16
            self.canvas.create_text(
                cx, cy,
                text=f"Slot {col + 1}",
                fill=COLOR_ACCENT,
                font=("Segoe UI", 9, "bold")
            )

        active_board = current_step["board"] if current_step else self.board
        active_row = current_step["row"] if current_step else None
        active_col = current_step["col"] if current_step else None
        step_type = current_step["type"] if current_step else None

        for row in range(N):
            # Draw Row Label (Subject)
            ry = start_y + row * cell_size + cell_size // 2
            self.canvas.create_text(
                start_x - 12, ry,
                text=SUBJECTS[row],
                anchor=tk.E,
                fill=COLOR_TEXT_MAIN,
                font=("Segoe UI", 9, "bold")
            )

            for col in range(N):
                x1 = start_x + col * cell_size
                y1 = start_y + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                cell_bg = COLOR_CELL_1 if (row + col) % 2 == 0 else COLOR_CELL_2
                is_active_cell = (row == active_row and col == active_col)

                if is_active_cell:
                    if step_type == "trying":
                        cell_bg = "#78350f"  # amber dark
                    elif step_type == "conflict":
                        cell_bg = "#7f1d1d"  # red dark
                    elif step_type == "placed":
                        cell_bg = "#064e3b"  # green dark

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=cell_bg,
                    outline=COLOR_BORDER,
                    width=1
                )

                # Token logic
                is_placed = (active_board[row] == col)
                if is_placed or (is_active_cell and step_type == "conflict"):
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    r = max(12, cell_size // 3 - 2)

                    token_color = COLOR_PLACED
                    symbol = "✔"

                    if is_active_cell:
                        if step_type == "trying":
                            token_color = COLOR_TRYING
                            symbol = "?"
                        elif step_type == "conflict":
                            token_color = COLOR_CONFLICT
                            symbol = "✖"
                        elif step_type == "placed":
                            token_color = COLOR_PLACED
                            symbol = "✔"
                    elif step_type == "solution":
                        token_color = "#10b981"
                        symbol = "★"

                    self.canvas.create_oval(
                        cx - r, cy - r, cx + r, cy + r,
                        fill=token_color,
                        outline="#ffffff",
                        width=2
                    )
                    self.canvas.create_text(
                        cx, cy,
                        text=symbol,
                        fill="#ffffff",
                        font=("Segoe UI", max(9, int(cell_size * 0.22)), "bold")
                    )

    def step_forward(self):
        if self.current_step_idx >= len(self.history_steps):
            self.is_running = False
            self.btn_play.config(text="▶ Start Animation")
            self.status_var.set(" Search complete! All paths and solutions verified.")
            return

        step = self.history_steps[self.current_step_idx]
        self.status_var.set(f"Step {self.current_step_idx + 1}/{len(self.history_steps)}: {step['msg']}")
        self.draw_board(step)

        if step["type"] == "solution":
            self.update_solution_display(step["board"], step.get("solution_index", 1))

        self.current_step_idx += 1

    def _run_loop(self):
        if not self.is_running:
            return

        if self.current_step_idx < len(self.history_steps):
            self.step_forward()
            self.root.after(self.speed_ms, self._run_loop)
        else:
            self.is_running = False
            self.btn_play.config(text="▶ Start Animation")

    def toggle_play(self):
        if self.is_running:
            self.is_running = False
            self.btn_play.config(text="▶ Resume Animation")
        else:
            if self.current_step_idx >= len(self.history_steps):
                self.reset()
            self.is_running = True
            self.btn_play.config(text="⏸ Pause Animation")
            self._run_loop()

    def jump_to_first_solution(self):
        """Immediately fast-forwards to the first complete solution."""
        self.is_running = False
        self.btn_play.config(text="▶ Resume Animation")
        
        # Locate first solution index in steps
        for idx, step in enumerate(self.history_steps):
            if step["type"] == "solution":
                self.current_step_idx = idx
                self.step_forward()
                return

    def reset(self):
        self.is_running = False
        self.current_step_idx = 0
        self.board = [-1] * N
        self.btn_play.config(text="▶ Start Animation")
        self.status_var.set(" Visualizer reset. Click 'Start Animation' or 'Jump to Solution'.")
        self.reset_solution_display()
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExamSchedulerVisualizer(root)
    root.mainloop()
