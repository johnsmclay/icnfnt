define([
  'underscore', 
  'backbone', 
  'models/glyph'
  ], function(_, Backbone, Glyph){
	  
	var GlyphsCollection = Backbone.Collection.extend({

    // Reference to this collection's model.
    model: Glyph,

    // Fetch all the glyphs from the server
    //url: 'js/fontawesome.json',

    // Filter down the list of all glyphs that are selected.
    selected: function() {
      
      // I'm sidestepping the tradition collection -> json convention
      // because I can't seem to get it to actually serialize *just* the
      // glyphs that have been selected.
      var selectedGlyphs = [];
      this.each(function(glyph){
        if (glyph.get("selected") === true) {
          selectedGlyphs.push(glyph.getVanilla());
        }
      });
      return selectedGlyphs;
    },

    comparator: function(glyph) {
      return glyph.get("name");
    },

    // Filter down the list to only glyphs that are not selected.
    remaining: function() {
      return this.without.apply(this, this.selected());
    },

    selectAll: function() {
      this.each(function(glyph){
        glyph.set({"selected": true});
      });
    },

    selectNone: function() {
      this.each(function(glyph){
        glyph.set({"selected": false});
      });
    },

    checkForSelected: function() {
      var count = 0;

      this.each(function(glyph){
        if (glyph.attributes.selected)
          count++;
      });

      if (count > 0) {
        return true;
      } else {
        return false;
      }
    }

  });
  return new GlyphsCollection;
});
