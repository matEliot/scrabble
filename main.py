import os
import random
import json
from tkinter import messagebox

FOLDER = 'DATA'
TYPE_EM, TYPE_DL, TYPE_TL, TYPE_DW, TYPE_TW = '--', '2l', '3l', '2w', '3w'
colors = {TYPE_EM: "\033[0m", TYPE_DL: "\033[34m", TYPE_TL: "\033[94m", TYPE_DW: "\033[31m", TYPE_TW: "\033[91m", "else": "\033[33m", "special": "\033[93m"}
board = [
    [TYPE_TW, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_TW],
    [TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM],
    [TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM],
    [TYPE_DL, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_DL],
    [TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM],
    [TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM],
    [TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM],
    [TYPE_TW, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_TW],
    [TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM],
    [TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM],
    [TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_EM],
    [TYPE_DL, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_DL],
    [TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM],
    [TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM],
    [TYPE_TW, TYPE_EM, TYPE_EM, TYPE_DL, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_TW, TYPE_EM, TYPE_EM, TYPE_EM, TYPE_DW, TYPE_EM, TYPE_EM, TYPE_TW]
]
scores = {
    '-': 0, 'E': 1, 'A': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1,
    'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
    'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10
}
quantity = {
    'K': 1, 'J': 1, 'X': 1, 'Q': 1, 'Z': 1, '-': 2, 'B': 2, 'C': 2, 'M': 2, 'P': 2, 'F': 2, 'H': 2, 'V': 2, 'W': 2, 'Y': 2,
    'G': 3, 'L': 4, 'S': 4, 'U': 4, 'D': 4, 'N': 6, 'R': 6, 'T': 6, 'O': 8, 'A': 9, 'I': 9, 'E': 12
}
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ-'
square_letters = letters[0:15]
square_digits = list(range(0, 15))
first_move = True
opposite_direction = {">": "V", "V": ">"}
user_end = False
bot_end = False
err_color = "\033[31m"
special = []

DATA = {}
for filename in os.listdir(FOLDER):
    with open(f'{FOLDER}/{filename}', 'r') as readfile:
        DATA[filename.split('_')[1].replace('.json', '')] = json.load(readfile)

tiles = []
for l in letters:
    for i in range(quantity[l]):
        tiles.append(l)
random.shuffle(tiles)

def display():
    print()
    print(f'{colors["--"]} A  B  C  D  E  F  G  H  I  J  K  L  M  N  O')
    for i_id, i in enumerate(board):
        row_display = ''
        for j_id, j in enumerate(i):
            dis = j
            if len(dis) == 1:
                dis = ' ' + dis
            if j in colors:
                color = colors[j]
            else:
                color = colors["else"]
            if f'{i_id}{j_id}' in special:
                color = colors["special"]
            row_display += f'{color} {dis}'
        print(f'{row_display} {colors["--"]}{i_id + 1}')

def getTile(amount=1):
    global tiles
    return_tiles = []
    for i in range(amount):
        if len(tiles) == 0:
            break;
        return_tiles.append(tiles[0])
        tiles.pop(0)
    return return_tiles

def getDif(str1, str2, get_chars=False):
    c = 0
    a = []
    for i in set(str1):
        c_ = str1.count(i) - str2.count(i)
        if c_ > 0:
            a.append(i)
            c += c_
    if get_chars:
        return a
    else:
        return c

def getWordScore(w):
    s = 0
    for i in w:
        s += scores[i]
    return s

def getBestTile(w):
    b = '-'
    s = 0
    for l in w:
        s_ = scores[l]
        if s_ > s:
            s = s_
            b = l
    return b

def getBestWord(l):
    b = ''
    s = 0
    for w in l:
        s_ = getWordScore(w)
        better_tile = False
        if s_ == s:
            btw = scores[getBestTile(w)]
            btb = scores[getBestTile(b)]
            if btw > btb:
                better_tile = True
            elif btw == btb:
                if random.randint(0, 1) == 0:
                    better_tile = True
        if s_ > s or better_tile:
            s = s_
            b = w
    return b

def getExtraWord(start, direction, direction2=1):
    min_y, min_x = start
    max_y, max_x = start
    if direction == ">":
        if direction2 == 1:
            max_x = 14
        else:
            min_x = 0
    else:
        if direction2 == 1:
            max_y = 14
        else:
            min_y = 0
    x_range = list(range(min_x, max_x + 1))
    y_range = list(range(min_y, max_y + 1))
    if len(x_range) == 1:
        x_range = [start[1]] * len(y_range)
    else:
        y_range = [start[0]] * len(x_range)
    word = ''
    go_through = range(len(x_range))
    if direction2 == -1:
        go_through = reversed(go_through)
    for i in go_through:
        value = board[y_range[i]][x_range[i]]
        if value[0] == " ":
            if direction2 == -1:
                word = value[1] + word
            else:
                word += value[1]
        else:
            break
    return word

def placeTile(start, hand, word, direction='>', bypass=False, hypothetical=False):
    global special
    hand_ = hand.copy()
    word_score = getWordScore(word)
    extra_words = {}
    extra_word_score = 0
    bonus = 0
    multiplier = 1
    interacted = False
    place_in = []
    written_in = 0
    for i, l in enumerate(word):
        intersection = False
        blank = False
        y, x, x_i, y_i = 0, 0, [-1, 1], [-1, 1]
        if direction == '>':
            x, x_i = i, [i, i]
        else:
            y, y_i = i, [i, i]
        bonus = 0
        if start[0] + y not in square_digits or start[1] + x not in square_digits:
            return "The word goes out of range"
        square_value = board[start[0] + y][start[1] + x]
        if l not in square_value:
            if square_value[0] == " ":
                return f'Ran into {square_value}'
            if l in hand_:
                hand_.remove(l)
            elif '-' in hand_:
                hand_.remove('-')
                word_score -= scores[l]
                blank = True
            else:
                return f"You don't have the letter {l}"
        else:
            interacted = True
            intersection = True
        if not intersection:
            extra_word = ['', '']
            for j in range(2):
                y_start, x_start = start[0] + y_i[j], start[1] + x_i[j]
                if y_start in square_digits and x_start in square_digits and board[y_start][x_start][0] == " ":
                    extra_word[j] = getExtraWord([y_start, x_start], direction=opposite_direction[direction], direction2=[-1, 1][j])
                    interacted = True
            formed = extra_word[0] + l + extra_word[1]
            if formed != l:
                if formed not in DATA['']:
                    return f"{l} creates invalid word formation ({formed})"
                else:
                    extra_words[formed] = getWordScore(formed)
                    extra_word_score += extra_words[formed]
        match square_value:
            case '2l':
                bonus = scores[l]
            case '3l':
                bonus = scores[l] * 2
            case '2w':
                multiplier *= 2
                if formed != l:
                    extra_word_score += extra_words[formed]
            case '3w':
                multiplier *= 3
                if formed != l:
                    extra_word_score += extra_words[formed] * 2
        if not blank:
            word_score += bonus
        place_in.append([start[0] + y, start[1] + x])
        if board[place_in[-1][0]][place_in[-1][1]][0] != " ":
            written_in += 1
    y_i, x_i = [-1, len(word)], [-1, len(word)]
    extra_word = ['', '']
    err_check = [[0, 0], [len(word) - 1, 0]]
    if direction == '>':
        y_i = [0, 0]
    else:
        x_i = [0, 0]
        err_check[1] = [0, len(word) - 1]
    for j in range(2):
        y_start, x_start = start[0] + y_i[j], start[1] + x_i[j]
        if y_start in square_digits and x_start in square_digits and board[y_start][x_start][0] == " ":
            if start[1] + err_check[j][1] in square_digits and start[0] + err_check[j][0] in square_digits and board[start[0] + err_check[j][0]][start[1] + err_check[j][1]][0] == " ":
                if j == 0:
                    return 'Invalid starting position'
                else:
                   return 'Invalid ending position'
            extra_word[j] = getExtraWord([y_start, x_start], direction=direction, direction2=[-1, 1][j])
            interacted = True
    formed = extra_word[0] + word + extra_word[1]
    if formed != word:
        if formed in DATA['']:
            extra_word_score += getWordScore(formed) * multiplier
        else:
            return f'Invalid word formation ({formed})'
    if not bypass and not interacted:
        return "The word you placed doesn't interact with anything"
    if not written_in:
        return "Writing over word not allowed"
    elif written_in == 7:
        bonus += 50
    if not hypothetical:
        special = []
        for sq in range(len(place_in)):
            board[place_in[sq][0]][place_in[sq][1]] = ' ' + word[sq]
            special.append(f'{place_in[sq][0]}{place_in[sq][1]}')
        hand[:] = hand_.copy()
    return word_score * multiplier + extra_word_score + bonus

def bot_exchange():
    global tiles, bot_end
    if 7 > len(tiles):
        bot_end = True
        messagebox.showinfo("Info", "The bot has stopped playing")
        end_game()
        return
    tiles += bot_hand
    random.shuffle(tiles)
    messagebox.showinfo("Info", f"The bot exchanged its letters")
    bot_hand = []
    bot_hand = getTile(amount=7)
    messagebox.showinfo("Info", "The bot exchanged tiles.")

def react(dif=[1]):
    global bot_score, bot_hand, first_move
    if bot_end:
        return
    played = False
    bh_str = ''.join(bot_hand)
    w_list = []
    for w in DATA['']:
        if getDif(w, bh_str) in dif:
            w_list.append(w)
    if first_move:
        d = {0: '>', 1: 'v'}[random.randint(0, 1)]
        best_score = 0
        best_word = ''
        real_place_at = [7, 7]
        for w in w_list:
            check_all = list(range(1 - len(w), 1))
            for p in check_all:
                place_at = [7, 7]
                if d == '>':
                    place_at[1] += p
                else:
                    place_at[0] += p
                word_score = placeTile(place_at, bot_hand, w, direction=d, bypass=True, hypothetical=True)
                equal = word_score == best_score and random.randint(0, 1) == 0
                if word_score > best_score or equal:
                    best_score = word_score
                    best_word = w
                    real_place_at = place_at.copy()
        played = True
        first_move = False
        if best_word == '':
            bot_exchange()
            return
        word_score = placeTile(real_place_at, bot_hand, best_word, direction=d, bypass=True)
        bot_score += word_score
    else:
        missing = {}
        word_scores = {}
        for w in w_list:
            for l in getDif(w, bh_str, get_chars=True):
                if l not in missing:
                    missing[l] = []
                missing[l].append(w)
            word_scores[w] = {'direction': '>', 'score': 0, 'location': [0, 0], 'word': w}
        for y in range(15):
            for x in range(15):
                if board[y][x].startswith(" "):
                    l = board[y][x][-1]
                    if l in missing:
                        for w in missing[l]:
                            l_loc = 0
                            for z in range(w.count(l)):
                                l_loc = w.find(l, l_loc)
                                for d in ['>', 'V']:
                                    y_, x_ = 0, 0
                                    if d == '>':
                                        x_ = l_loc
                                    else:
                                        y_ = l_loc
                                    pos = [y - y_, x - x_]
                                    sc = placeTile(pos, bot_hand, w, direction=d, hypothetical=True)
                                    if type(sc) is not str:
                                        if sc > word_scores[w]['score']:
                                            word_scores[w]['score'] = sc
                                            word_scores[w]['location'] = pos
                                            word_scores[w]['direction'] = d
                                l_loc += 1
        played = True
        word_scores = sorted(list(word_scores.values()), key=lambda x: x['score'], reverse=True)
        if len(word_scores) == 0:
            bot_exchange()
            return
        best_word = word_scores[0]
        word_score = placeTile(best_word['location'], bot_hand, best_word['word'], direction=best_word['direction'])
        bot_score += word_score
    if played:
        bot_hand += getTile(amount=7 - len(bot_hand))

def regular_bot_move():
    if bot_end:
       return
    if first_move:
        react(dif=list(range(0, bot_hand.count("-") + 1)))
    else:
        react(dif=list(range(1, bot_hand.count("-") + 2)))

def cmd_len(cmd, length, err=''):
    if len(cmd) < length:
        if err:
                messagebox.showwarning("Error", err)
        return False
    return True

def end_game():
    global bot_score, player_score, player_hand, bot_hand
    if bot_end and user_end:
        minused = 0
        for tile in bot_hand:
            minused += scores[tile]
            bot_score -= scores[tile]
        for tile in player_hand:
            minused += scores[tile]
            player_score -= scores[tile]
        if len(bot_hand) == 0:
            bot_score += minused
        if len(player_hand) == 0:
            player_score += minused
        winner = "Bot"
        if player_score > bot_score:
            winner = "Player"
        elif player_score == bot_score:
            winner = "Draw"
        while True:
            os.system("CLS")
            print(" The game has ended")
            print(f" Winner:       {winner}")
            print(f" Player Score: {player_score}")
            print(f" Bot Score:    {bot_score}")
            input(" >> ")

turn = 0
bot_score = 0
player_score = 0
os.system('cls')
while True:
    bot_hand = sorted(getTile(amount=7))
    player_hand = sorted(getTile(amount=7))
    if (bot_hand[0] != player_hand[0]):
        if sorted([bot_hand[0], player_hand[0]])[0] == bot_hand[0]:
            regular_bot_move()
        break
while True:
    os.system('cls')
    display()
    show_hand = ' '
    for tile_id, tile in enumerate(player_hand):
        if tile_id != 0:
            show_hand += ' | '
        show_hand += f'{tile} x{scores[tile]}'
    print(f'{colors["--"]}')
    print(f' Bot score: {bot_score}')
    print(f' Your score: {player_score}')
    print(f' Tiles in Bag: {len(tiles)}')
    print(' Your hand:')
    print(show_hand)
    answer = input(" >> ")
    cmd = answer.split(' ')
    if user_end:
        regular_bot_move()
        continue
    match cmd[0]:
        case "p" | "play":
            if not cmd_len(cmd, 3, 'Command too Short'):
                continue
            move = cmd[1].upper()
            square_letter = move[0:1]
            square_digit = move[1:-1]
            direction = move[-1]
            if not square_digit.isdigit() or square_letter not in letters:
                messagebox.showwarning("Error", "Invalid square")
                continue
            square = [int(square_digit) - 1, letters.index(square_letter)]
            word = cmd[2].upper()
            if first_move:
                word_range = [list(range(square[0], square[0] + len(word))), list(range(square[1], square[1] + len(word)))]
                if 7 not in word_range[0] or 7 not in word_range[1]:
                    messagebox.showwarning("Error", "The first word must interact with the center square")
                    continue
            if word not in DATA['']:
                messagebox.showwarning("Error", "Invalid word")
                continue
            add_score = placeTile(square, player_hand, word, direction=direction, bypass=first_move)
            if type(add_score) is str:
                messagebox.showwarning("Error", add_score)
                continue
            player_score += add_score
            player_hand += getTile(amount=7 - len(player_hand))
            first_move = False
            regular_bot_move()
        case "s" | "skip" | "ps" | "pass":
            regular_bot_move()
        case "ex" | "exchange" | "rp" | "replace" | "t" | "trade":
            if not cmd_len(cmd, 2, 'Command too Short'):
                continue
            characters = cmd[1::]
            if 7 > len(tiles):
                messagebox.showwarning("Error", "There are fewer than 7 tiles left.")
                continue
            for c in range(len(characters)):
                characters[c] = characters[c].upper()
                char = characters[c]
                if char not in letters or char not in player_hand:
                    messagebox.showwarning("Error", f"Invalid tile ({char}) found")
                    continue
            for c in characters:
                player_hand.remove(c)
                player_hand += getTile()
            random.shuffle(tiles)
            regular_bot_move()
        case "end":
            if len(tiles) >= 7:
                messagebox.showwarning("Warning", "There are too many tiles left in the bag")
                continue
            user_end = True
            regular_bot_move()
            end_game()
            
