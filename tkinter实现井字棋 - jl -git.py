from tkinter import *
from tkinter.simpledialog import *

class tic_tac_toe(object):
	root = Tk()
	root.title('井字棋游戏')
	root.geometry('400x400') #设置初始化界面大小
	root.resizable(width = False, height = False) #界面不可拉伸
	def __init__(self):
		self.__board = list('012345678')
		self.__computerLetter = ''
		self.__playerLetter = ''
		self.__turn = ''
		self.__boardcopy = ()
		self.is_start = False

		self.header_bg = '#CDC0B0'
		self.board_bg = '#CDBA96'
		self.chess_color = self.board_bg
		self.label_color = "#2E8B57"
		self.b_font = ('黑体', 12, 'bold')
		self.row = 4 
		self.column = 4
		self.mesh = 80  #棋盘一格的宽度
		self.ratio = 0.9
		self.step = self.mesh / 2
		self.chess_r = self.step * 0.7

		self.f_header = Frame(self.root, bg =self.header_bg)
		self.f_header.pack(fill=BOTH ,ipadx =10)
		self.b_start = Button(self.f_header, text ='开始' , font =self.b_font, command = self.bf_startgame)
		self.b_restart = Button(self.f_header, text ='重来', font = self.b_font, state = DISABLED , command = self.bf_restart)
		self.l_info = Label(self.f_header, text='未开始', bg = self.header_bg, font=('楷体', 15, 'bold'), fg=self.label_color)
		self.b_lose = Button(self.f_header, text ='认输' , font = self.b_font, state = DISABLED, command =self.bf_lose)
		self.b_note = Button(self.f_header, text ='说明' , font = self.b_font, state = NORMAL , command = self.bf_note)

	
		self.b_start.pack(side = LEFT,padx = 20)
		self.b_restart.pack(side = LEFT)
		self.l_info.pack(side = LEFT ,fill = BOTH ,expand = YES,pady =10)
		self.b_note.pack(side = RIGHT,padx = 20)
		self.b_lose.pack(side = RIGHT)

	
		self.c_chess = Canvas(self.root, bg = self.board_bg, width=(self.column + 1) * self.mesh, height=(self.row + 1) * self.mesh)
		self.draw_board()
		self.c_chess.bind("<Button-1>", self.cf_board)
		self.c_chess.pack()

	
	def draw_line(self, x, y):	
		ratio = (1 - self.ratio) * 0.99 + 1  #绘画棋子时，棋盘的边界线会留有棋子的痕迹，设置ratio防止边界线受影响。
		center_x = self.mesh * (x + 1) #落棋的位置，即一格的中心
		center_y = self.mesh * (y + 1)
		self.c_chess.create_rectangle(center_y - self.step, center_x - self.step,center_y + self.step, center_x + self.step,fill=self.board_bg, outline=self.board_bg)
		a, b = [0, ratio] if y == 0 else [-ratio, 0] if y == self.row - 1 else [-ratio, ratio]
		c, d = [0, ratio] if x == 0 else [-ratio, 0] if x == self.column - 1 else [-ratio, ratio]
		self.c_chess.create_line(center_y + a * self.step, center_x, center_y + b * self.step, center_x)
		self.c_chess.create_line(center_y, center_x + c * self.step, center_y, center_x + d * self.step)

	
	def draw_board(self):
		for x in range(self.row):
			for y in range(self.column):
				self.draw_line(x, y)

	
	def draw_chess_player(self , x, y):
		center_x = self.mesh *(x+1.5)
		center_y = self.mesh *(y+1.5)
		self.c_chess.create_oval(center_y - self.chess_r, center_x - self.chess_r, center_y +self.chess_r, center_x +self.chess_r, fill = self.chess_color)

	
	def draw_cross_player(self, x, y ,cur_x , cur_y):
		center_x = self.mesh *(x+1.5)
		center_y = self.mesh *(y+1.5)
		if abs(cur_x - center_x) <22 and abs(cur_y - center_y) <22 :
			self.c_chess.create_line(center_y + self.step*0.6, center_x + self.step*0.6, center_y - self.step *0.6 , center_x - self.step *0.6)
			self.c_chess.create_line(center_y + self.step*0.6, center_x - self.step*0.6, center_y - self.step *0.6 , center_x + self.step *0.6)

	
	def draw_computer(self):
		if not self.is_start and not self.__turn == '电脑':
			return
		computer_move = self.move
		computer_coordinate = self.move_transferto_coordinate(computer_move)
		center_x = computer_coordinate[0]
		center_y = computer_coordinate[1]
		if self.__computerLetter == 'X':
			self.c_chess.create_line(center_y + self.step*0.6, center_x + self.step*0.6, center_y - self.step *0.6 , center_x - self.step *0.6)
			self.c_chess.create_line(center_y + self.step*0.6, center_x - self.step*0.6, center_y - self.step *0.6 , center_x + self.step *0.6)
		else:
			self.c_chess.create_oval(center_y - self.chess_r, center_x - self.chess_r, center_y +self.chess_r, center_x +self.chess_r, fill = self.chess_color)

	def legal_moves(self):
		moves = []
		for i in range(9):
			if self.__board[i] in list('012345678'):
				moves.append(i)
		return moves

	def get_computer_move(self):
		self.__boardcopy = self.__board.copy()
		for self.move in self.legal_moves():
			self.__boardcopy[self.move] = self.__computerLetter
			if self.is_winner():
				return self.move
			self.__boardcopy[self.move] = str(self.move)

		for self.move in self.legal_moves():
			self.__boardcopy[self.move] = self.__playerLetter
			if self.is_winner():
				return self.move
			self.__boardcopy[self.move] = str(self.move)

		for self.move in (4,0,2,6,8,1,3,5,7):
			if self.move in self.legal_moves():
				return self.move

	
	def move_transferto_coordinate(self , move_value):
		if move_value == 0:
			center_x ,center_y = self.step*3, self.step*3
		elif move_value == 1:
			center_x ,center_y = self.step*3, self.step*5
		elif move_value == 2:
			center_x ,center_y = self.step*3, self.step*7
		elif move_value == 3:
			center_x ,center_y = self.step*5, self.step*3
		elif move_value == 4:
			center_x ,center_y = self.step*5, self.step*5		
		elif move_value == 5:
			center_x ,center_y = self.step*5, self.step*7
		elif move_value == 6:
			center_x ,center_y = self.step*7, self.step*3
		elif move_value == 7:
			center_x ,center_y = self.step*7, self.step*5
		else:
			center_x ,center_y = self.step*7, self.step*7
		return center_x,center_y

	
	def set_btn_state(self, state):
		if state == "init":
			state_list = [NORMAL, DISABLED, DISABLED, NORMAL] 
		else:
			state_list =[DISABLED, NORMAL, NORMAL, NORMAL]
		self.b_start.config(state=state_list[0])
		self.b_restart.config(state=state_list[1])
		self.b_lose.config(state=state_list[2])
		self.b_note.config(state=state_list[3])
			
	
	def bf_start_chose_character(self):
		choice = askstring('游戏角色','请选择您的角色：X 或 O （默认为O）')
		if choice in ('X' , 'x'):
			self.__turn = '玩家'
			self.__playerLetter = 'X'
			self.__computerLetter ='O'
		else:
			self.__turn = '电脑'
			self.__computerLetter = 'X'
			self.__playerLetter ='O'
		return ("%s为先手" % self.__turn)

	
	def bf_startgame(self):
		self.is_start = True
		text = self.bf_start_chose_character()
		self.l_info.config(text = text)
		self.set_btn_state("start")
		if self.__turn =='电脑':
			self.computer_turn()


	def bf_lose(self):
		self.set_btn_state('init')
		self.is_start = False
		text = "玩家认输"
		self.l_info.config(text = text)
		messagebox.showinfo('游戏结果','玩家认输')
		self.bf_restart()

	def bf_restart(self):
		self.set_btn_state('init')
		text = "游戏结束"
		self.l_info.config(text = text)
		self.draw_board()
		self.__board = ['0','1','2','3','4','5','6','7','8']
	

	def bf_note(self):
		messagebox.showinfo('游戏说明',' \n\t 1、游戏棋盘为 3 X 3 的九宫格，玩家点击相应格子下棋。\n\t 2、游戏模式为人机模式。\n\t 3、玩家可以选择X或O两种角色(X为先手）。\n\t 4、首先实现横线、竖线、斜线连续三个格子一样的一方获胜。')


	def cf_board(self ,e):
		#/----------------姜来 2020.5.5------------------/#
		self.draw_board()
		"""计算鼠标点击时的坐标"""
		cur_x , cur_y = e.y ,e.x
		if self.mesh <= e.y <self.mesh*2:
			x = 0
		elif self.mesh *2 <= e.y <self.mesh *3:
			x = 1
		elif self.mesh *3 <= e.y <self.mesh *4:
			x = 2
		else:
			x = 100 #超出棋盘范围

		if self.mesh<= e.x <self.mesh*2:
			y = 0
		elif self.mesh *2<= e.x <self.mesh *3:
			y = 1
		elif self.mesh *3 <= e.x <self.mesh *4:
			y = 2
		else:
			y = 100 #超出棋盘范围


		if x == 0 and y == 0:
			move = 0
		elif x == 0 and y == 1:
			move = 1
		elif x == 0 and y == 2:
			move = 2
		elif x == 1 and y == 0:
			move = 3
		elif x == 1 and y == 1:
			move = 4
		elif x == 1 and y == 2:
			move = 5
		elif x == 2 and y == 0:
			move = 6
		elif x == 2 and y == 1:
			move = 7
		elif x == 2 and y == 2:
			move = 8
		else:
			move = 100

		if move in self.legal_moves():
			if not self.is_start and not self.__turn == '玩家':
				return
			if self.__playerLetter == 'X':
				self.draw_cross_player(x , y , cur_x , cur_y)
			else:
				self.draw_chess_player(x, y)
			self.move = move
			self.player_turn()
		else:
			self.bf_restart()
			if x == 100 or y == 100:
				messagebox.showinfo('提示','超出棋盘范围，请重新开始')
			else:
				messagebox.showinfo('提示','该位置已有棋子，请重新开始')
			self.bf_restart()

	def is_winner(self):
		win = {(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)}
		for r in win:
			if self.__boardcopy[r[0]]==self.__boardcopy[r[1]]==self.__boardcopy[r[2]]:
				return True
		return False

	def is_tie(self):
		for i in list("012345678"):
			if i in self.__board:
				return False
		return True

	def reshow_board(self):
		for i in range(9):
			if self.__board[i] == 'X':
				i_coordinate = self.move_transferto_coordinate(i)
				center_x = i_coordinate[0]
				center_y = i_coordinate[1]
				self.c_chess.create_line(center_y + self.step*0.6, center_x + self.step*0.6, center_y - self.step *0.6 , center_x - self.step *0.6)
				self.c_chess.create_line(center_y + self.step*0.6, center_x - self.step*0.6, center_y - self.step *0.6 , center_x + self.step *0.6)

			if self.__board[i] == 'O':
				i_coordinate = self.move_transferto_coordinate(i)
				center_x = i_coordinate[0]
				center_y = i_coordinate[1]
	
				self.c_chess.create_oval(center_y - self.chess_r, center_x - self.chess_r, center_y +self.chess_r, center_x +self.chess_r, fill = self.chess_color)

	def player_turn(self):
		text = "正在游戏"
		self.l_info.config(text = text)
		self.__board[self.move] = self.__playerLetter
		self.__boardcopy = self.__board
		self.reshow_board()
		if self.is_winner():
			messagebox.showinfo('游戏结果','玩家获胜！')
			text = "游戏结束"
			self.l_info.config(text = text)
			self.bf_restart()
		else:
			self.__turn = '电脑'		
		if self.is_tie():
			messagebox.showinfo('游戏结果','平局')
			text = "游戏结束"
			self.l_info.config(text = text)
			self.bf_restart()
		elif not self.is_winner():
			self.computer_turn()

	def computer_turn(self):
		self.move = self.get_computer_move()
		self.__board[self.move] = self.__computerLetter
		self.__boardcopy = self.__board
		self.reshow_board()
		self.draw_computer()
		if self.is_winner():
			messagebox.showinfo('游戏结果','计算机获胜！')
			text = "游戏结束"
			self.l_info.config(text = text)
			self.bf_restart()
		if self.is_tie():
			messagebox.showinfo('游戏结果','平局')
			text = "游戏结束"
			self.l_info.config(text = text)
			self.bf_restart()
		else:
			self.__turn = '玩家'	

def main():
	play_game = tic_tac_toe()
	mainloop()

if __name__ == '__main__':
	main()
