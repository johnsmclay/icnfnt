'use strict';

// Create angular app
var icnfnt = angular.module('icnfnt', []);

icnfnt.config(['$routeProvider', function($routeProvider, $anchorScroll) {
	// Set up the route
    $routeProvider.when('/', {templateUrl: 'app/partials/partial1.html', controller: FontBuilderCtrl});
  }]);
