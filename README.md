# Two-player Checkers

## Tools
Back end: flask, flask-socketio, python </br>
Front end: jQuery, angularjs, socketio, bootstrap, javascript </br>

## Design
==========Back end==========</br>
class Game (Thread)</br>
class Player</br>

One game contains one current_player which points to opponent. Two players points to each other.</br>
    
class Model: mocks memory and database</br>
</br>
Gateway (app.py) receives incoming requests and creates threads to do work.</br>

</br>
==========Front end==========</br>
main controller |socket connection<----gateway| <-----send request-----  view controllers </br>

main controller |one socket connection----> dispatcher| -----dispatch response----> |gateway------>handlers| view controllers </br>


    
 
