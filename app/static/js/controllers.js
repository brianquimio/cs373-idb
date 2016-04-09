(function(){
  var app = angular.module('VAScontrollers',['ngRoute']);

  app.controller('mainCtrl', ['$scope', '$http', '$route', '$routeParams', '$location', function($scope, $http, $route, $routeParams, $location){
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
    $scope.name = "Virtual Address Space";
    $scope.status = 200;
    $scope.$pagedata = {"content": "is missing"};
    this.updateData = function(uri) {
      var dataLocation = '/app/templates/angular_routing/api/' + uri.toLowerCase() + '.json' ;
      console.log("doing a get on " + dataLocation);
      $http.get(dataLocation).then(
        //success
        function(response){
          $scope.status = response.status;
          $scope.$pagedata = response.data;
        },
        //error
        function(response){
          $scope.status = response.status;
          $scope.$pagedata = {};
        }
      );
    };
    this.printInfo = function() {
      console.log($scope.$location.$$path);
      console.log($scope.$pagedata);
    };
  }]);

  app.controller('splashCtrl', ['$scope', '$location', function($scope, $location) {
     $scope.name = "splashPage";
   }]);

  app.controller('aboutCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.name = "aboutPage";
  }]);


  app.controller('tableCtrl', ['$scope', '$location','$http', function($scope, $location, $http){
    this.tableData = [
      {
        "No": "Was",
        "Data": "Passed"
      }
    ];

    var splitPath = $location.$$path.split('/');
    $scope.tableName = splitPath[splitPath.length - 1];
    $scope.shownColumns = {};
    this.headers = [];
    this.rows = [];
    $scope.sorting = {
      "column": "",
      "descending": false
    };
    //reset the table to blank slate
    this.resetTable = function() {
      $scope.shownColumns = {};
      this.headers = [];
      this.rows = [];
    };
    //add a new column (header)
    this.addHeader = function(name) {
      this.headers.push(name);
      $scope.shownColumns[name]=true;
    };
    //add a new row
    this.addRow = function(rowAsJSON) {
      this.rows.push(rowAsJSON);
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
      $scope.sorting["column"]=this.headers[0];
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
    this.linkable = function (key) {
      var linkableCols = [
        "state_code",
        "state_name",
        "city_name",
        "neighborhood_name"
      ];
      function contains(a, obj) {
        for (var i = 0; i < a.length; i++) {
          if (a[i] === obj) {
            return true;
          };
        };
        return false;
      };
      return contains(linkableCols, key.toLowerCase());
    };
    this.buildPath = function(row,key) {
      if (row && key) {
        var path = "/app/templates/angular_routing";
        if (key === "neighborhood_name") {
          path += "/" + row["state_name"] + "/" + row["city_name"] + "/" + row["neighborhood_name"];
        } else if (key === "city_name") {
          path += "/" + row["state_name"] + "/" + row["city_name"];
        } else if (key === "state_name" || key === "state_code") {
          path += "/" + row["state_name"];
        } else {
          path = "#"
        };
      };
      return path;
    };
    this.buildTable($scope.$pagedata[$scope.tableName.toLowerCase()]);

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
