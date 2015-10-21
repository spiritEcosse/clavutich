module.exports = (grunt) ->
  grunt.initConfig(
    pkg: grunt.file.readJSON('package.json')
    min:
      dist:
        src: ['node_modules/jquery/dist/jquery.min.js',
              'node_modules/bootstrap/dist/js/bootstrap.min.js',
              'static/src/js/**/*.js'],
        dest: 'static/build/js/script.min.js'
    cssmin:
      dist:
        src: ['static/src/css/**/*.css',
              'node_modules/font-awesome/css/font-awesome.css'],
        dest: 'static/build/css/style.min.css'
  )

  grunt.loadNpmTasks('grunt-yui-compressor')

