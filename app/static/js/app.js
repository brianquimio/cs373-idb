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
      this.addLink(new Link("About", "/app/static/json/test-about.json"));
      this.addLink(new Link("States", "/app/static/json/test-states.json"));
      this.addLink(new Link("Cities", "/app/static/json/test-cities.json"));
      this.addLink(new Link("Neighborhoods", "/app/static/json/test-neighborhoods.json"));
      this.isActive = function(pageName){
        return $rootScope.currentPage === pageName;
      };
  }]);

  app.controller('contentController',[ '$rootScope',function($rootScope){
    this.showContent = function(category){
      // return false;
      return $rootScope.data['category'] === category;
    };
  }]);

  app.controller('tableController',[ '$rootScope', function($rootScope){
    this.showColumn = function (subCategory, depth) {
      this.depth = this.showHelper(subCategory);
      return this.depth >= depth;
    };
    this.showHelper = function(subCategory){
      if (subCategory === "neighborhood") return 3;
      if (subCategory === "city") return 2;
      if (subCategory === "state") return 1;
      return 0;
    };
  }]);

  app.controller('mapController',['$rootScope', function($rootScope){

  }]);

  function Link(display, ref) {
    this.display = display;
    this.ref = ref;
  };

})();
