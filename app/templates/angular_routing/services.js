(function(){
  var app = angular.module('VASservices',['ngResource']);

  app.factory('getAPIResponse', ['$http', function($http){
    
  }]);

  app.factory('tableDataFactory', ['$http', function($http){
    return {
      "rows":
      [
        {
          "data":1
        },
        {
          "data":2
        },
        {
          "data":3
        }
      ]
    };
  }]);

})();
