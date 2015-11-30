/*jshint node: true*/

var fs = require("fs");
var assert = require("assert");
var sassify = require("../lib/index");

var templatePath = __dirname + "/hello.css";
var exported = __dirname + "/compiled.js";

try {
  fs.unlinkSync(exported);
} catch (err) { }

fs.createReadStream(templatePath)
.pipe(sassify(templatePath))
.pipe(fs.createWriteStream(exported))
.on("close", function() {
  var css = require(exported);
  console.log(css);
  // var res = template({ msg: "hi!" });
  // assert.equal(res, "<h1>hi!</h1>");
  console.log("ok");
});

