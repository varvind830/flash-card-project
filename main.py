from tkinter import *
import pandas as pd
import random
from tkinter import messagebox
import os

word = {}

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- CREATE NEW FLASH CARD ------------------------------- #
try:
    flashcard_df = pd.read_csv("data/words_to_learn.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    original_data = pd.read_csv("data/french_words.csv")
    flashcard_dict = original_data.to_dict(orient="records")
else:
    flashcard_dict = flashcard_df.to_dict(orient="records")


def check_next_card():
    global word, flip_timer
    try:
        flashcard_dict.remove(word)
        next_card()
    except IndexError:
        messagebox.showinfo(title="Congrats!", message="Congrats! You've learned every word in the flashcard app!")
        file = "data/words_to_learn.csv"
        if (os.path.exists(file) and os.path.isfile(file)):
            os.remove(file)
        window.destroy()
    else:
        words_to_learn = flashcard_dict
        pd.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv", index=False)


def next_card():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = random.choice(flashcard_dict)
    french_language = list(word.keys())[0]
    flashcard_canvas.itemconfig(flashcard_canvas_img, image=front_card_img)

    flashcard_canvas.itemconfig(language_text, text=french_language, fill="black")
    flashcard_canvas.itemconfig(word_text, text=word[french_language], fill="black")
    flip_timer = window.after(3000, card_flip)


# ---------------------------- FLIP THE CARD ------------------------------- #
def card_flip():
    english_language = list(word.keys())[1]
    flashcard_canvas.itemconfig(flashcard_canvas_img, image=back_card_img)
    flashcard_canvas.itemconfig(language_text, fill="white", text=english_language)
    flashcard_canvas.itemconfig(word_text, fill="white", text=word[english_language])


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")
flip_timer = window.after(3000, card_flip)

# Canvas
flashcard_canvas = Canvas(width=800, height=526)
flashcard_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
flashcard_canvas_img = flashcard_canvas.create_image(400, 263, image=front_card_img)

language_text = flashcard_canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = flashcard_canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

flashcard_canvas.grid(column=0, row=0, columnspan=2)

# Button
xmark_img = PhotoImage(file="images/wrong.png")
x_button = Button(image=xmark_img, highlightthickness=0, command=next_card)
x_button.grid(column=0, row=1)

checkmark_img = PhotoImage(file="images/right.png")
check_button = Button(image=checkmark_img, highlightthickness=0, command=check_next_card)
check_button.grid(column=1, row=1)

next_card()
window.mainloop()
