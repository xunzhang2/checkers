'use strict';

console.log('welcome.js');


$(document).ready(function(){
	// init display
	$("#enter_username").hide();
	$("#show_room").hide();

	$("#enter_room_key").hide();
	$("#enter_username_invited").hide();


	// setup onclick
	$("#invite_opponent").click(invite_opponent);
	$("#go").click(go);

	$("#i_am_invited").click(i_am_invited);
	$("#go_invited").click(go_invited);  // room_key
	$("#go_invited_username").click(go_invited_username);
});



function invite_opponent(){
	$("#welcome_btn_group").hide();
	$("#enter_username").show();
}


function go(){
	username=$("#username").val();
	$("#enter_username").hide();
	$("#show_room").show();
	app_gateway('invite', username);
}

// I am invited

function i_am_invited(){
	$("#welcome_btn_group").hide();
	$("#enter_room_key").show();
}


// when username is entered
function go_invited(){
	room=$("#room_key_invited").val();
	$("#enter_room_key").hide();
	$("#enter_username_invited").show();
}


function go_invited_username(){
	username=$("#username_invited").val();
	app_gateway('join',username);
}


function welcome_gateway(command, json){
	if(command=='invite'){
		room=json.room;
		$("#room_key")[0].innerHTML=room;
		$("#welcome_intro")[0].innerHTML=json.status+': '+json.statusDetail;
	}else if(command=='join'){
		if(json.status=='success'){
			window.location.replace(endpoint+"/#/game");
		}else{
			$("#welcome_intro")[0].innerHTML=json.status+': '+json.statusDetail;
		}
	}
}




