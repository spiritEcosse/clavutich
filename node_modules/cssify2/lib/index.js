var through = require('through');

module.exports = function(file) {
	
	if (!/\.css/.test(file)) return through();
	
	var source = "";
	
	return through(function(chunk) {
	    source += chunk.toString();
	},
	function() {
		
		var css = source.replace(/\"/g, "\\\"").replace(/\n/g, "\\\n");
		var compiled = "var css = '" + css + "'; (require('cssify2'))(css); module.exports = css;";
		
		this.queue(compiled);
		this.queue(null);
  	});
};