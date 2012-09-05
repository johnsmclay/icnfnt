'use strict';

var icnfnt = angular.module('icnfnt', ['icnfnt.filters', 'icnfnt.services']);

icnfnt.config(['$routeProvider', function($routeProvider, $anchorScroll) {
    $routeProvider.when('/', {templateUrl: 'app/partials/partial1.html', controller: FontBuilderCtrl});
    //$routeProvider.otherwise({redirectTo: '/view1'});
  }]);
