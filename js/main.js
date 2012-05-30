// Author: Thomas Davis <thomasalwyndavis@gmail.com>
// Filename: main.js

// Require.js allows us to configure shortcut alias
require.config({
  paths: {
    jquery: "libs/jquery/jquery-min",
    underscore: "libs/underscore/underscore-min",
    backbone: "libs/backbone/backbone-optamd3-min",
    text: "libs/require/text",
    order: "libs/require/order"
  }

});

require(['views/app', 'views/selected', 'views/download'], function(AppView, SelectedView, DownloadView){
  var app_view = new AppView;
  var selected_view = new SelectedView;
  var download_view = new DownloadView;
});
