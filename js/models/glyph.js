define(['underscore', 'backbone'], function(_, Backbone) {
  var GlyphModel = Backbone.Model.extend({

    // Default attributes for the todo.
    defaults: {
      name: "icon",
      uni: "000",
      selected: false
    },

    // Ensure that each todo created has `name`.
    initialize: function() {
      if (!this.get("name")) {
        this.set({"name": this.defaults.content});
      }
      this.set({"selected": this.defaults.selected});
    },

    // Toggle the `selected` state of the glyph.
    toggle: function() {
      this.save({selected: !this.get("selected")});
      return this.selected;
    },

    // Remove this Glyph from *localStorage*.
    clear: function() {
      this.destroy();
    },

    // It seems like every model has a reference to every other model inside
    // so when try to convert a filtered collection to json you get every single
    // model in the collection instead of just the ones you want.

    // I made this function to sidestep that process
    // See also: collections/glyphs.getSelected()
    getVanilla : function() {
      var vanilla = {
        name: this.get("name"),
        uni:  this.get("uni")
      };
      return vanilla;
    }

  });
  return GlyphModel;
});
