#from tkinter import *
import math
import search_algorithms as sa
import time

# master = Tk()

# class GUI(object):

# 	def __init__(self, state):
# 		self.canvas = Canvas(master, width = 96, height=96)
# 		self.canvas.pack()
# 		self.state = state

# 		for row in range(len(self.state)):
# 			for column in range(len(self.state[row])):
# 				self.canvas.create_rectangle((column * 32), (row * 32), ((column + 1) * 32), ((row + 1) * 32), fill="grey")
# 				self.canvas.create_text((column * 32) + 16, (row * 32) + 16, text=str(state[row][column]))

# 		self.SolutionNum = Label(text = "0")
# 		self.SolutionNum.pack(side = "right")

# 		self.SolutionLabel = Label(text = "Solution:")
# 		self.SolutionLabel.pack(side = "left")

# 		#self.ExpandedLabel = Label(text = "States Expanded:")
# 		#self.ExpandedLabel.pack(side = "left")

# 	def run():
# 		master.mainloop()

	#def solveBFS()
		
#Easy test case
test_state_easy = ((1, 4, 2),
              (0, 5, 8), 
              (3, 6, 7))  

#More difficult test case
test_state_hard = ((7, 2, 4),
              (5, 0, 6), 
              (8, 3, 1))  

#Potentially even harder test case
test_state_reversed = ((8,7,6),
                       (5,4,3),
                       (2,1,0))

current_test_state = test_state_hard

#mainApp = GUI(current_test_state)

#GUI.run()

def PrintSearch():
	print(sa.state_to_string(current_test_state))
	print()

	print("====BFS====")
	startBFS = time.time()
	solution_BFS, states_expanded_BFS, max_frontier_BFS = sa.bfs(current_test_state) #
	#print_result(solution_BFS, states_expanded_BFS, max_frontier_BFS)
	endBFS = time.time()
	if solution_BFS is not None:
	    sa.print_actions(solution_BFS, current_test_state)
	#print("Total time: {0:.3f}s".format(endBFS-startBFS))
	#print(best_first(current_test_state))

	print() 
	print("====DFS====") 
	startDFS = time.time()
	solution_DFS, states_expanded_DFS, max_frontier_DFS = sa.dfs(current_test_state)
	endDFS = time.time()
	#print_result(solution_DFS, states_expandedDFS, max_frontier_DFS)
	#print_actions(solution_DFS, current_test_state)
	#print("Total time: {0:.3f}s".format(endDFS-startDFS))

	print() 
	print("====Greedy Best-First (Misplaced Tiles Heuristic)====") 
	startBF = time.time()
	solution_best_first, states_expanded_best_first, max_frontier_best_first = sa.best_first(current_test_state)
	endBF = time.time()
	sa.print_result(solution_best_first, states_expanded_best_first, max_frontier_best_first)
	#sa.print_actions(solution_best_first, current_test_state)

	print() 
	print("====A* (Misplaced Tiles Heuristic)====") 
	start_astar = time.time()
	solution_astar, states_expanded_astar, max_frontier_astar = sa.astar(current_test_state)
	end_astar = time.time()
	#sa.print_actions(solution_astar, current_test_state)

	print()
	print("====Final Results For BFS, DFS, Greedy Best-First(Misplaced Tile Heuristic), and A*(Misplaced Tile Heuristic)====")
	sa.print_result(solution_BFS, states_expanded_BFS, max_frontier_BFS)
	print()
	sa.print_result(solution_DFS,states_expanded_DFS,max_frontier_DFS)
	print()
	sa.print_result(solution_best_first,states_expanded_best_first,max_frontier_DFS)
	print()
	sa.print_result(solution_astar, states_expanded_astar, max_frontier_astar)
	print()
	print("Total time for BFS: {0:.3f}s".format(endBFS-startBFS))
	print("Total time for DFS: {0:.3f}s".format(endDFS-startDFS))
	print("Total time for Greedy Best-First: {0:.3f}s".format(endBF-startBF))
	print("Total time for A*: {0:.3f}s".format(end_astar-start_astar))

if __name__ == "__main__":
	PrintSearch()