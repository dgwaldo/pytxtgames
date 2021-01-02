# coding=utf-8
import random


def draw_gallows(hang_count):
    head, arms, stomach, legs, feet = "", "", "", "", ""
    if hang_count >= 2:
        head = "0"
    if hang_count >= 3:
        arms = r"\|/"
    if hang_count >= 4:
        stomach = "X"
    if hang_count >= 5:
        legs = r"/ \"
    if hang_count >= 6:
        feet = "() ()"

    print("""
    |-----------|
    |           |
    |           {0} 
    |          {1}
    |           {2}
    |          {3}
    |         {4}
____|____""".format(head, arms, stomach, legs, feet))


def get_words():
    return ["dog", "frog", "hog", "slob", "bacon", "avacado", "jelly", "mommy", "grandma", "mississippi", "minnesota",
            "noodles", "chicken", "liver", "tap", "jenny", "moose", "light", "bulb", "lake", "river", "bear", "grill",
            "yarn", "antelope", "chair", "snake", "bite", "barn", "door", "noel", "snot", "shark", "beard", "beard",
            "socks", "bank", "victoria", "lizard", "lion", "pig" "sock", "ankle", "muffin", "target", "dress"]


def main():
    words = get_words()
    random_idx = random.randrange(0, len(words), 1)
    chosen = words[random_idx]
    print("------Welcome to Hang-Man------")
    print("The word we have choose has {0} letters: \n".format(len(chosen)))
    blanks = ['_ ' for s in chosen if s]
    print(blanks)

    hang_man_count = 0
    correct_letter_count = 0
    while correct_letter_count <= len(chosen) and hang_man_count < 6:
        letter = str(input("Please input a letter: ")).lower()
        letter_idx = chosen.find(letter)
        if letter_idx != -1:
            for i in range(0, len(chosen)):
                if chosen[i] == letter:
                    blanks[i] = letter
        else:
            hang_man_count += 1
            draw_gallows(hang_man_count)
        print(str(blanks))
        if blanks.count('_ ') == 0:
            print(chosen)
            print("THE PRESIDENT WOULD SAY YOU ARE A WINNER!!!!\n\n")
            return main()
        if hang_man_count == 6:
            print("The word was: " + chosen)
            print("THE PRESIDENT WOULD SAY YOU ARE A LOSER!!!!\n\n")
            return main()


if __name__ == '__main__':
    main()