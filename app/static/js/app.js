(function(){
  var app = angular.module('VASapp',['VAScontrollers','ngRoute']);

  app.config(function($routeProvider,$locationProvider) {
    $routeProvider.
      when('/states', {
        templateUrl: "PARTIALS/states.html",
        controller: "tableCtrl",
        controllerAs: "table",
        caseInsensitiveMatch: true
      }).
      when('/cities', {
        templateUrl: "PARTIALS/states.html",
        controller: "tableCtrl",
        controllerAs: "table",
        caseInsensitiveMatch: true
      }).
      when('/neighborhoods', {
        templateUrl: "PARTIALS/states.html",
        controller: "tableCtrl",
        controllerAs: "table",
        caseInsensitiveMatch: true
      }).
      when('/about', {
        templateUrl: "about.html",
        controller: "aboutCtrl",
        caseInsensitiveMatch: true
      }).
      when('/index.html', {
        redirectTo: '/'
      }).
      when('/:state', {
        template: "someState.html",
        controller: "tableCtrl",
        controllerAs: "table",
        caseInsensitiveMatch: true
      }).
      when('/:state/:city', {
        template: "someCity.html",
        controller: "tableCtrl",
        caseInsensitiveMatch: true
      }).
      when('/:state/:city/:neighborhood', {
        template: "someNeighborhood.html",
        controller: "tableCtrl",
        caseInsensitiveMatch: true
      }).
      when('/', {
        templateUrl: "PARTIALS/index.html",
        controller: "splashCtrl",
        caseInsensitiveMatch: true
      }).
      otherwise({
        redirectTo: '/'
      });

    $locationProvider.html5Mode(true);
  });

})();
