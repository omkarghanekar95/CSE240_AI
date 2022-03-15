import numpy as np
import math
import random

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def is_player_winning(self, board):

        player = self.player_number
        # Check horizontal locations for win
        rows = board.shape[0]
        columns = board.shape[1]
        for c in range(columns-3):
            for r in range(rows):
                if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                    return True

        # Check vertical locations for win
        for c in range(columns):
            for r in range(rows-3):
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                    return True

        # Check positively sloped diagonals
        for c in range(columns-3):
            for r in range(rows-3):
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                    return True

        # Check negatively sloped diagonals
        for c in range(columns-3):
            for r in range(3, rows):
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                    return True

    def get_next_open_row(self, board, col):
        rows = board.shape[0]
        # print('in get_next_open_row, rows', rows, col )
        for r in range(rows-1,-1,-1):
            if board[r][col] == 0:
                return r

    def is_terminal_node(self, board):
        return self.is_player_winning(board) or len(self.get_valid_locations(board)) == 0

    def get_valid_locations(self, board):
        # print('in valid locations', board)

        columns = board.shape[1]
        valid_columns = []
        for col in range(columns):
            if self.get_next_open_row(board, col): 
                valid_columns.append(col)
        return valid_columns

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if is_terminal or depth ==0 :
            node_score = self.evaluation_function(board)
            # print('node score is ', board, node_score)
            return (None, node_score)
            
        if maximizingPlayer:                # Maximizing player
            value = -1000001
            column = 0
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                
                b_copy = board.copy()
                b_copy[row][col] = self.player_number

                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            #print('in maximizing minimax', column, value)
            return column, value

        else:                               # Minimizing player
            value = 1000001
            column = 0
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                
                b_copy = board.copy()
                b_copy[row][col] = self.player_number
                
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            #print('in minimizing minimax', column, value)
            return column, value


    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        #col, val = self.minimax(board, 5, -float("inf"), float("inf"), True)
        col, score = self.minimax(board, 1, -1000001, 1000001, True)          # board, depth, alpha, beta, maximizing
        
        print('minimax score is', score, col)
        # print()
        # print()
        return col
        raise NotImplementedError('Whoops I don\'t know what to do')


    def expectimax(self, board, depth, is_max):
        value, column = -1000000, 0
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        
        if is_terminal or depth ==0 :
            node_score = self.evaluation_function(board)
            print('node score is ', board, node_score)
            return (None, node_score)

        if is_max:                                  # Maximizing player
            
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                
                b_copy = board.copy()
                b_copy[row][col] = self.player_number

                new_score = self.expectimax(b_copy, depth-1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            #print('in maximizing expectimax', column, value)
            return column, value

        else:                                       # Expectimax player

            number_of_moves = len(valid_locations)
            print ('number of moves', number_of_moves)
            expectedValue = 0
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                
                b_copy = board.copy()
                b_copy[row][col] = self.player_number
                
                new_score = self.expectimax(b_copy, depth-1, True)[1]
                probable_score = new_score/number_of_moves
                if new_score > value:
                    value = new_score
                    column = col

            #print('in expectimax', column, value)
        return column, value

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        col, score = self.expectimax(board, 8, True)
        print('expectimax score is', score, col)
        return col
        
        raise NotImplementedError('Whoops I don\'t know what to do')


    def evaluate_window(self, window, piece):
        score = 0
        empty_cells =0
        opp_piece = 1
        if opp_piece == piece:
            opp_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(empty_cells) == 1:
            score += 30
        elif window.count(piece) == 2 and window.count(empty_cells) == 2:
            score += 15

        if window.count(opp_piece) == 3 and window.count(empty_cells) == 1:
            score -= 200

        return score

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        
        window_size = 4
        rows, columns = board.shape[0], board.shape[1]
        score = 0
        
        ## Score center column
        center_array = [int(i) for i in list(board[:, columns//2])]
        center_count = center_array.count(self.player_number)
        score += center_count * 3

        ## Score Horizontal
        for r in range(rows):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(columns-3):
                window = row_array[c:c+window_size]
                score += self.evaluate_window(window, self.player_number)

        ## Score Vertical
        for c in range(columns):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(rows-3):
                window = col_array[r:r+window_size]
                score += self.evaluate_window(window, self.player_number)

        ## Score posiive sloped diagonal
        for r in range(rows-3):
            for c in range(columns-3):
                window = [board[r+i][c+i] for i in range(window_size)]
                score += self.evaluate_window(window, self.player_number)

        for r in range(rows-3):
            for c in range(columns-3):
                window = [board[r+3-i][c+i] for i in range(window_size)]
                score += self.evaluate_window(window, self.player_number)

        return score


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

