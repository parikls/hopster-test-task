var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('js', function () {
    gulp.src(['movie/*.js', "movie/**/*.js", 'movie/**/**/*.js', 'movie/**/**/**/*.js'])
        .pipe(concat('movie.js'))
        .pipe(gulp.dest('.'))
});

gulp.task("watch", ["js"], function () {

    var depth = "**/";

    for (var i = 0; i < 5; i++) {
        gulp.watch("movie/" + depth + "*.js", ["js"]);
        depth += "**/"

    }
});