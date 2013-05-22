require('js-yaml');

// Get document, or throw exception on error
try {
  var doc = require('./newglyphs.yml');
  var glyphs = doc['icons'];
  glyphs.forEach(function(glyph){
  	delete glyph['name'];
  	delete glyph['created'];
  	//console.log("cleaning up: ", glyph.id)
  });
  console.log(JSON.stringify(glyphs, null, 2));
} catch (e) {
  console.log(e);
}