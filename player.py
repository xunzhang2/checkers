
class Player:
	def __init__(self, sid, opponent, side, room, username='anonymous'):
		self.__id=sid
		self.__opponent=opponent
		self.__side=side
		self.__room=room
		self.__username=username


	def get_opponent(self):
		return self.__opponent


	def set_opponent(self, opponent):
		self.__opponent=opponent


	def get_room(self):
		return self.__room


	def get_username(self):
		return self.__username


	def set_username(self, username):
		self.__username=username


	def get_side(self):
		return self.__side





