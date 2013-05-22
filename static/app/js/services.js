'use strict';

/* Services */
angular.module('icnfnt.services', ['ngResource']).
    factory('Glyph', function($resource){
  return $resource('app/data/glyphs.json', {}, {
    query: {method:'GET', isArray:true},
  });
});