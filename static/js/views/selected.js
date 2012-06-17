define([
  'order!jquery',
  'order!underscore', 
  'order!backbone',
  'collections/glyphs',
  'views/selected-glyphs'
  ], function($, _, Backbone, Glyphs, GlyphView){
  var SelectedView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#selected-view"),

    // Delegated events for creating new items, and clearing completed ones.
    events: {},

    // At initialization we bind to the relevant events on the `Glyphs`
    // collection, when glyphs are added or changed.
    initialize: function() {
      this.render();
      _.bindAll(this, 'render', 'addAll');
      Glyphs.bind('reset',        this.addAll);
    },

    // Re-rendering the App just means refreshing the statistics -- the rest
    // of the app doesn't change.
    render: function() {
      return this;
    },

    // Add a single todo item to the list by creating a view for it, and
    // appending its element to the `<ul>`.
    addOne: function(glyph) {
      var view = new GlyphView({model: glyph});
      this.$("#selected-glyph-list").append(view.render().el);
    },

    // Add all items in the **Glyphs** collection at once.
    addAll: function() {
      Glyphs.each(this.addOne);
    }

  });
  return SelectedView;
});
