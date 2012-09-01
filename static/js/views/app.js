define([
  "order!jquery",
  "order!underscore", 
  "order!backbone",
  "collections/glyphs",
  "views/glyphs",
  "order!bootstrapjs/bootstrap-tooltip"
  ], function($, _, Backbone, Glyphs, GlyphView, bootstraptooltip){
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#glyphapp"),

    // Delegated events for creating new items, and clearing completed ones.
    events: {
      "click .js-btn-all":  "selectAll",
      "click .js-btn-none": "selectNone"
    },

    // At initialization we bind to the relevant events on the `Glyphs`
    // collection, when glyphs are added or changed. Kick things off by
    // loading any preexisting glyphs that might be saved in *localStorage*.
    initialize: function() {
      _.bindAll(this, 'addOne', 'addAll');

      Glyphs.bind('add',     this.addOne);
      Glyphs.bind('reset',   this.addAll);

      Glyphs.fetch();
    },

    render: function() {
    },

    // Add a single todo item to the list by creating a view for it, and
    // appending its element to the `<ul>`.
    addOne: function(glyph) {
      var view = new GlyphView({model: glyph});
      this.$("#glyph-list").append(view.render().el);
    },

    // Add all items in the **Glyphs** collection at once.
    addAll: function() {
      Glyphs.each(this.addOne);
      $(".glyph").tooltip({placement: "bottom"});
    },

    selectAll: function(evt) {
      evt.preventDefault();
      Glyphs.selectAll();
      _gaq.push(['_trackEvent', 'Glyphs', 'Select All']);
    },

    selectNone: function(evt) {
      evt.preventDefault();
      Glyphs.selectNone();
      _gaq.push(['_trackEvent', 'Glyphs', 'Select None']);
    }

  });
  return AppView;
});
