'use strict';

angular.module('troika', []);

angular.module('troika').config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});