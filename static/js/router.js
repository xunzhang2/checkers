angular.module('myApp',['ngRoute'])
            .config(['$routeProvider', function($routeProvider){
                $routeProvider
                .when('/',{templateUrl: '/static/views/welcome.html'})
                .when('/game',{templateUrl: '/static/views/game.html'})
                .otherwise({redirectTo:'/'});
            }]);