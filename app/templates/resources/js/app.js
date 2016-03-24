(function(){
  var app = angular.module('app', [ ]);
  app.controller('containerGenerator', function(){
    this.containers = [];
    this.containers.push(new container("'container-fluid regionTitleContainer'","SomeName", null, false));
    this.containers.push(new container("'container-fluid dataContainer'","SomeName","SomeContent",true));
    this.containers.push(new container("'container-fluid dataContainer'","SomeName2","SomeContent1231",true));

  });

  // var dataContainer = {
  //   classes : "container-fluid dataContainer",
  //   name : "SomeName",
  //   content : "Some Data"
  // };

  function container(classes, name, content, hasContent){
    this.classes = classes;
    this.name = name;
    this.content = content;
    this.hasContent = hasContent;
  };

})();
