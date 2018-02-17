'use strict';

console.log('welcome.js');


$(document).ready(function(){
	// setup enter trigger


	// init display
	$("#enter_username").hide();
	$("#show_room").hide();

	$("#enter_room_key").hide();
	$("#enter_username_invited").hide();

	$("#enter_room_key_resume").hide();
	$("#enter_username_resume").hide();



	// setup onclick
	$("#invite_opponent").unbind('click').click(invite_opponent);
	$("#go").click(go);

	$("#i_am_invited").unbind('click').click(i_am_invited);
	$("#go_invited").unbind('click').click(go_invited);  // room_key
	$("#go_invited_username").unbind('click').click(go_invited_username);

	$("#resume").unbind('click').click(resume);
	$("#go_resume").unbind('click').click(enter_room_key_resume);
	$("#go_resume_username").unbind('click').click(enter_username_resume);
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


function go_invited(){
	room=$("#room_key_invited").val();
	$("#enter_room_key").hide();
	$("#enter_username_invited").show();
}


function go_invited_username(){
	username=$("#username_invited").val();
	app_gateway('join',username);
}


function resume(){
	$("#welcome_btn_group").hide();
	$("#enter_room_key_resume").show();
}

function enter_room_key_resume(){
	$("#enter_room_key_resume").hide();
	$("#enter_username_resume").show();
}

function enter_username_resume(){
	room=$("#room_key_resume").val();
	username=$("#username_resume").val();
	app_gateway('resume','{"room":"'+room+'","username":"'+username+'"}');
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
	}else if(command=='resume'){
		if(json.status=='success'){
			window.location.replace(endpoint+"/#/game");
		}
	}
}




