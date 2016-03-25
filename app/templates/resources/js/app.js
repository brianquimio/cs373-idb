(function(){
  var app = angular.module('app', [ ]);
  app.controller('containerGenerator', function(){
    this.containers = [];
    this.containers.push(new container("'container-fluid regionTitleContainer'","SomeName", null));
    this.containers.push(new container("'container-fluid dataContainer'","SomeName","SomeContent"));
    this.containers.push(new container("'container-fluid dataContainer'","SomeName2","SomeContent1231"));

  });

  function getPageData(uri){

    return null;
  };

  function container(classes, name, content){
    this.classes = classes;
    this.name = name;
    this.content = content;
  };

})();
