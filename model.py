import time


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Model(object):
	__metaclass__ = Singleton

	def __init__(self):
		self.__playerDict={} # key=sid, val=player instance
		self.__roomDict={} # key=room, val=game instance


	def is_room_valid(self, room):
		return str(room) in self.__roomDict;


	def get_room(self, sid):
		if str(sid) in self.__playerDict:
			return self.__playerDict[str(sid)].get_room()
		else:
			return str(int(round(time.time() * 1000))) # new room



	def put_game(self, room, game):
		self.__roomDict[str(room)]=game


	def get_game(self, room):
		return self.__roomDict[str(room)]

	def put_player(self, sid, player):
		self.__playerDict[str(sid)]=player


	def get_player(self, sid):
		return self.__playerDict[str(sid)]


	def remove_player(self, sid):
		self.__playerDict.pop(str(sid))


