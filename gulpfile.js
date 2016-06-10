var gulp = require('gulp');
var shell = require('gulp-shell')

gulp.task('run-tests', shell.task([
   'python3 manage.py test']))

gulp.task('watch', function(){
   gulp.watch(['./presto/**/*.html', './presto/**/*.py'], ['run-tests']);
});

gulp.task('default',['run-tests','watch']);
