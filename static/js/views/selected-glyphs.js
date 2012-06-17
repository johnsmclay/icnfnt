define([
  'jquery', 
  'underscore', 
  'backbone',
  'text!templates/selected-glyph.html'
  ], function($, _, Backbone, glyphsTemplate){
  var GlyphView = Backbone.View.extend({

    //... is a list tag.
    tagName:  "li",

    // Cache the template function for a single item.
    template: _.template(glyphsTemplate),

    // The DOM events specific to an item.
    events: {
      "click"  : "toggleSelected",
    },

    // The GlyphView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Glyph** and a **GlyphView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      _.bindAll(this, 'render');
      this.model.bind('change', this.render);
      this.model.bind('destroy', this.remove);
    },

    // Re-render the contents of the todo item.
    render: function() {
      // cache the jquery selector for efficiency
      var glyph = $(this.el);
      glyph.html(this.template(this.model.toJSON()));
      glyph.addClass("preview hide");
      if (this.model.get("selected")) {
        glyph.removeClass("hide");
      }
      return this;
    },

    // Toggle the `"selected"` state of the model.
    toggleSelected: function(evt) {
      this.model.toggle();
    },

  });
  return GlyphView;
});
