'use strict';


var socket=null;
var endpoint=null;
var username=null;
var room=null;
var myTurn=false;


$(document).ready(function(){
	dynamicallyLoadScript(['/static/js/welcome.js','/static/js/game.js']);

	endpoint='http://' + document.domain + ':' + location.port;
	console.log(endpoint);

});


function dynamicallyLoadScript(urlList) {
	urlList.forEach((url)=>{
		let script = document.createElement("script"); 
    	script.src = url; 
    	document.head.appendChild(script);
	});
}



function app_gateway(command, data){
	console.log('app_gateway '+command+" "+data);
	if(command=='invite'){
		socket=io.connect(endpoint);
		socket.on('response', on_response);

		socket.emit('json','{"command":"invite","username":"'+data+'"}');
	}else if(command=='join'){
		socket=io.connect(endpoint);
		socket.on('response', on_response);

		socket.emit('join','{"command":"join","room":"'+room+'","username":"'+username+'"}');
	}else if(command=='click'){
		socket.emit('json',data);
	}
}

function on_response(response){
	console.log('on_response='+response);
	let json=JSON.parse(response);
	let command=json.command;
	if(command=='invite'){
		welcome_gateway('invite',json);
		myTurn=true; // invitors always start first
	}else if(command=='join'){
		welcome_gateway('join',json);
	}else if(command=='click'){
		game_gateway('click',json);
	}
}




