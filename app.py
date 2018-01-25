from flask import Flask, render_template, request, copy_current_request_context
from flask_socketio import SocketIO, join_room, leave_room
from model import Model
from game import Game
from player import Player
import json as JSON
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
model=Model()



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
			currentPlayer=Player(sid, None, '+', room, jsonDict['username'])
			game=Game(currentPlayer, room)
			game.start()
			model.put_game(room,game)
			model.put_player(sid,currentPlayer)
			response='{"command":"invite","status":"success","statusDetail":"Use room key to invite. Game automatically starts when the opponent joins.","room":"'+str(room)+'"}'
			socketio.emit('response',response,room=room)
		elif command=='click':
			room=str(model.get_room(sid))
			game=model.get_game(room)
			# put side
			jsonDict['side']=model.get_player(sid).get_side()
			game.set_json(jsonDict)
			# waiting for game to calculate response
			while(not game.get_response()):
				time.sleep(2)
			response=game.get_response()
			game.set_response(None)
			socketio.emit('response',response,room=room)
		elif command=='resume':
			room=str(jsonDict['room'])
			if model.is_room_valid(room):
				username=str(jsonDict['username'])
				game=model.get_game(room)
				# get player which may be invalid
				# NOTE: avoid pretend as the other player!
				player=None
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
					print response
					socketio.emit('response',response,room=room)
					# retrieve status and update board, make sure send later
					game.set_json(jsonDict)
					# waiting for game to calculate response
					while(not game.get_response()):
						time.sleep(2)
					response=game.get_response()  # (response overwritten!)
					print response
					game.set_response(None)
					# make sure send later
					time.sleep(1)
					socketio.emit('response',response,room=room)
				else:
					response='{"command":"resume","status":"failure","statusDetail":"Cannot resume due to invalid username."}'
					print response
					socketio.emit('response',response,room=room)
			else:
				response='{"command":"resume","status":"failure","statusDetail":"Cannot resume due to invalid room key."}'
				print response
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
			anotherPlayer=Player(sid, None, '-', room, jsonDict['username'])
			# save player '-'
			model.put_player(sid, anotherPlayer)
			# retrieve game
			game=model.get_game(room)
			# add player to game
			anotherPlayer.set_opponent(game.get_current_player())
			game.get_current_player().set_opponent(anotherPlayer)
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

