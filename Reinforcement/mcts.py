#mcts algorthm implementation 
#load packages 
import math
import random

#define tree node class definition
class TreeNode():
    #class constructor( create tree node class instance)
    def __init__(self,board,parent):
        #init associated board state
        self.board=board

        #init is node terminal flag

        #define node is terminal or not #flag either won or lost or drawn
        if self.board.is_win() or self.board.is_draw():
            #we have terminal node or game is over
            self.is_terminal=True
        #otherwise
        else:
           # we have non terminal node 
           self.is_terminal=False

        #init is fully expanded flag
        self.is_fully_expanded=self.is_terminal

        
        #init parent node is available
        self.parent=parent

        #initialize the number of node visits 
        self.visits=0

        #init the total score t over the node
        self.score=0

        #init current node's children
        self.children={}

#mont carlo tree search class definition
class MCTS():
    #search for the best move in the current position
    def search(self,initial_state):
        #create root node 
        self.root=TreeNode(initial_state,None)

        #selection simulation backpropogation phases

        #go through 1000 iterations 
        for iteration in range(1000):

            #select a node(selection phase)
            node=self.select(self.root)

            #again fully expanded vs non fully expanded node matters here

            #score current node(simulation phase)
            score=self.rollout(node.board)

            #backpropagate the number of visits as well as score
            self.backpropagate(node,score)

        #pick up the best move in the current position
        try:
            return self.get_best_move(self.root,0)
        
        except:
            pass
    
    #select the most promising node 
    def select (self,node):
        #make sure that we r doing with non terminal nodes
        while not node.is_terminal:
            #case when node is  fully expanded
            if node.is_fully_expanded:
                node=self.get_best_move(node,2)

            #case where node is not fully exapnded
            else:
                #otherwise expand the node
                return self.expand(node)
        #return node
        return node
    
    #expand node 
    def expand(self,node):
        #generate legal states or moves for the given node(parent)
        states=node.board.generate_states()

        #loop ove generated states(moves)
        for state in states:
            #make sure taht current state  (move) is not present in child nodes
            if str(state.position) not in node.children:
              #create a new node
              new_node=TreeNode(state,node)

              #add child node to parent's  node children list (actual it is doctionary)
              node.children[str(state.position)]=new_node

              #case when node is fully expanded or not
              if len(states)== len(node.children):
                  node.is_fully_expanded=True
              #return newly created node
              return new_node
        #debuugging
        print('should not get here')

    #simulate the game via making random moves until reach end of the game
    def rollout(self,board):
        #make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            #try to make a move 
            try:
               #no moves available
               board=random.choice(board.generate_states())
            except:
                #return a draw score 
                return 0
        # print(board)
    
        #return score from the player "x " perspective
        if board.player_2=='x': return 1
        elif board.player_2=='o':return -1 

    #backpropagate the number of visits and score up to the root node
    def backpropagate (self,node,score):
        #update node's up to root node
        while node is not None:

            #update node visits
            node.visits+=1

            #update node's score
            node.score+=score

            #set node to parent 
            node=node.parent


    #select the best node  basing on UCB1 or UCT formulae
    def get_best_move(self,node,exploration_constant):
        #uct is base don ucb formulae and exploration constant where it is given as constant parameter above ln(parentnode/childnode visits)
        #define best score and best move
        best_score=float('-inf')
        best_moves=[]
        #loop over child nodes
        for child_node in node.children.values():
            #define current player
            if child_node.board.player_2=='x':current_player=1
            if child_node.board.player_2=='o':current_player=-1

            #get move score using UCT formuale
            move_score=current_player*child_node.score /child_node.visits + exploration_constant * math.sqrt(math.log(node.visits/child_node.visits))
            # print('move_score:',move_score)

            #better move has been found
            if move_score>best_score:
                best_score=move_score
                best_moves=[child_node] 
            #found as good move as already available
            elif move_score==best_score:
                best_moves.append(child_node)
        #return one of the best moves randomly
        return random.choice(best_moves)










    



        



