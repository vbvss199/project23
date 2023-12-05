from copy import deepcopy
from sys import exception
from tkinter import NO
from mcts import *

class Board():
    def __init__(self, board=None):

        # define players
        self.player_1= 'x'
        self.player_2 = 'o'
        self.empty_square = '.'
        
        # define board position
        self.position = {}
        
        # init (reset) board
        self.init_board()
        
        # create a copy of a previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    #init board method(initial state of the board)
    def init_board(self):
        #loop over all the rows 
        for row in range(3):
            #over the columns as well
            for col in range(3):
                self.position[row,col]=self.empty_square
    
    #MAKE MOVE function 
    #along with the self it takes cordinates in order to move to the next 
    #first the column is defined then the row make sure of it
    def make_move(self,row,col):
        #creating a new board instance inherits from the current state board
        #so newly generated also contains the previous one as well
        board=Board(self)

        #make move now
        #first time x and then o alterante changing of board position icon x or o
        board.position[row,col]=self.player_1

        #then swap players
        (board.player_1,board.player_2)=(board.player_2,board.player_1)

        #return new board state
        return board
    
    #game is drawn or not 
    def is_draw(self):
        #loop over board squares
        for row,col in self.position:
            #if empty dquare is available
            if self.position[row,col]==self.empty_square:
                #this is not a draw 
                return False
        #by default return True
        return True
    
    #get whether the game is win or not

    def is_win(self):
        #define a series of sequences which say as win

        ###################################
        #one is vertical sequence detection
        #loop over board columns
        for col in range(3):
            #define winning sequence list
            winning_sequence=[]
            #loop over board rows
            for row in range(3):
                #if found same next element in the row 
                if( self.position[row,col]==self.player_2):
                    #update winning sequence
                    #only length of winning sequence matters at last doesnt matter what u append
                    winning_sequence.append((row,col))
                #if we have 3 elements in the column
                if(len(winning_sequence)==3):
                    return True
        ###################################



        ########################################
        #other is 1st DIAGONAL sequence detection
        #define winning sequence list
            winning_sequence=[]
            #loop over board rows
            for row in range(3):
                #initialise column
                col=row
                #if found same next element in the row 
                if( self.position[row,col]==self.player_2):
                    #update winning sequence
                    #only length of winning sequence matters at last doesnt matter what u append
                    winning_sequence.append((row,col))
                #if we have 3 elements in the column
                if(len(winning_sequence)==3):
                    return True
 
        #########################################

        ########################################
        #other is 2nd DIAGONAL sequence detection
        #define winning sequence list
            winning_sequence=[]
            #loop over board rows
            for row in range(3):
                #initialise column
                col=3-row-1
                #if found same next element in the row 
                if( self.position[row,col]==self.player_2):
                    #update winning sequence
                    #only length of winning sequence matters at last doesnt matter what u append
                    winning_sequence.append((row,col))
                #if we have 3 elements in the column
                if(len(winning_sequence)==3):
                    return True
 
        #########################################


        ########################################
        #other is horizantal sequence detection
        #loop over board columns
        for row in range(3):
            #define winning sequence list
            winning_sequence=[]
            #loop over board rows
            for col in range(3):
               #if found same next element in the row 
                if( self.position[row,col]==self.player_2):
                    #update winning sequence
                    #only length of winning sequence matters at last doesnt matter what u append
                    winning_sequence.append((row,col))
                #if we have 3 elements in the column
                if(len(winning_sequence)==3):
                    return True

        #########################################

        #by default return a non winning state 
        return False
    

    #generate appropriate moves to play in the current position
    def generate_states(self):
        #define state lists(move list -list of available actions to consider )
        #list of board class instances where every single instance had an adjusted position
        actions=[]
        #loop over board rows
        for row in range(3):
            #loop over columns
            for col in range(3):
                #make sure that current square is empty
                if(self.position[row,col]==self.empty_square):
                    #append available action /board state to action list
                    actions.append(self.make_move(row,col))
        #return the list of available actions(these are actually board class instances)
        #from monti carlo perspective it is to be the set of actions availble but here it is available board class instance
        return actions
    

    #main game loop
    def game_loop(self):
        print('\ntic tac toe game\n')
        print('Type exit to quit the game\n')
        print('enter the move like:1,1 where the format is [column][row] or [x][y] cordinates\n')
        #print board
        print(self)

        #create monte carlo search tee instance 
        mcts=MCTS()

        #game loop
        while True:
            # take user input
            user_input=input('>')
            if user_input=='exit':break

            #skip empty input
            if user_input=='':continue

            try:
              #format user input move column first then row [col,row] eg [1,2]
              row=int(user_input.split(',')[-1])-1
              #minus one id done to ensure that as the board runs from 0 to 2 not 1 to 3
              col=int(user_input.split(',')[0])-1

              #check legality
              if self.position[row,col]!= self.empty_square:
                  print('illegal move')
                  continue
                  

              #print(row,col)
              #print(user_input.split(','))

              #make move on board
              self=self.make_move(row,col)

              #search for the best move
              best_move=mcts.search(self)

              ##############################
              #make AI agent move now!!!!!!!!!!!!!
              try:
                  self=best_move.board
              except Exception as e:
                  print('error',e)
              ##############################

              #print board
              print(self)

              #check the game is won
              if self.is_win():
                  print('player "%s" : has won the game ' %self.player_2)
                  break
              #check the game is drawn
              elif self.is_draw():
                  print('game is drawn')
                  break

            except Exception as e:
                print('Error',e)
                print('illegal move')
                print('Move format [x,y]:1,2 where 1 is column and 2 is row')




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


#main driver of the code
if __name__=='__main__':
    #create board instance
    board=Board()
    board.game_loop()
    # #create MCTS instance
    # mcts=MCTS()

    # #loop to play the game AI vs AI
    # while True:
    #     #find the best move 
    #     best_move=mcts.search(board)

    #     #make the best move on board
    #     board=best_move.board

    #     print(board)

    #     input()

    #enable board loop and start AI vs human

    
    
    
    
    #start game loop
    #board.game_loop

    #create MCTS instance
    #mcts=MCTS()
    # #simualte random game
    # score=mcts.rollout(board)

    # #print game result
    # print('Score',score)

    # #start game loop






    #initialise the root node
    # root=TreeNode(board,None)
    # root.visits=6
    # root.score=12

    # #init move1
    # move_1=TreeNode(board.generate_states()[0],root)
    # move_1.visits=2
    # move_1.score=4

    # #init move2
    # move_2=TreeNode(board.generate_states()[0],root)
    # move_2.visits=4
    # move_2.score=8
    # print(move_2.__dict__)

    # #create couple of children nodes in order not to get error 
    # root.children={
    #     'child_1':move_1,
    #     'child_2':move_2

    # }

    # #create MCTS instance
    # mcts=MCTS()
    #call get best move assuming search is finished (exploration constant =0)
    #zero in the sense there's no exploration so ended for the exploration constant
    # best_move=mcts.get_best_move(root,0)
    # print(best_move.board)

    # #call get best move as human that search is going on (exploration constant is 2 which is better option)
    # best_move_search=mcts.get_best_move(root,2)
    # print(best_move_search.board)
    
    
    #print('initial board state')
    #print(board)

    #start game loop
    #board.game_loop()

    # #create treenode instnce
    # root=TreeNode(board,None)
    # #we get tree properties with no children create some children and start the expansion process
    # root.children['child1']=TreeNode(board.make_move(1,1),root)
    # print(root.__dict__)
    # print(root.children['child1'])


    #generate available actions
    # actions=board.generate_states()
    
    # #take action(make move on board) this is done by mcts algorithm
    # board=actions[0]

    #print updated board
    # print('generate available actions for after first move has been made')
    # actions=board.generate_states()
    # board=actions[0]
    # #single action
    # print(actions[0])

    #generate available actions after first move had been made
    #actions are nothing but available states 
    # actions=board.generate_states()
    # board=actions[3]
    # print(actions[3])

    #for looping over all the generated actions
    # for action in actions:
    #     print(action)
    




    #printing the intial state of the board
    # print(board)
    # print(board.__dict__)

    #define custom board
    # board.position={
    #     (0,0):'x',(0,1):'o',(0,2):'x',
    #     (1,0):'x',(1,1):'o',(1,2):'x',
    #     (2,0):'x',(2,1):'x',(2,2):'o',
    # }

    # #print the board
    # print(board.__dict__)
    #print('game Draw status:', board.is_draw())


    #if we wanna make move on board
    # board=board.make_move(2,2)

    #print the state of board after making move
    # print(board)
    # print(board.__dict__)

    # board1=Board(board)
    # print(board1)
    # print(board1.__dict__)
    # board1.player_1='o'
    # board1.player_2='x'
    # print('player_2: "%s"' % board1.player_2)

    # #distinguish between win and draw status
    # if board1.is_win():
    #     print('Game is won:', board1.is_win())
    # else:
    #     print('Game is draw:',board1.is_draw())




    #testing against the board position 
    #index starts from 0 so make sure of it
    #board.position[2,2]='x'
    #board.position[1,1]='o' 
    #board.position[0,0]='x' 
    #sending the exaxct board to the Board class we use
    # board1=Board(board)
    # print(board1)
    # print(board1.position)

