define([
  'jquery', 
  'underscore', 
  'backbone',
  'text!templates/glyphs.html'
  ], function($, _, Backbone, glyphsTemplate){
  var GlyphView = Backbone.View.extend({

    //... is a list tag.
    tagName:  "li",

    // Cache the template function for a single item.
    template: _.template(glyphsTemplate),

    // The DOM events specific to an item.
    events: {
      "click"  : "toggleSelected"
    },

    // The GlyphView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Glyph** and a **GlyphView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      _.bindAll(this, 'render');
      this.model.bind('destroy', this.remove);
      this.model.bind('change', this.render);
    },

    // Re-render the contents of the todo item.
    render: function() {
      if (this.model.get("selected")) {
        $(this.el).addClass("selected");
      } else if (!this.model.get("selected")) {
        $(this.el).removeClass("selected");
      }
      $(this.el).html(this.template(this.model.toJSON()));
      $(this.el).attr("title", ".icon-" + this.model.get('name'));
      $(this.el).addClass("glyph");
      return this;
    },

    // Toggle the `"selected"` state of the model.
    toggleSelected: function(evt) {
      this.model.toggle();
      this.render();
    },

  });
  return GlyphView;
});
