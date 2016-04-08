(function(){
  var app = angular.module('VASapp', ['ngResource']);

  app.errorPage = "../error404.html";
  app.nowhere= "#";

  app.controller('mainController',
    [ '$rootScope',
      '$http',
      function($rootScope, $http){
        $rootScope.name = "Virtual Address Space";
        $rootScope.currentPage = "Home";
        $rootScope.data = {};
        this.pageData = {};
        this.followRef = function(link) {
          // $rootScope.currentPage = link.display;
          $http.get(link.ref)
          .then(function(response) {
            $rootScope.status = response.status;
            $rootScope.data = response.data;
            $rootScope.currentPage = $rootScope.data["name"];
            }, function(response) {
            $rootScope.data = response.data || "Request failed";
            $rootScope.status = response.status;
          })
        };
      }]);

  app.controller('navbarController',
    [ '$rootScope',
      '$http',
      function($rootScope, $http){
      $rootScope.navLinks = [];
      this.addLink = function(link) {
        $rootScope.navLinks.push(link);
      };
      this.addLink(new Link("About", "../json/test-about.json"));
      this.addLink(new Link("States", "../json/test-states.json"));
      this.addLink(new Link("Cities", "../json/test-cities.json"));
      this.addLink(new Link("Neighborhoods", "../json/test-neighborhoods.json"));
      this.isActive = function(pageName){
        return $rootScope.currentPage === pageName;
      };
  }]);

  app.controller('contentController',[ '$rootScope',function($rootScope){
    this.showContent = function(category){
       return true;
      //return $rootScope.data['category'] === category;
    };
  }]);

  app.controller('tableController',[ '$scope', function($scope){
     
    this.tableData = [    
      {
        "City": "Houston",
        "State": "Texas"
      },
      {
        "City": "Austin",
        "State": "Texas"
      },
      {
        "City": "Dallas",
        "State": "Texas"
      },
      {
        "City": "New York City",
        "State": "New York"
      },
      {
        "City": "Los Angeles",
        "State": "California"
      }
      
    ];
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
    this.buildTable = function() {
      this.resetTable();
      //get the property names from the first element
      for( var o in this.tableData[0] ) {
        this.addHeader(o);
      };
      //for each row, build and add
      for(var rowData in this.tableData) {
        var newRow = this.tableData[rowData];
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
  }]);

  app.controller('mapController',['$rootScope', '$sce', function($rootScope, $sce){
    this.mapSrcBuilder = function(data = $rootScope.data) {
      var embedKey = "AIzaSyCADkkH1GoSKSlgVxk_oyLp6roM6XEx44I"
      var q = "";
      if (data.hasOwnProperty("neighborhood") && data["neighborhood"]){
        q += data["neighborhood"].replace(/ /g, "+");
        q += ',';
      };
      if (data.hasOwnProperty("city") && data["city"]){
        q += data["city"].replace(/ /g, "+");
        q += ',';
      };
      if (data.hasOwnProperty("state") && data["state"]){
        q += data["state"].replace(/ /g, "+");
        q += ',';
      };
      // var src = "https://maps.googleapis.com/maps/api/staticmap?center=";
      // src += q;
      // src += "&zoom=14&size=400x400&key=";
      // src += embedKey;
      var src = "https://www.google.com/maps/embed/v1/place?key="
      src += embedKey;
      src += "&q=";
      src += q;
      console.log(src);

      var x ="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6509713.084021231!2d-123.77347912442343!3d37.1866687017569!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x808fb9fe5f285e3d%3A0x8b5109a227086f55!2sCalifornia!5e0!3m2!1sen!2sus!4v1458871633347"
      return $sce.trustAsResourceUrl(x);
    };
  }]);

  function Link(display, ref) {
    this.display = display;
    this.ref = ref;
  };

})();
