'use strict';

angular.module('troika').controller('CardController',
    function($scope, $http, $compile) {

  $scope.search = {};
  
  $scope.searchCards = function(search) {
    var troika_id_param = '';
    if (
      !angular.isUndefined(search) 
      && !angular.isUndefined(search.troika_id) 
      && search.troika_id.length)
        troika_id_param = '?troika_id=' + search.troika_id;
        
    angular.element(location).attr('href','/card/' + troika_id_param);
  };
});
