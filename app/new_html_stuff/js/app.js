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
        templateUrl: 'partials/about.html',
        controller: 'aboutController'
      }).when('/search', {
        templateUrl: 'partials/search.html',
        controller: 'searchController'
      }).when('/state/:stateCode', {
        templateUrl: 'partials/model.html',
        controller: 'stateModelController'
      }).when('/city/:cityId', {
        templateUrl: 'partials/model.html',
        controller: 'cityModelController'
      }).when('/neighborhood/:neighborhoodId', {
        templateUrl: 'partials/model.html',
        controller: 'neighborhoodModelController'
      }).when('/', {
        templateUrl: 'partials/splash.html',
        controller: 'splashController'
      }).
      // otherwise({
      //   redirectTo: '/'
      // });
    $locationProvider.html5Mode(true);
  });

  app.controller('mainController',['$scope', 'idMappingService', function($scope,idMappingService){
    this.printMappings = function(){console.log($scope.stateIdToName);console.log($scope.cityIdToName);console.log($scope.neighborhoodIdToName);};
  }]);

  app.controller('navController',['$scope', function($scope){}]);

  app.controller('splashController',['$scope', function($scope){}]);

  app.controller('aboutController',['$scope', function($scope){}]);

  app.controller('stateModelController',['$scope', '$routeParams', 'dataService', function($scope, $routeParams, dataService){
    $scope.data = {};
    console.log($routeParams);
    // var makeStateMapUrl = function() {
    //   var embedKey = "AIzaSyCADkkH1GoSKSlgVxk_oyLp6roM6XEx44I"
    //   var q = $scope.data[];
    //   var src = "https://www.google.com/maps/embed/v1/place?key="
    //   src += embedKey;
    //   src += "&q=";
    //   src += q;
    //   console.log(src);
    //
    //   var x ="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6509713.084021231!2d-123.77347912442343!3d37.1866687017569!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x808fb9fe5f285e3d%3A0x8b5109a227086f55!2sCalifornia!5e0!3m2!1sen!2sus!4v1458871633347"
    //   return $sce.trustAsResourceUrl(x);
    // }
    var init = function() {
      dataService.callAPI().then(function(data){$scope.data = data;}, function(data) {alert(data);});
    };
    init();
  }]);

  app.controller('statesController',['$scope', 'dataService', function($scope, dataService){
    //used to control table sorting through orderBy
    $scope.sort = {
      by: 'name',
      descending: false
    };
    //used to update/set sort values
    this.sortBy = function(col) {
      if ($scope.sort['by'] === col) {
        $scope.sort['descending'] = !$scope.sort['descending'];
      } else {
        $scope.sort['by'] = col;
        $scope.sort['descending'] = false;
      }
    };
    //used by ng-show, for chevron on column
    this.sortedBy = function(col) {
      return $scope.sort['by'] === col;
    };
    //used by ng-class, for chevron direction
    this.isDescending = function() {
      return $scope.sort['descending'];
    };
    //initializing function. sets scope data after resolving promise
    var init = function() {
      dataService.callAPI().then(function(data){$scope.rows = data['states'];},function(data){alert(data);});
    }
    init();
  }]);

  //controller for the citites page
  app.controller('citiesController',['$scope', 'dataService', function($scope, dataService){
    //used to control table sorting through orderBy
    $scope.sort = {
      by: 'name',
      descending: false
    };
    //used to update/set sort values
    this.sortBy = function(col) {
      if ($scope.sort['by'] === col) {
        $scope.sort['descending'] = !$scope.sort['descending'];
      } else {
        $scope.sort['by'] = col;
        $scope.sort['descending'] = false;
      }
    };
    //used by ng-show, for chevron on column
    this.sortedBy = function(col) {
      return $scope.sort['by'] === col;
    };
    //used by ng-class, for chevron direction
    this.isDescending = function() {
      return $scope.sort['descending'];
    };
    //initializing function. sets scope data after resolving promise
    var init = function() {
      dataService.callAPI().then(function(data){$scope.rows = data['cities'];},function(data){alert(data);});
    }
    init();
  }]);

  app.controller('neighborhoodsController',['$scope', 'dataService', function($scope, dataService){
    //used to control table sorting through orderBy
    $scope.sort = {
      by: 'name',
      descending: false
    };
    //used to update/set sort values
    this.sortBy = function(col) {
      if ($scope.sort['by'] === col) {
        $scope.sort['descending'] = !$scope.sort['descending'];
      } else {
        $scope.sort['by'] = col;
        $scope.sort['descending'] = false;
      }
    };
    //used by ng-show, for chevron on column
    this.sortedBy = function(col) {
      return $scope.sort['by'] === col;
    };
    //used by ng-class, for chevron direction
    this.isDescending = function() {
      return $scope.sort['descending'];
    };
    $scope.rows = [];
    var rowsHelper = function(data) {
      for (var row in data['neighborhoods']) {
        var newRow = data['neighborhoods'][row];
        newRow['cityName'] = $scope.cityIdToName[data['neighborhoods'][row]['city']];
        // console.log(newRow);
        $scope.rows.push(newRow);
      };
      // console.log($scope.rows);
    };
    //initializing function. sets scope data after resolving promise
    var init = function() {
      dataService.callAPI().then(function(data){rowsHelper(data);},function(data){alert(data);});
    }
    init();
  }]);

  //service to actually call API and manage the data
  //following example at http://tylermcginnis.com/angularjs-factory-vs-service-vs-provider/ for design
  app.service('dataService', ['$q','$http', '$location', function($q,$http,$location){
    var baseUrl = '';
    // var apiExtension = '/api';
    var apiExtension = '/json_data';
    var jsonUrl = '';
    var makeJsonUrl = function() {
      // jsonUrl = baseUrl + apiExtension + $location.path();
      jsonUrl = baseUrl + apiExtension + $location.path() + '.json';
      return jsonUrl;
    };
    this.data = {};
    this.callAPI = function(){
      makeJsonUrl();
      var deferred = $q.defer();
      console.log("calling API at: " + jsonUrl);
      $http.get(jsonUrl).then(
      // $http.get('/json_data/cities.json').then(
        //success
        function(response){
          this.data = response.data;
          deferred.resolve(response.data);
        }
        , //failure
        function(response){
          deferred.reject("api call failed on: " + jsonUrl);
        }
      )
      return deferred.promise;
    };
  }]);
  app.service('idMappingService',['$q','$http', '$location', '$rootScope', function($q,$http,$location,$rootScope){
    var dataGetHelper = function(url) {
      var deferred = $q.defer();
      $http.get(url).then(
      // $http.get('/json_data/cities.json').then(
        //success
        function(response){
          this.data = response.data;
          deferred.resolve(response.data);
        }
        , //failure
        function(response){
          deferred.reject("api call failed on: " + jsonUrl);
        }
      )
      return deferred.promise;
    };
    $rootScope.neighborhoodIdToName = {};
    $rootScope.cityIdToName = {};
    $rootScope.stateIdToName = {};
    var idToName = function(topLevelName, idTag, nameTag){
      this.cityIdToName = {};
      dataGetHelper('/json_data/'+topLevelName+'.json').then(
        function(data){
          // console.log(data);
          for (var i = 0; i < data[topLevelName].length; i += 1 ) {
            // console.log(data[topLevelName][i][idTag]);
            var id = data[topLevelName][i][idTag];
            // console.log(data[topLevelName][i][nameTag]);
            var name = data[topLevelName][i][nameTag];
            if(topLevelName === "states") $rootScope.stateIdToName[id] = name;
            if(topLevelName === "cities") $rootScope.cityIdToName[id] = name;
            if(topLevelName === "neighborhoods") $rootScope.neighborhoodIdToName[id] = name;
          };

        }, function(data){
          alert(data)
        });
    };
    idToName('cities','cityId','name');
    idToName('neighborhoods','id','name');
    idToName('states','stateCode','name');
    // console.log($rootScope.cityIdToName);
  }]);
})();
``
