module.exports = (grunt) ->
  grunt.initConfig(
    pkg: grunt.file.readJSON('package.json')
    coffee:
      files:
        src: [
          'clavutich/src/coffee/**/*.coffee',
          'catalog/src/coffee/**/*.coffee',
          'easy_cart/src/coffee/**/*.coffee',
        ],
        dest: 'static/src/js/clavutich/src/js/script.js'
    min:
      dist:
        src: [
          'static/bower_components/jquery/dist/jquery.min.js',
          'static/bower_components/bootstrap/dist/js/bootstrap.min.js',
          'static/bower_components/angular/angular.min.js',
          'static/bower_components/angular-animate/angular-animate.min.js',
          'static/bower_components/bootstrap-checkbox/dist/js/bootstrap-checkbox.js',
          'static/bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
          'static/bower_components/angular-scroll/angular-scroll.min.js',
          'static_root/djangular/js/django-angular.js',
          'static/src/highslide/highslide-with-gallery.js',
          'static/bower_components/loadcss/loadCSS.js',
          'static/bower_components/loadcss/onloadCSS.js',
          'static/src/js/**/*.js',
        ],
        dest: 'static/build/js/script.min.js'
    cssmin:
      dist:
        src: [
          'static/bower_components/font-awesome/css/font-awesome.css',
          'static_root/djangular/css/styles.css',
          'static/src/highslide/highslide.css',
          'static/src/css/**/*.css',
        ],
        dest: 'static/build/css/style.min.css'
  )

  grunt.loadNpmTasks('grunt-contrib-coffee')
  grunt.loadNpmTasks('grunt-yui-compressor')
  grunt.loadNpmTasks('grunt-contrib-imagemin')
  grunt.registerTask('default', ['coffee:files', 'min:dist', 'cssmin:dist'])

