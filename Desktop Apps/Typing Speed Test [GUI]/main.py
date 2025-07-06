from tkinter import *
from tkinter import messagebox, PhotoImage, ttk, simpledialog
import json
import re


# >>>>>>>>>> Constants and Globals <<<<<<<<<<
SCOREBOARD_FILE = "scoreboard.json"
# >>>>>>>>>> UI Constants <<<<<<<<<<
BG_COLOR = "#2E3440"  # Nord Dark
SECONDARY_BG = "#3B4252"
FG_COLOR = "#D8DEE9"  # Nord Light
ACCENT_COLOR = "#88C0D0"  # Nord Frost
ERROR_COLOR = "#BF616A"  # Nord Red

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_DESC = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_GUIDE = ("Segoe UI", 10, "italic")

TIME_LIMIT = 30
timer_id = None
timer_running = False

text_guide = "there are many variations of passages of lorem ipsum available but the majority have suffered alteration in some form " \
             "by injected humour or randomised words which do not look even slightly believable if you are going to use a passage of lorem ipsum " \
             "you need to be sure there is not anything embarrassing hidden in the middle of text all the lorem ipsum generators on the internet " \
             "tend to repeat predefined chunks as necessary making this the first true generator on the internet"

words_list = text_guide.lower().split()


# >>>>>>>>>> Functions, Commands and Methods <<<<<<<<<<

def compare_words():
    """Calculates the score and updates the UI when the timer ends."""
    global words_list
    user_text = typing_box.get("1.0", END).strip()
    user_words_list = user_text.split()

    wrong_words = []
    word_counter = 0

    # Compare word by word up to the number of words typed
    for i, user_word in enumerate(user_words_list):
        if i < len(words_list) and user_word == words_list[i]:
            word_counter += 1
        else:
            wrong_words.append(user_word)

    wpm = word_counter * (60 // TIME_LIMIT)
    wpm_box.config(text=f"{wpm}")

    messagebox.showinfo(
        "Result",
        f"You typed {word_counter} correct words in {TIME_LIMIT}s, resulting in approximately {wpm} WPM.\n"
        f"{len(wrong_words)} words with typos were not counted."
    )

    username = simpledialog.askstring("Save Score", "Enter your username:", parent=root)
    if username:
        # Add score to the scoreboard and save it
        scoreboard.insert('', 'end', values=(username, wpm))
        save_scores()

def countdown(count):
    """Handles the timer countdown logic."""
    global timer_id
    time_box.config(text=f"{count}")
    if count > 0:
        timer_id = root.after(1000, countdown, count - 1)
    else:
        time_box.config(text="Time's up!")
        typing_box.config(state="disabled")
        compare_words()





def start_timer(event=None):
    """Starts the timer if it's not already running."""
    global timer_running
    if not timer_running:
        timer_running = True
        countdown(TIME_LIMIT)


def reset_game():
    """Resets the game to its initial state."""
    global timer_id, timer_running
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

    timer_running = False
    time_box.config(text="--")
    wpm_box.config(text="--")
    typing_box.config(state="normal")
    typing_box.delete("1.0", END)
    


def save_scores():
    """Saves the current scoreboard to a JSON file."""
    scores = []
    for child_id in scoreboard.get_children():
        values = scoreboard.item(child_id)['values']
        if values:
            scores.append({"username": values[0], "wpm": int(values[1])})

    scores.sort(key=lambda x: x['wpm'], reverse=True)

    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=4)


def load_scores():
    """Loads scores from the JSON file into the scoreboard."""
    try:
        with open(SCOREBOARD_FILE, "r") as f:
            scores = json.load(f)
            for score in scores:
                scoreboard.insert('', 'end', values=(score['username'], score['wpm']))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

# >>>>>>>>>> TK Interface <<<<<<<<<<<
# >>>>>> Main window <<<<<<
root = Tk()
root.title("Typing Speed Tester")
root.geometry("800x800")
root.resizable(True, True)
root.configure(bg=BG_COLOR)
root.minsize(800, 600)

# >>>>>> Style Configuration (ttk) <<<<<<
style = ttk.Style(root)
style.theme_use("clam")

# Style for the Scoreboard
style.configure("TTreeview",
                background=SECONDARY_BG,
                foreground=FG_COLOR,
                fieldbackground=SECONDARY_BG,
                borderwidth=0,
                rowheight=25)
style.map('TTreeview', background=[('selected', ACCENT_COLOR)])
style.configure("TTreeview.Heading",
                background=BG_COLOR,
                foreground=FG_COLOR,
                font=FONT_LABEL,
                padding=(10, 5))
style.layout("TTreeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove borders

# Style for the Button
style.configure("TButton",
                background=ACCENT_COLOR,
                foreground=BG_COLOR,
                font=FONT_LABEL,
                padding=10,
                borderwidth=0)
style.map("TButton",
          background=[('active', FG_COLOR)],
          foreground=[('active', BG_COLOR)])

# >>>>>> Frames <<<<<<
left_frame = Frame(root, bg=BG_COLOR, padx=20, pady=20)
left_frame.pack(side="left", fill="both", expand=True)

right_frame = Frame(root, bg=SECONDARY_BG, padx=20, pady=20)
right_frame.pack(side="right", fill="y")

# >>>>>> Logo <<<<<<
try:
    logo_img = PhotoImage(file="typing_logo.png")
    logo_canvas = Canvas(left_frame, width=60, height=60, bg=BG_COLOR, highlightthickness=0)
    logo_canvas.create_image(30, 30, image=logo_img)
    logo_canvas.grid(row=0, column=0, columnspan=2, pady=(0, 10))
except TclError:
    pass

# >>>>>> Title and Description <<<<<<
title_label = Label(left_frame, text="Typing Speed Tester", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
title_label.grid(row=1, column=0, columnspan=2, pady=(0, 5))

desc_label = Label(
    left_frame,
    text=f"Type the text below in {TIME_LIMIT} seconds and find out your speed in Words Per Minute (WPM).",
    bg=BG_COLOR, fg=FG_COLOR, justify="center", font=FONT_DESC, wraplength=500
)
desc_label.grid(row=2, column=0, columnspan=2, pady=(0, 20))

# >>>>>> Labels <<<<<<
wpm_label = Label(left_frame, text="WPM", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR)
wpm_label.grid(row=3, column=0, pady=(5, 2))
wpm_box = Label(left_frame, text="--", relief="flat", width=10, height=2, bg=SECONDARY_BG, fg=FG_COLOR, font=FONT_TITLE)
wpm_box.grid(row=4, column=0, padx=10)

time_label = Label(left_frame, text="Time Remaining", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR)
time_label.grid(row=3, column=1, pady=(5, 2))
time_box = Label(left_frame, text="--", relief="flat", width=10, height=2, bg=SECONDARY_BG, fg=FG_COLOR, font=FONT_TITLE)
time_box.grid(row=4, column=1, padx=10)

guidetext_widget = Message(left_frame, text=text_guide, width=500, font=FONT_GUIDE, bg=BG_COLOR, fg=ACCENT_COLOR, justify="left")
guidetext_widget.grid(row=5, column=0, columnspan=2, pady=20)

# >>>>>> Entries <<<<<<
typing_box = Text(left_frame, height=5, width=50, relief="flat", wrap="word", bg=SECONDARY_BG, fg=FG_COLOR,
                  font=FONT_BODY, insertbackground=FG_COLOR, bd=5, selectbackground=ACCENT_COLOR)
typing_box.tag_configure("error", background=ERROR_COLOR, foreground=FG_COLOR)
typing_box.bind("<KeyPress>", start_timer)
typing_box.grid(row=6, column=0, columnspan=2, pady=10)

# >>>>>> Buttons <<<<<<
reset_button = ttk.Button(left_frame, text="Restart", command=reset_game, style="TButton")
reset_button.grid(row=7, column=0, columnspan=2, pady=5)

# >>>>>> Scoreboard <<<<<<
score_title = Label(right_frame, text="Scoreboard", font=FONT_TITLE, bg=SECONDARY_BG, fg=FG_COLOR)
score_title.pack(pady=(10, 0))

score_subtitle = Label(right_frame, text="See where you rank", bg=SECONDARY_BG, fg=FG_COLOR, font=FONT_DESC)
score_subtitle.pack(pady=(0, 10))

scoreboard = ttk.Treeview(right_frame, columns=("Username", "WPM"), show="headings", height=20, style="TTreeview")
scoreboard.heading("Username", text="Username")
scoreboard.heading("WPM", text="WPM")
scoreboard.column("Username", width=120, anchor="center")
scoreboard.column("WPM", width=80, anchor="center")
scoreboard.pack()

load_scores()


root.mainloop()