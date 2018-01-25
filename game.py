from threading import Thread
import time

class Game(Thread):

	def init_board_and_nums(self):
		board=[0] * 64 
		nums=[0] * 4   #  len=4, signed 32-bit int
		for x in [0,2,4,6, 9,11,13,15, 16,18,20,22]:
			board[x]= 1
			if(x<32):
				nums[0]|=(1<<x)
			else:
				nums[1]|=(1<<(x-32))
		for x in [41,43,45,47, 48,50,52,54, 57,59,61,63]:
			board[x]= -1
			if(x<32):
				nums[2]|=(1<<x)
			else:
				nums[3]|=(1<<(x-32))
		return board, nums



	def __init__(self, currentPlayer, room):
		Thread.__init__(self)
		self.__currentPlayer=currentPlayer
		self.__board, self.__nums=self.init_board_and_nums()
		self.__room=room
		self.__json=None   # mocks input stream in java
		self.__response=None
		self.__isActive=True  # reserved for collecting finished game threads
		self.__isEnd=False


	def set_json(self, json):
		self.__json=json


	def get_current_player(self):
		return self.__currentPlayer
	

	def get_response(self):
		return self.__response


	def set_response(self, response):
		self.__response=response


	

	def run(self):
		while self.__isActive:
			print 'Game waiting for player!'
			while self.__currentPlayer and self.__currentPlayer.get_opponent() and self.__currentPlayer.is_active() and self.__currentPlayer.get_opponent().is_active():
				print 'Game starts!'
				while self.__json:
					print 'Game calculates!'
					print str(self.__json)
					if self.__json['command']=='click':
						self.__response=self.handle_move(self.__json['start'].split('_')[1],self.__json['end'].split('_')[1])
					elif self.__json['command']=='resume':
						nums_string=self.int_list_2_str_list_str(self.__nums)
						# check winner
						username=self.check_winner()
						# set command='click', instead of 'resume'
						self.__response='{"command":"click","action":"update","actionDetail":'+nums_string+',"winner":"'+username+'","currentPlayer":"'+self.__currentPlayer.get_username()+'"}'
					print '**return response',self.__response
					self.__json=None
				time.sleep(2)
			time.sleep(5)
		print 'Game is inactive!'

	

	# start and end are always within range			
	def handle_move(self, start, end):
		if self.__isEnd:
			return '{"command":"click","action":"none","actionDetail":["Game is over."],"winner":"__None__"}'

		start=int(start)
		end=int(end)
		direction_factor= 1 if self.__json['side']=='+' else -1
		# is your turn?
		if self.__currentPlayer.get_side()!=self.__json['side']:
			return '{"command":"click","action":"none","actionDetail":["Not your turn."],"winner":"__None__"}'
		# check points
		# start must be filled AND at my side
		if self.__board[start]!=(direction_factor):
			return '{"command":"click","action":"none","actionDetail":["Invalid start point."],"winner":"__None__"}'
		# end must be empty
		if self.__board[end]!=0:
			return '{"command":"click","action":"none","actionDetail":["Invalid end point."],"winner":"__None__"}'
		# check path
		start_row=start/8
		start_col=start%8
		end_row=end/8
		end_col=end%8
		# diagonal adjacent
		if (start_col>0 and end==(start_row+direction_factor)*8+(start_col-1)) or (start_col<7 and end==(start_row+direction_factor)*8+(start_col+1)):
			self.toggle_start_and_end(start, end, direction_factor) # nums and board
			nums_string=self.int_list_2_str_list_str(self.__nums)
			# check winner
			username=self.check_winner()
			# toggle currentPlayer
			self.__currentPlayer=self.__currentPlayer.get_opponent()
			return '{"command":"click","action":"update","actionDetail":'+nums_string+',"winner":"'+username+'","currentPlayer":"'+self.__currentPlayer.get_username()+'"}'
		# succesive diagonal skip
		res=self.dfs(start_row, start_col, end_row, end_col, [], direction_factor)
		if res[0]:
			self.toggle_start_and_end(start, end, direction_factor) # nums and board
			self.toggle_middles(res[1],direction_factor)
			nums_string=self.int_list_2_str_list_str(self.__nums)
			# check winner
			username=self.check_winner()
			# toggle currentPlayer
			self.__currentPlayer=self.__currentPlayer.get_opponent()
			return '{"command":"click","action":"update","actionDetail":'+nums_string+',"winner":"'+username+'","currentPlayer":"'+self.__currentPlayer.get_username()+'"}'
	
		return '{"command":"click","action":"none","actionDetail":["Invalid path."],"winner":"__None__"}'



	def toggle_start_and_end(self, start, end, direction_factor):
		# toggle/remove start
		if start<32:
			self.__nums[abs(direction_factor-1)]^=(1<<start) 
		else:
			self.__nums[abs(direction_factor-1)+1]^=(1<<(start-32))
		# toggle/add end
		if end<32:
			self.__nums[abs(direction_factor-1)]^=(1<<end) 
		else:
			self.__nums[abs(direction_factor-1)+1]^=(1<<(end-32))
		# same logic applied to board
		self.__board[start]=0
		self.__board[end]=direction_factor



	def toggle_middles(self, middles, direction_factor):
		for middle in middles:
			# remove/toggle middle (opponent's)
			if middle<32:
				self.__nums[abs((-direction_factor)-1)]^=(1<<middle) 
			else:
				self.__nums[abs((-direction_factor)-1)+1]^=(1<<(middle-32))
			# same logic applied to board
			self.__board[middle]=0



	def check_winner(self):
		username='__None__'
		for x in range(8): # 1st row
				if self.__board[x]==-1:
					username=self.__currentPlayer.get_username() if (self.__currentPlayer.get_side()=='-') else self.__currentPlayer.get_opponent().get_username()
		for x in range(56,63): # last row
				if self.__board[x]==1:
					username=self.__currentPlayer.get_username() if (self.__currentPlayer.get_side()=='+') else self.__currentPlayer.get_opponent().get_username()
		# run out of chessman?
		if not username=='__None__':
			self.__isEnd=True
		return username



	def int_list_2_str_list_str(self, int_list):
		s='['
		for x in int_list:
			s+=('"'+str(self.unsigned_2_signed(x))+'"')
			s+=','
		s=s[:-1]
		s+=']'
		return s


	def unsigned_2_signed(self, n):
		if n & 0x80000000:
			n =- 0x100000000+n
		return n



	# direction_factor is in fact "vertical_direction_factor"
	def dfs(self, start_row, start_col, end_row, end_col, middles, direction_factor):
		if start_row==end_row and start_col==end_col:
			return True, middles
		for horizontal_direction_factor in (-1, 1):
			tmp=(start_row+2*direction_factor)*8+(start_col+2*horizontal_direction_factor)
			if start_col+2*horizontal_direction_factor>=0 and start_col+2*horizontal_direction_factor<8 and tmp>=0 and tmp<64 and self.__board[(start_row+direction_factor)*8+(start_col+horizontal_direction_factor)]==-direction_factor and self.__board[tmp]==0:
				middles.append((start_row+direction_factor)*8+(start_col+horizontal_direction_factor))
				res=self.dfs(start_row+2*direction_factor, start_col+2*horizontal_direction_factor, end_row, end_col, middles, direction_factor)
				if res[0]:
					return True, res[1]
				middles.pop()
		return False, []



