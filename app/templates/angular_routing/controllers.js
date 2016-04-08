(function(){
  var app = angular.module('VAScontrollers',['ngRoute']);

  app.controller('mainCtrl', ['$scope', '$http', '$route', '$routeParams', '$location', function($scope, $http, $route, $routeParams, $location){
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
    $scope.name = "Virtual Address Space";
    $scope.status = 200;
    $scope.data = {"content": "is missing"};
    this.updateData = function(uri) {
      var dataLocation = '/app/templates/angular_routing/api/' + uri.toLowerCase() + '.json' ;
      console.log(dataLocation);
      $http.get(dataLocation).then(
        //success
        function(response){
          $scope.status = response.status;
          $scope.data = response.data;
          $scope.currentPage = $scope.$location.$$path;
        },
        //error
        function(response){
          $scope.status = response.status;
          $scope.data = response.statusText;
        }
      );
    };
    this.printInfo = function() {
      console.log($scope.$location.$$path);
      console.log($scope.data);
    };
    this.printInfo();
  }]);

  app.controller('splashCtrl', ['$scope', '$location', function($scope, $location) {
     $scope.name = "splashPage";
   }]);

  app.controller('aboutCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.name = "aboutPage";
  }]);


  app.controller('tableCtrl', ['$scope', '$location', function($scope, $location){
    this.tableData = [
      {
        "No": "Was",
        "Data": "Passed"
      }
    ];

    var splitPath = $location.$$path.split('/')
    $scope.tableName = splitPath[splitPath.lentgth - 1];
    $scope.shownColumns = {};
    $scope.headers = [];
    $scope.rows = [];
    $scope.sorting = {
      "column": "",
      "descending": false
    };
    //reset the table to blank slate
    this.resetTable = function() {
      $scope.shownColumns = {};
      $scope.headers = [];
      $scope.rows = [];
    };
    //add a new column (header)
    this.addHeader = function(name) {
      $scope.headers.push(name);
      $scope.shownColumns[name]=true;
    };
    //add a new row
    this.addRow = function(rowAsJSON) {
      $scope.rows.push(rowAsJSON);
    };
    //build the table from a json
    this.buildTable = function(data = this.tableData) {
      this.resetTable();
      //get the property names from the first element
      for( o in data[0] ) {
        this.addHeader(o);
      };
      //for each row, build and add
      for(var rowData in data) {
        var newRow = data[rowData];
        this.addRow(newRow);
      };
      $scope.sorting["column"]=$scope.headers[0];
    };
    //column is shown
    this.colIsShown = function(columnName) {
      return $scope.shownColumns[columnName];
    };
    //make column visible
    this.showCol = function(columnName) {
      if ($scope.shownColumns.hasOwnProperty(columnName)) {
        $scope.shownColumns[columnName] = true;
      };
    };
    //make column hidden
    this.hideCol = function(columnName) {
      if ($scope.shownColumns.hasOwnProperty(columnName)) {
        $scope.shownColumns[columnName] = false;
      };
    };
    //sort the table
    this.sortBy = function(columnName) {
      if ($scope.sorting["column"] = columnName) {
        this.flipDir();
      } else {
        $scope.sorting["column"] = columnName;
      };
    };
    //flip the direction of the table
    this.flipDir = function() {
      $scope.sorting["descending"] = !$scope.sorting["descending"];
    };
    this.buildTable($scope.data);
  }]);

  app.controller('navbarCtrl', ['$scope', function($scope) {
    $scope.navLinks = ["About", "States", "Cities", "Neighborhoods"];
  }]);

  // app.config(function($routeProvider,$locationProvider) {
  //   $routeProvider.when('/', {
  //
  //   })
  // });

})();
