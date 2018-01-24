from flask import Flask, render_template, request, copy_current_request_context
from flask_socketio import SocketIO, join_room
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
		room=str(model.get_room(sid))
		print 'room=',room

		if command=='invite':
			join_room(room,sid)
			currentPlayer=Player(sid, None, '+', room, jsonDict['username'])
			game=Game(currentPlayer, room)
			game.start()
			model.put_game(room,game)
			model.put_player(sid,currentPlayer)
			response='{"command":"invite","status":"success","statusDetail":"Use room key to invite. Game automatically starts when the opponent joins.","room":"'+str(room)+'"}'
		elif command=='click':
			game=model.get_game(room)
			# put side
			jsonDict['side']=model.get_player(sid).get_side()
			game.set_json(jsonDict)
			# waiting for game to calculate response
			while(not game.get_response()):
				time.sleep(5)
			response=game.get_response()
			game.set_response(None)
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




def handle_leave(sid):
	pass




if __name__ == '__main__':
	socketio.run(app)

