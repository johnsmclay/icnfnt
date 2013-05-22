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
"use strict";angular.module("icnfnt.directives",[]).directive("tooltip",function(){return{restrict:"A",link:function(t,n,r){var i=$(n);i.attr("title",".icon-"+t.$eval(r.tooltip));i.tooltip({title:"ohai"})}}}).directive("icnSpinner",function(){return{restrict:"A",replace:!0,link:function(e,t,n){var r=(new Spinner(smallSpinnerOpts)).spin();$(t[0]).prepend(r.el)}}});var smallSpinnerOpts={lines:9,length:5,width:4,radius:6,corners:1,rotate:0,color:"#eee",speed:1,trail:60,shadow:!1,hwaccel:!0,className:"spinner",zIndex:2e9,top:"0",left:"0"};