from flask import Flask, render_template, request, copy_current_request_context
from flask_socketio import SocketIO, join_room, leave_room
from model import Model
from game import Game
from player import Player
import json as JSON
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
model=Model()
condition = threading.Condition()
# condition.acquire()  # make sure main thread firstly get lock



@app.route('/')
def hello_world():
	return render_template('index.html')



@socketio.on('connect')
def on_connect():
	print 'connect! sid=',request.sid



@socketio.on('json')
def on_json(json):
	print 'received json: ', str(json)

	@copy_current_request_context
	def handle_request(json):
		jsonDict=JSON.loads(json)
		command=jsonDict['command']
		sid=str(request.sid)

		if command=='invite':
			room=str(model.get_room(sid))
			join_room(room,sid)
			currentPlayer=model.get_player(sid)
			if not currentPlayer:
				currentPlayer=Player(sid, None, '+', room, jsonDict['username'])
			game=Game(currentPlayer, room, condition)
			game.start()
			model.put_game(room,game)
			model.put_player(sid,currentPlayer)
			response='{"command":"invite","status":"success","statusDetail":"Use room key to invite. Game automatically starts when the opponent joins.","room":"'+str(room)+'"}'
			socketio.emit('response',response,room=room)
		elif command=='click':
			print 'click acquiring    !!!'
			condition.acquire()
			print 'click acquired    !!!'
			room=str(model.get_room(sid))
			game=model.get_game(room)
			# put side
			jsonDict['side']=model.get_player(sid).get_side()
			game.set_json(jsonDict)
			condition.notifyAll()
			condition.release()
			# waiting for game to calculate response
			time.sleep(0.005) # make sure game threads get the lock
			print 'click acquiring  2  !!!'
			condition.acquire()
			print 'click acquired  2  !!!'
			while(not game.get_response()):
				condition.wait()
			response=game.get_response()
			game.set_response(None)
			condition.release()
			socketio.emit('response',response,room=room)
		elif command=='resume':
			room=str(jsonDict['room'])
			if model.is_room_valid(room):
				username=str(jsonDict['username'])
				game=model.get_game(room)
				# get player which may be invalid
				# NOTE: avoid pretend as the other player!
				player=None
				print '+++++++++'+str(game.get_current_player().get_username())+" | "+str(game.get_current_player().is_active())+" | "+str(game.get_current_player().get_opponent().get_username())+" | "+str(game.get_current_player().get_opponent().is_active())
				if game.get_current_player().get_username()==username and (not game.get_current_player().is_active()):
					player=game.get_current_player()
				elif game.get_current_player().get_opponent().get_username()==username and (not game.get_current_player().get_opponent().is_active()):
					player=game.get_current_player().get_opponent()
				# username is valid
				if player:
					model.remove_player(player.get_id())
					player.set_id(sid)
					player.set_isActive(True)
					model.put_player(sid,player)
					# join room
					join_room(room,sid)
					response='{"command":"resume","status":"success","statusDetail":"Game resumes."}'
					socketio.emit('response',response,room=room)
					# retrieve status and update board, make sure send later
					print 'acquiring    !!!'
					condition.acquire()
					print 'acquirED    !!!'
					game.set_json(jsonDict)
					condition.notifyAll()
					condition.release()
					# waiting for game to calculate response
					time.sleep(1) # make sure game threads get the lock AND page is re-loaded
					condition.acquire()
					while(not game.get_response()):
						condition.wait()  # (response overwritten!)
					response=game.get_response()
					game.set_response(None)
					condition.release()
					socketio.emit('response',response,room=room)
				else:
					response='{"command":"resume","status":"failure","statusDetail":"Cannot resume due to invalid username."}'
					socketio.emit('response',response,room=room)
			else:
				response='{"command":"resume","status":"failure","statusDetail":"Cannot resume due to invalid room key."}'
				socketio.emit('response',response,room=room)
	socketio.start_background_task(handle_request,(json))



@socketio.on('join')
def on_join(data):
	print 'joined! data=', str(data), 'sid=', request.sid

	@copy_current_request_context
	def handle_join(data):
		# create player '-'
		sid=str(request.sid)
		jsonDict=JSON.loads(data)
		room=str(jsonDict['room'])
		# validate room
		if model.is_room_valid(room):
			anotherPlayer=model.get_player(sid)
			if(not anotherPlayer):
				anotherPlayer=Player(sid, None, '-', room, jsonDict['username'])
			# save player '-'
			model.put_player(sid, anotherPlayer)
			# retrieve game
			game=model.get_game(room)
			# add player to game
			anotherPlayer.set_opponent(game.get_current_player())
			game.get_current_player().set_opponent(anotherPlayer)
			print '***********'+str(anotherPlayer.get_opponent().get_username())+" | "+str(game.get_current_player().get_opponent().get_username())
			# join room
			join_room(room,sid)
			response='{"command":"join","room":"'+room+'","player":"'+game.get_current_player().get_username()+'","opponent":"'+anotherPlayer.get_username()+'","status":"success","statusDetail":"success"}'
			socketio.emit('response', response, room=room)		
		else:
			response='{"command":"join","room":"'+room+'","status":"failure","statusDetail":"Opponent has entered invalid room key."}'
			socketio.emit('response', response, broadcast=False)

	socketio.start_background_task(handle_join,(data))



@socketio.on('leave')
def on_leave(data):
	print 'leave! data=', str(data), 'sid=', request.sid
	jsonDict=JSON.loads(data)
	username = str(jsonDict['username'])
	room = str(jsonDict['room'])
	leave_room(room)
	socketio.emit('response', '{"command":"leave","username":"'+username+'"}', room=room)
	# change server status
	@copy_current_request_context
	def handle_leave(room):
		# retrieve game
		game=model.get_game(room)
		game.set_response(None) # optional
		sid=str(request.sid)
		if game.get_current_player().get_id()==sid:
			game.get_current_player().set_isActive(False)
		elif game.get_current_player().get_opponent().get_id()==sid:
			game.get_current_player().get_opponent().set_isActive(False)

	socketio.start_background_task(handle_leave,(room))









if __name__ == '__main__':
	socketio.run(app)

