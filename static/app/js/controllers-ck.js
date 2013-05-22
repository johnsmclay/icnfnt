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
"use strict";function FontBuilderCtrl(e,t,n,r){e.loading=!1;e.categories={"Web Application Icons":[],"Text Editor Icons":[],"Video Player Icons":[],"Directional Icons":[],"Brand Icons":[],"Medical Icons":[]};e.compact=!1;e.about=!1;e.filtering=!1;e.selected=[];e.glyphs=t.query(function(t){angular.forEach(t,function(t,n){t.selected=!1;e.categories[t.categories[0]].push(t)});console.log(e.categories)});e.toggleGlyphSelected=function(t){t.selected=!t.selected;t.selected?e.selected.push(t):e.selected.splice(e.selected.indexOf(t),1)};e.selectAll=function(t){if(!t){e.selected=[];angular.forEach(e.glyphs,function(t){t.selected=!0;e.selected.push(t)})}};e.selectNone=function(){angular.forEach(e.selected,function(e){e.selected=!1});e.selected=[]};e.toggleLoading=function(){console.log("changing loading from: "+e.loading+" -> "+!e.loading);e.loading=!e.loading};e.downloadNow=function(){if(e.selected.length>0){e.toggleLoading();var t=$.param({json_data:JSON.stringify(e.selected)});r({url:"/api/createpack",data:t,method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"}}).success(function(t,n){e.toggleLoading();_gaq.push(["_trackEvent","Download","Success"]);window.location.href=t}).error(function(t,n){e.toggleLoading();alert("There was a problem creating your icon pack.  Please try again.")})}else{alert("Please select at least one icon.");_gaq.push(["_trackEvent","Download","Rejected - No glyphs selected."])}};e.scrollToAbout=function(){$.smoothScroll({scrollTarget:".megafooter"})}}Array.prototype.unique=function(){var e={},t,n=this.length,r=[];for(t=0;t<n;t+=1)e[this[t]]=this[t];for(t in e)e[t]!=""&&r.push(e[t]);return r};