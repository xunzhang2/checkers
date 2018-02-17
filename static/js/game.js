'use strict';
console.log('game.js');
var start=null;

$(document).ready(function(){
	
	// init-draw board and checkers
	for(var i=0;i<64;i++){
		var row=parseInt(i/8);
		if(row%2==0){
		    $(".wrapper").append("<div class='box box_even' id='box_"+i+"'><div></div></div>");
		}
		else{
		     $(".wrapper").append("<div class='box box_odd' id='box_"+i+"'><div></div></div>");
		}
		if((row+i)%2!=0)  // white box
			continue;
		if(row<3)
			try{
				document.getElementById('wrapper').children[i].children[0].setAttribute('class', "glyphicon glyphicon-plus-sign");
			}catch(err){}
		else if(row>4)
			try{
				document.getElementById('wrapper').children[i].children[0].setAttribute('class', "glyphicon glyphicon-minus-sign");
			}catch(err){}
	}


	// setup onclick
	$(".box").unbind('click').click(clickHandler);
	$("#leave").unbind('click').click(clickHandler);
});




function updateBox(boxId, isEmpty, side) {
	let box=getBox(boxId);
	if(isEmpty)
		box.children[0].setAttribute('class', '');
	else if(side==1)
		box.children[0].setAttribute('class', "glyphicon glyphicon-plus-sign");
	else if(side==-1)
		box.children[0].setAttribute('class', "glyphicon glyphicon-minus-sign");
}



function getBox(boxId) {
	if(typeof boxId === 'number')
		return document.getElementById('wrapper').children[boxId];
	else if(typeof boxId === 'string')
    	return document.getElementById('wrapper').children[parseInt(boxId.split('_')[1])];
}


function clickHandler(){
	if($(this).attr('id')=='leave'){
		console.log('clicked leave! room='+room);
		app_gateway('leave',room);
	}else if(this.classList.contains('box')){
		let boxId=$(this).attr('id');
		console.log("clickHandler!"+boxId);
		console.log('myturn'+String(myTurn));
		console.log('start'+String(start));
		if(!myTurn){
			$("#game_intro")[0].innerHTML='Not your turn.';
			return;
		}
		let isFilled=getBox(boxId).children[0].classList.contains('glyphicon')
		if(start){  // start is filled
			if(isFilled){
				start=boxId;  // reset start
			}else{
				app_gateway('click','{"command":"click","start":"'+start+'", "end":"'+boxId+'"}');  // move!
			}
		}else{   // start is empty
			if(isFilled){
				start=boxId;  // init start
			}else{
				;
			}
		}
	}

	
}


function refreshBoard(json){
	console.log('====refreshBoard====');
	var mask=1;
	var num0=parseInt(json.actionDetail[0]);
	var num1=parseInt(json.actionDetail[1]);
	var num2=parseInt(json.actionDetail[2]);
	var num3=parseInt(json.actionDetail[3]);

	for(var i=0;i<32;i++){

		if(i==27){
			console.log("******"+String((mask&num0))+" | "+String(mask&num2))
		}

		if((mask&num0)||(mask&num2))
			(mask&num0)?updateBox(i,false,1):updateBox(i,false,-1);
		else
			updateBox(i,true,0);


		if((mask&num1)||(mask&num3))
			(mask&num1)?updateBox(i+32,false,1):updateBox(i+32,false,-1);
		else
			updateBox(i+32,true,0);

		mask<<=1;
	}

	$("#game_intro")[0].innerHTML="Board status has been synchronized with server.";


	// check winner
	if(json.winner!='__None__'){
		$("#game_intro")[0].innerHTML='Game over. The winner is '+ json.winner+'.';
	}
	// take turns
	console.log("take turns   "+username+"  "+json.currentPlayer);
	myTurn=(username==json.currentPlayer);

	// clear start point
	start=null;
}


function updateBoard(json){
	let start_time=date.getTime();
	
	json.actionDetail.forEach((pair)=>{
		if(pair.side==0)
			updateBox(pair.boxId, true, 0);
		else
			updateBox(pair.boxId, false, pair.side);
	});

	$("#game_intro")[0].innerHTML="success";

	// check winner
	if(json.winner!='__None__'){
		$("#game_intro")[0].innerHTML='Game over. The winner is '+ json.winner+'.';
	}
	// take turns
	console.log("take turns   "+username+"  "+json.currentPlayer);
	myTurn=(username==json.currentPlayer);

	// clear start point
	start=null;
	console.log('====updateBoard===='+String(date.getTime()-start_time));
}


function explain_none(msg){
	$("#game_intro")[0].innerHTML=msg;
}


function game_gateway(command, json){
	if(command=='click'){
		switch(json.action){
			case 'refresh': refreshBoard(json); break;
			case 'update': updateBoard(json); break;
			// case 'show_hints': show_hints(json.actionDetail); break;
			case 'none': explain_none(json.actionDetail[0]); break;
		}
	}else if(command=='leave'){
		$("#game_intro")[0].innerHTML=json.username+' has left the game.';
	}
}





