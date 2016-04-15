(function(){
  var app = angular.module('VASapp', ['ngRoute']);


  // configure routes with routeProvider
  // locationProvider needed to remove the /#/ from the url
  app.config(function($routeProvider, $locationProvider){
    $routeProvider
      .when('/states',{
        templateUrl: 'partials/states.html',
        controller: 'statesController',
        controllerAs: 'states'
      }).when('/cities', {
        templateUrl: 'partials/cities.html',
        controller: 'citiesController',
        controllerAs: 'cities',
      }).when('/neighborhoods', {
        templateUrl: 'partials/neighborhoods.html',
        controller: 'neighborhoodsController',
        controllerAs: 'neighborhoods'
      }).when('/about', {
        templateUrl: 'about.html',
        controller: 'aboutController'
      }).otherwise({
        redirectTo: '/'
      });
    $locationProvider.html5Mode(true);
  });

  app.controller('statesController',['$scope', 'dataService', function($scope, dataService){
    $scope.$on('dataService.callAPISuccess', function(data){
      $scope.rows = data['states'];
      // $scope.apply();
    });
  }]);

  app.controller('citiesController',['$scope', 'dataService', function($scope, dataService){
    $scope.$on('dataService.callAPISuccess', function(data){
      $scope.rows = data['cities'];
      // $scope.apply();
    });
    this.sort = {
      by: 'id',
      descending: true
    };
    var init = function() {
      dataService.callAPI();
    }
    init();
  }]);

  //service to actually call API and manage the data
  //following example at http://tylermcginnis.com/angularjs-factory-vs-service-vs-provider/ for design
  app.service('dataService', ['$rootScope','$http', '$location', function($rootScope,$http,$location){
    var baseUrl = '';
    var apiExtension = '/api';
    var jsonUrl = '';
    var makeJsonUrl = function() {
      jsonUrl = baseUrl + apiExtension + $location.path();
      return jsonUrl;
    };
    this.data = {};
    this.callAPI = function(){
      makeJsonUrl();
      console.log("calling API at: " + jsonUrl);
      // $http.get(jsonUrl).then(
      $http.get('/json_data/cities.json').then(
        //success
        function(response){
          this.data = response.data;
          $rootScope.broadcast('dataService.callAPISuccess', response.data);
        }
        , //failure
        function(response){
          console.log("api call failed on: " + jsonUrl);

        }
      );
    };

  }]);
})();
