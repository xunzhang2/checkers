# Two-player Checkers

## Demo
Website: http://34.230.44.118:5000/ </br>
Vedio: https://www.youtube.com/watch?v=aiqTH5YXh2o  </br>

## Tools
Back end: flask, flask-socketio, python </br>
Front end: jQuery, angularjs, socketio, bootstrap, javascript </br>

## Design
==========Back end==========</br>
class Game extends Thread</br>
class Player</br>

One game contains one current_player which points to opponent. Two players points to each other.</br>
    
class Model: represents memory and mocks database, recording runtime players and games status. (In production db should be used.) </br>
</br>
Gateway (app.py) receives incoming requests and creates games(threads) to do work. Or if game exists, "notify" it. </br>

</br>
==========Front end==========</br>
main controller |socket connection<----gateway| <-----send request-----  view controllers </br>

main controller |one socket connection----> dispatcher| -----dispatch response----> |gateway------>handlers| view controllers </br>

## Time spent on dev
1.5 days + 2 nights</br>

## How to run locally

pip install Flask</br>
pip install flask-socketio</br>
python app.py</br>


    
 
