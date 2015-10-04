module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		constants: {
			tinyPngImgFiles: 'jpg,jpeg,png',
			resPath: 'static'
		},

		sass: {
			dist: {
				options: {
					outputStyle: 'compressed',
					cacheLocation: '<%= constants.resPath %>/sass/.sass-cache',
					sourceMap: true
				},
				files: {
					'<%= constants.resPath %>/css/style.css': '<%= constants.resPath %>/sass/style.scss'
				}
			}
		},

		uglify: {
			min: {
				files: {
					'<%= constants.resPath %>/js/main.min.js': '<%= constants.resPath %>/js/main.js'
				}
			}
		},

		watch: {
			css: {
				files: '<%= constants.resPath %>/sass/**/*.scss',
				tasks: ['sass'],
				options: {
					// Start a live reload server on the default port 35729
					livereload: true,
				},
			},
			scripts: {
				files: [
					'<%= constants.resPath %>/js/main.js',
				],
				tasks: ['uglify'],
				options: {
					debounceDelay: 10,
				},
			}
		}
	});

	// Load the plugin that provides the "sass" task.
	// grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-uglify');

	// Default task(s).
	grunt.registerTask('default', ['sass', 'uglify']);

};