'use strict';
console.log('game.js');
var start=null;
var isEnd=false;

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
	$(".box").click(clickHandler);
});




function updateBox(boxId, isEmpty, side) {
	let box=getBox(boxId);
	if(isEmpty)
		box.children[0].setAttribute('class', '');
	else if(side=='+')
		box.children[0].setAttribute('class', "glyphicon glyphicon-plus-sign");
	else if(side=='-')
		box.children[0].setAttribute('class', "glyphicon glyphicon-minus-sign");
}



function getBox(boxId) {
    return document.getElementById('wrapper').children[parseInt(boxId.split('_')[1])];
}


function clickHandler(){
	if(isEnd){
		console.log('game over. abort.')
		return;
	}
	let boxId=$(this).attr('id');
	console.log("clickHandler!"+boxId);
	console.log('myturn'+String(myTurn));
	console.log('start'+String(start));
	if(!myTurn){
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


function updateBoard(json){
	console.log('====updateBoard====');
	var mask=1;
	var num0=parseInt(json.actionDetail[0]);
	var num1=parseInt(json.actionDetail[1]);
	var num2=parseInt(json.actionDetail[2]);
	var num3=parseInt(json.actionDetail[3]);

	for(var i=0;i<32;i++){

		if((mask&num0)||(mask&num2))
			(mask&num0)?updateBox('box_'+i,false,'+'):updateBox('box_'+i,false,'-');
		else
			updateBox('box_'+i,true,'');


		if((mask&num1)||(mask&num3))
			(mask&num1)?updateBox('box_'+(i+32),false,'+'):updateBox('box_'+(i+32),false,'-');
		else
			updateBox('box_'+(i+32),true,'');

		mask<<=1;
	}
	// check winner
	if(json.winner!='__None__'){
		$("#game_intro")[0].innerHTML='Game over. The winner is '+ json.winner+'.';
		// end game
		isEnd=true;
	}
	// take turns
	console.log("take turns   "+username+"  "+json.currentPlayer);
	myTurn=(username==json.currentPlayer);

	// clear start point
	start=null;

	$("#game_intro")[0].innerHTML="success";
}


function explain_none(msg){
	$("#game_intro")[0].innerHTML=msg;
}


function game_gateway(command, json){
	if(command=='click'){
		switch(json.action){
			case 'update': updateBoard(json); break;
			// case 'show_hints': show_hints(json.actionDetail); break;
			// case 'end': end_game(json.actionDetail[0]); break;
			case 'none': explain_none(json.actionDetail[0]); break;
		}
	}
}





