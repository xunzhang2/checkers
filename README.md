# Two-player Checkers

## Youtube demo
https://www.youtube.com/watch?v=aiqTH5YXh2o

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

## Time spent in dev
1.5 days + 2 nights</br>

## How to run locally

pip install Flask</br>
pip install flask-socketio</br>
python app.py</br>


    
 
