// Copyright 2012 Grant Gordon
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to permit
// persons to whom the Software is furnished to do so, subject to the
// following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
// NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
// USE OR OTHER DEALINGS IN THE SOFTWARE.

'use strict';

/* Directives */

angular.module('icnfnt.directives', [])

.directive('tooltip', function () {
    return {
        restrict:'A',
        link: function postLink(scope, element, attrs)
        {
            var el = $(element);
            //var title = el.attr('class');
            //el.attr('title',title);
            el.attr('title',".icon-" + scope.$eval(attrs.tooltip));
            el.tooltip({title: "ohai"});
        }
    }
})

.directive('icnSpinner', function() {
    return {
        restrict: 'A',
        replace: true,
        link: function(scope, element, attrs) {
            var spinner = new Spinner(smallSpinnerOpts).spin();
            //element[0].appendChild(spinner);
            $(element[0]).prepend(spinner.el);
        }
    };
});

var smallSpinnerOpts = {
  lines: 9, // The number of lines to draw
  length: 5, // The length of each line
  width: 4, // The line thickness
  radius: 6, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 0, // The rotation offset
  color: '#eee', // #rgb or #rrggbb
  speed: 1, // Rounds per second
  trail: 60, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: true, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: '0', // Top position relative to parent in px
  left: '0' // Left position relative to parent in px
};