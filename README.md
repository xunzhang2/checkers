# Two-player Checkers

## Tools
Back end: flask, flask-socketio, python </br>
Front end: jQuery, angularjs, socketio, bootstrap, javascript </br>

## Design
==========Back end==========</br>
class Game (Thread) contains: </br>
    current player (Player) <--(points each other)--> opponent (Player)</br>
    board array: len=64, val in (-1, 0, 1)</br>
    board value encoding (signed 32-bit int * 4): | 0~31 current player | 32~63 current player | 0~32 opponent | 32~63 opponent | </br>
    json payload: mocks input stream of socket, because flask-socketio does not return connection instance. </br>
    ...</br>
</br>
class Player contains: </br>
    pointer to opponent</br>
    socket id</br>
    ...</br>
</br>    
class Model: mocks memory and database</br>
</br>
Gateway (app.py) receives incoming requests and creates threads to do work.</br>

</br>
==========Front end==========</br>
main controller |socket connection<----gateway| <-----send request-----  view controllers </br>

main controller |one socket connection----> dispatcher| -----dispatch response----> |gateway------>handlers| view controllers </br>


    
 
