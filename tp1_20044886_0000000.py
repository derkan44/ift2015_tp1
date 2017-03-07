import sys


class Game:
    def __init__(self,jeu):
        self._jeu = jeu

    def winner(self):
        # 0 partie non terminee
        # 1 x gagnant
        # 2 o gagnant
        # 3 partie nulle
        winners = [[0,1,2], [3,4,5], [6,7,8],
                   [0,3,6], [1,4,7], [2,5,8],
                   [0,4,8], [2,4,6]]
        win = 0
        cases_vides = 0
        nulle = 3  # code pour partie nulle

        for i in range(0, 9):
            valeur = self._jeu >> ((8 - i) << 1) & 3
            if valeur == 0:
                cases_vides += 1

        for winning_case in winners:  # check if x wins
            count = 0
            for j in winning_case:
                valeur = self._jeu >> ((8 - j) << 1) & 3
                if valeur == 1:
                    count += 1
                if count == 3:
                    win = 1
                    return win

        for winning_case in winners:  # check if o wins
            count = 0
            for j in winning_case:
                valeur = self._jeu >> ((8 - j) << 1) & 3
                if valeur == 2:
                    count += 1
                if count == 3:
                    win = 2
                    return win

        return nulle if (cases_vides == 0 and win == 0) else win

"""
if __name__ == '__main__':

    r = range(45, 54)
    entier = 459329034283597291728327479273734123420780266358036
    t = 1
    for i in r:
        value = entier >> ((80 - i) << 1) & 3
        t = (t << 2) + value
        print(str(bin(t)))

    testGame = Game(t)
    print(testGame.winner())

"""


class MetaGame:
    def __init__(self, entier):
        self._entier = entier
        self._last = entier >> 162 & 127
        self._player = (entier >> ((80 - self._last) << 1) & 3) ^ 0b11 # XOR avec 0b11 pour inverser le player

    def get_entier(self):
        return self._entier

    def get_last(self):
        return self._last

    def get_player(self):
        return self._player

    def winner(self):
        q = 1
        for i in range(0, 9):
            r = range(0 + i*9, 9 + i*9)
            t = 1
            for j in r:
                value = self._entier >> ((80 - j) << 1) & 3
                t = (t << 2) + value
            tmpgame = Game(t)
            value = tmpgame.winner()  # test chaque sous partie pour un gagnant
            value = 0 if value == 3 else value
            q = (q << 2) + value

        # q devient un obj Game, test pour winner
        tmpgame = Game(q)
        return tmpgame.winner()

    def getInt(self,move):
        new_int = (self._player << ((80 - move) << 1)) + self._entier
        new_int &= 11692013098647223345629478661730264157247460343807  # remove 7 premiers bits avec un masque de 162bits
        new_int += move << 162  # padding de 0 et combinaison
        return new_int

    def possibleMoves(self):
        possible = []
        next_case = self._last % 9
        indice_deb = next_case * 9
        range_indice = range(indice_deb, indice_deb + 9)  # les coups possibles dans le petit tic tac toe
        t = 1

        for i in range_indice:
            value = self._entier >> ((80 - i) << 1) & 3
            t = (t << 2) + value  # construire un petit tic tac toe
            if value == 0:
                possible.append(i)  # garder les coups possibles en memoire

        tmpgame = Game(t)
        if tmpgame.winner() != 0:  # test s'il est possible de jouer dans le petit tic tac toe
            possible = []

        if not possible:  # on peut jouer dans un autre tic tac toe
            for i in range(0, 9):
                if i == next_case:  # skip celui qu'y vient d'etre analyser
                    continue
                r = range(0 + i * 9, 9 + i * 9)
                t = 1
                tmp_possible = []

                for j in r:
                    value = self._entier >> ((80 - j) << 1) & 3
                    t = (t << 2) + value
                    if value == 0:
                        tmp_possible.append(j)

                tmpgame = Game(t)
                winstate = tmpgame.winner()  # test chaque sous partie pour un gagnant
                if winstate == 0:  # la partie n'est pas fini, on peut y jouer
                    possible.extend(tmp_possible)
                else:
                    continue

        return possible

if __name__ == '__main__':

    entier = 459329034283597291728327479273734123420780266358036
    print(bin(entier))
    meta = MetaGame(entier)
    print(meta.possibleMoves())



class Node:
    def __init__(self,data):
        self._data = data
        self._children = []

    def add_child(self, obj):
        self._children.append(obj)


class GameTree:
    def __init__(self, root):
        self._root = root

    def __str__(self):
        return "tree"


# debut programme

#entier = sys.argv[0]

#METAGAME = MetaGame(entier)

