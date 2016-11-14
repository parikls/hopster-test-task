var gulp = require('gulp');
var concat = require('gulp-concat');


function build_directory_list(dir, depth){
    var result = [],
        path = "";

    for (var i=0; i<depth; i++){
        result.push(dir + path + "*.js");
        path = path + "**/";
    }

    return result;
}

gulp.task('js', function () {
    var dirs = build_directory_list("app/", 5);
    gulp.src(dirs)
        .pipe(concat('bundle.js'))
        .pipe(gulp.dest('../backend/static/js/'))
});

gulp.task("watch", ["js"], function () {

    var dirs = build_directory_list("app/", 5);

    dirs.forEach(function(element, index, array){
        gulp.watch(element, ["js"]);
    })

});