var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('js', function () {
    gulp.src(['app/*.js', "app/**/*.js", 'app/**/**/*.js', 'app/**/**/**/*.js'])
        .pipe(concat('bundle.js'))
        .pipe(gulp.dest('../backend/static/js/'))
});

gulp.task("watch", ["js"], function () {

    var depth = "**/";

    for (var i = 0; i < 5; i++) {
        gulp.watch("app/" + depth + "*.js", ["js"]);
        depth += "**/"

    }
});