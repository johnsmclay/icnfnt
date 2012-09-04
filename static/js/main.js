// Author: Thomas Davis <thomasalwyndavis@gmail.com>
// Filename: main.js

// Require.js allows us to configure shortcut alias
require.config({
  paths: {
    jquery: "libs/jquery/jquery-min",
    underscore: "libs/underscore/underscore-min",
    backbone: "libs/backbone/backbone-optamd3-min",
    //backbone: "libs/backbone/backbone-min",
    text: "libs/require/text",
    order: "libs/require/order"
  }

});

require([
  'underscore',
  'backbone',
  'views/app',
  'views/selected', 
  'views/download'
  ], function(_, Backbone, AppView, SelectedView, DownloadView){

  var vent = _.extend({}, Backbone.Events);

  var app_view = new AppView({vent: vent});
  var selected_view = new SelectedView({vent: vent});
  var download_view = new DownloadView({vent: vent});
});
