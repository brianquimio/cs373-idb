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
        templateUrl: 'partials/state_model.html',
        controller: 'stateModelController',
        controllerAs: 'state'
      }).when('/city/:cityId', {
        templateUrl: 'partials/model.html',
        controller: 'cityModelController'
      }).when('/neighborhood/:neighborhoodId', {
        templateUrl: 'partials/model.html',
        controller: 'neighborhoodModelController'
      }).when('/', {
        templateUrl: 'partials/splash.html',
        controller: 'splashController'
      });
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

  app.controller('stateModelController',['$scope', '$routeParams', 'dataService', '$sce', function($scope, $routeParams, dataService, $sce){
    $scope.data = {};
    $scope.week = null;
    $scope.weeks = [];
    $scope.filterOptions = {};
    var buildData = function(data) {
      $scope.data = {};
      $scope.weeks = [];
      var temp = {};
      $scope.data['stateCode'] = $routeParams['stateCode'];
      $scope.data['propertyStats'] = [];
      $scope.data['cities'] = [];
      for (var key in data['stats']) {
        var newRow = {};
        var weekOf = data['stats'][key]['week_of'];
        var propertyType = data['stats'][key]['property_type'];
        var avg = data['stats'][key]['avg_listing_price'];
        var med = data['stats'][key]['med_listing_price'];
        var num = data['stats'][key]['num_properties'];
        temp[weekOf] = true;
        newRow['week'] = weekOf;
        newRow['type'] = propertyType;
        newRow['average'] = Number(avg);
        newRow['median'] = Number(med);
        newRow['numProps'] = Number(num);
        $scope.data['propertyStats'].push(newRow);
      };
      for (var key in data['cities']) {
        $scope.data['cities'].push(data['cities'][key]['city_name']);
      }
      $scope.filterOptions = {};
      for(var key in $scope.data['propertyStats'][0]) {
        $scope.filterOptions[key] = true;
      }
      for(var key in temp) {
        $scope.weeks.push(key);
      }
      $scope.week = $scope.weeks[$scope.weeks.length - 1];
      // {week_of: {propertyType: {avg: int, median: int, numProps: int}, ... }, ... }
    };
    this.printData = function(){
      console.log($scope.data);
      console.log($scope.filterOptions);
      console.log($scope.week);
    }
    //FROM HERE ########################
    $scope.sort = {
      by: 'type',
      descending: false
    };
    this.showRow = function(row) {
      // console.log(row);
      return $scope.week === row['week'];
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
    //TO HERE ########################## is VERY repetitive code (copy-paste)
    this.setStateMapUrl = function() {
      var embedKey = "AIzaSyC5xVHl08OeT9jM4q_lwfY30IYPf3Jd3B0"
      var q = "State+of+" + $scope.data['stateCode'];
      var src = "https://www.google.com/maps/embed/v1/place?key="
      src += embedKey;
      src += "&q=";
      src += q;
      console.log(src);
      // var x ="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6509713.084021231!2d-123.77347912442343!3d37.1866687017569!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x808fb9fe5f285e3d%3A0x8b5109a227086f55!2sCalifornia!5e0!3m2!1sen!2sus!4v1458871633347"
      return $sce.trustAsResourceUrl(src);
    }
    var test_object = { "cities":{"05000":{"city_id":"05000","city_name":"Austin","latitude":"30.265887","longitude":"-97.745876","state_code":"TX"},"07396":{"city_id":"07396","city_name":"Bellevue","latitude":"33.6338544894988","longitude":"-98.0163214693602","state_code":"TX"},"19000":{"city_id":"19000","city_name":"Dallas","latitude":"32.775728","longitude":"-96.798477","state_code":"TX"},"35000":{"city_id":"35000","city_name":"Houston","latitude":"29.754839","longitude":"-95.365104","state_code":"TX"}},"stats":{"51":{"avg_listing_price":"389681","id":51,"med_listing_price":"277473","num_properties":"39109","property_type":"All Properties","state_code":"TX","week_of":"2016-03-12"},"52":{"avg_listing_price":"399421","id":52,"med_listing_price":"137555","num_properties":"588","property_type":"1 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"53":{"avg_listing_price":"246210","id":53,"med_listing_price":"169593","num_properties":"3097","property_type":"2 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"54":{"avg_listing_price":"285476","id":54,"med_listing_price":"215097","num_properties":"15975","property_type":"3 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"55":{"avg_listing_price":"422477","id":55,"med_listing_price":"341389","num_properties":"14038","property_type":"4 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"56":{"avg_listing_price":"667787","id":56,"med_listing_price":"456424","num_properties":"3748","property_type":"5 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"57":{"avg_listing_price":"1592651","id":57,"med_listing_price":"771707","num_properties":"321","property_type":"6 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"58":{"avg_listing_price":"2597785","id":58,"med_listing_price":"982114","num_properties":"74","property_type":"7 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"59":{"avg_listing_price":"2208287","id":59,"med_listing_price":"1553000","num_properties":"22","property_type":"8 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"60":{"avg_listing_price":"5250080","id":60,"med_listing_price":"2178571","num_properties":"13","property_type":"9 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"61":{"avg_listing_price":"3008709","id":61,"med_listing_price":"2965786","num_properties":"6","property_type":"10 Bedroom Properties","state_code":"TX","week_of":"2016-03-12"},"62":{"avg_listing_price":"415439","id":62,"med_listing_price":"289450","num_properties":"24685","property_type":"All Properties","state_code":"TX","week_of":"2016-03-19"},"63":{"avg_listing_price":"525410","id":63,"med_listing_price":"148500","num_properties":"373","property_type":"1 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"64":{"avg_listing_price":"256589","id":64,"med_listing_price":"182245","num_properties":"1877","property_type":"2 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"65":{"avg_listing_price":"298659","id":65,"med_listing_price":"224900","num_properties":"9672","property_type":"3 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"66":{"avg_listing_price":"437791","id":66,"med_listing_price":"348250","num_properties":"9150","property_type":"4 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"67":{"avg_listing_price":"695985","id":67,"med_listing_price":"468498","num_properties":"2551","property_type":"5 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"68":{"avg_listing_price":"1752797","id":68,"med_listing_price":"897450","num_properties":"210","property_type":"6 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"69":{"avg_listing_price":"2965977","id":69,"med_listing_price":"1407250","num_properties":"57","property_type":"7 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"70":{"avg_listing_price":"2111666","id":70,"med_listing_price":"1846250","num_properties":"13","property_type":"8 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"71":{"avg_listing_price":"6697849","id":71,"med_listing_price":"4250000","num_properties":"10","property_type":"9 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"},"72":{"avg_listing_price":"3025000","id":72,"med_listing_price":"3025000","num_properties":"3","property_type":"10 Bedroom Properties","state_code":"TX","week_of":"2016-03-19"}}};
    var init = function() {
      dataService.callAPI().then(function(data){buildData(data);}, function(data) {alert(data);buildData(test_object);});
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
    // var baseUrl = 'virtual-address.space';
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
      //update this later
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
