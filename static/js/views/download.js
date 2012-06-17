define([
  'jquery',
  'underscore', 
  'backbone',
  'collections/glyphs',
  'libs/json2'
  ], function($, _, Backbone, Glyphs, Json2){
  var DownloadView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#download"),

    // Delegated events for creating new items, and clearing completed ones.
    events: {
      "click .btn-download": "downloadKit"
    },

    // Makes sure "this" is available throughout
    initialize: function() {
      _.bindAll(this);
    },

    render: function() {
    },

    // Send request to download font kit
    downloadKit: function(glyph) {
      //alert(JSON.stringify(Glyphs.selected()));
      $.ajax({
        url: "/api/createpack",
        type: 'POST',
        data: { 
            json_data: JSON.stringify(Glyphs.selected())
        },
        context: document.body
      }).done(function(url) { 
        window.location.href = url;
      });
    },

  });
  return DownloadView;
});
