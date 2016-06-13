var gulp = require('gulp');
var shell = require('gulp-shell');
var exec = require('child_process').exec;

// gulp.task('run-tests', shell.task([
//     'python3 manage.py test'
// ]));

gulp.task('watch', function() {
    // gulp.watch(['./presto/**/*.html', './presto/**/*.py'], ['run-tests']);
    gulp.watch(['./presto/**/*.html', './presto/**/*.py'])
        .on('change', function(file) {
            path_split = file.path.split('/');
            filename = path_split[path_split.length - 1];
            filename = filename.split('.')[0];
            is_test = filename.split('_')[0];

            if (is_test == 'test') {
                exec('python manage.py tests ' + filename, function(err, stdout, stderr) {
                    console.log(stdout);
                    console.log(stderr);
                });
            } else {
                exec('python3 manage.py test', function(err, stdout, stderr) {
                    console.log(stdout);
                    console.log(stderr);
                });
            }
        });
});

// gulp.task('default', ['run-tests', 'watch']);
gulp.task('default', ['watch']);
