# Two-player Checkers

## Demo (https://www.youtube.com/watch?v=S319CzQkpsQ)
[![Watch the video](https://github.com/xunzhang2/checkers/blob/master/screenshot3.png)](https://www.youtube.com/watch?v=S319CzQkpsQ)

## Tools
Back end: flask, flask-socketio, python </br>
Front end: jQuery, angularjs, socketio, bootstrap, javascript </br>

## Design
==========Back end==========</br>
class Game extends Thread</br>
</br>
class Player</br>
</br>
One game contains one current_player which points to opponent. Two players points to each other.</br>
</br>
class Model: represents memory and mocks database, recording runtime players and games status. (In production db should be used.)</br>
</br>
Gateway (app.py) receives incoming requests and creates games(threads) to do work. Or if game exists, "notify" it.</br>
</br>
Used threading.Condition to synchronize threads.</br>
</br>
==========Front end==========</br>
main controller |socket connection<----gateway| <-----send request-----  view controllers </br>
</br>
main controller |one socket connection----> dispatcher| -----dispatch response----> |gateway------>handlers| view controllers</br>
</br>
==========Algorithm==========</br>
DFS, bit manipulation, ...</br>

## Time spent on dev
2 days + 2 nights</br>

## How to run locally

pip install Flask</br>
pip install flask-socketio</br>
python app.py</br>


    
 
