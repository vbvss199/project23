from copy import deepcopy

class Board:
    def __init__(self, board=None):
        # define players
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'

        # define board position
        self.position = {}

        # init (reset) board
        self.init_board()

        # create a copy of a previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    # init board method(initial state of the board)
    def init_board(self):
        # loop over all the rows
        for row in range(3):
            # over the columns as well
            for col in range(3):
                self.position[row, col] = self.empty_square

    # MAKE MOVE function
    # along with the self it takes coordinates in order to move to the next
    # first the column is defined then the row make sure of it
    def make_move(self, row, col, player):
        # creating a new board instance inherits from the current state board
        # so newly generated also contains the previous one as well
        board = Board(self)

        # make move now
        # player alternately changes the board position icon 'x' or 'o'
        board.position[row, col] = player

        return board

    # game is drawn or not
    def is_draw(self):
        # loop over board squares
        for (row, col), value in self.position.items():
            # if empty square is available
            if value == self.empty_square:
                # this is not a draw
                return False
        # by default return True
        return True

    # get whether the game is won or not
    def is_win(self, player):
        # define a series of sequences which say as win

        # one is vertical sequence detection
        # loop over board columns
        for col in range(3):
            # loop over board rows
            winning_sequence = [(row, col) for row in range(3) if self.position[row, col] == player]
            if len(winning_sequence) == 3:
                return True

        # other is 1st DIAGONAL sequence detection
        winning_sequence = [(row, row) for row in range(3) if self.position[row, row] == player]
        if len(winning_sequence) == 3:
            return True

        # other is 2nd DIAGONAL sequence detection
        winning_sequence = [(row, 2 - row) for row in range(3) if self.position[row, 2 - row] == player]
        if len(winning_sequence) == 3:
            return True

        # other is horizontal sequence detection
        # loop over board rows
        for row in range(3):
            # loop over board columns
            winning_sequence = [(row, col) for col in range(3) if self.position[row, col] == player]
            if len(winning_sequence) == 3:
                return True

        # by default return a non-winning state
        return False

    # generate appropriate moves to play in the current position
    def generate_states(self, player):
        # define state lists(move list -list of available actions to consider )
        # list of board class instances where every single instance had an adjusted position
        actions = []
        # loop over board rows
        for row in range(3):
            # loop over columns
            for col in range(3):
                # make sure that the current square is empty
                if self.position[row, col] == self.empty_square:
                    # append available action /board state to action list
                    actions.append(self.make_move(row, col, player))
        # return the list of available actions(these are actually board class instances)
        # from the monte carlo perspective, it is to be the set of actions available, but here it is available board class instance
        return actions

    # main game loop
    def game_loop(self):
        print('\ntic tac toe game\n')
        print('Type exit to quit the game\n')
        print('Player 1 (x) is a human player. Player 2 (o) is controlled by AI.\n')
        # print board
        print(self)

        # create minimax_alpha_beta instance
        minimax_ab = MinimaxAlphaBeta(max_depth=3)

        # game loop
        while True:
            # take user input for player 1
            user_input = input('Player 1 (x) Move: ')
            if user_input == 'exit':
                break
            # skip empty input
            if user_input == '':
                continue

            try:
                # format user input move column first then row [col, row] eg [1, 2]
                row = int(user_input.split(',')[-1]) - 1
                # minus one is done to ensure that the board runs from 0 to 2 not 1 to 3
                col = int(user_input.split(',')[0]) - 1

                # check legality
                if self.position[row, col] != self.empty_square:
                    print('Illegal move')
                    continue

                # make move on the board for player 1
                self = self.make_move(row, col, self.player_1)

                # print board
                print(self)

                # check if player 1 has won
                if self.is_win(self.player_1):
                    print('Player 1 (x) has won the game!')
                    break
                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!')
                    break

                # make move for player 2 (AI)
                best_move = minimax_ab.get_best_move(self)
                self.position = best_move.position

                # print board
                print(self)

                # check if player 2 has won
                if self.is_win(self.player_2):
                    print('Player 2 (o) has won the game!')
                    break
                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!')
                    break

            except Exception as e:
                print('Error', e)
                print('Illegal move')
                print('Move format [x, y]: 1, 2 where 1 is column and 2 is row')


    #print board state
    #every time we do print(board it will call the default str method here )
    def __str__(self):
        board_str=''
        for row in range(3):
            for col in range(3):
                board_str+= ' %s '  % self.position[row,col]
            #define board string in the beggining of this method in to get a 3*3 representation

            #print new line every time it reaches the ending of row 
            board_str+='\n'

        #prepending the side to move
        if self.player_1=='x':
            board_str='\n----------\n"x" to move\n----------\n'+ board_str
        
        elif self.player_1=='o':
            board_str='\n----------\n"o" to move\n----------\n'+ board_str


        #return str in the line and make sure it is outside the loop to get 3*3 column else will end up with getting a 1*1 matrix
        return board_str


class MinimaxAlphaBeta:
    def __init__(self, max_depth=5, player_1='x', player_2='o'):
        self.max_depth = max_depth
        self.player_1 = player_1
        self.player_2 = player_2

    def evaluate(self, board):
        # Count 'x' and 'o' symbols and return the difference
        count_x = sum(1 for (row, col), value in board.position.items() if value == self.player_1)
        count_o = sum(1 for (row, col), value in board.position.items() if value == self.player_2)
        return count_x - count_o

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_win(self.player_1) or board.is_win(self.player_2) or board.is_draw():
            return self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            for child in board.generate_states(self.player_2):
                eval = self.minimax_alpha_beta(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for child in board.generate_states(self.player_1):
                eval = self.minimax_alpha_beta(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def get_best_move(self, board):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for child in board.generate_states(self.player_2):
            eval = self.minimax_alpha_beta(child, self.max_depth, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = child
            alpha = max(alpha, eval)

        return best_move


# main driver of the code
if __name__ == '__main__':
    # create board instance
    board = Board()
    board.game_loop()
