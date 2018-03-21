var gulp = require('gulp');
var sass = require('gulp-sass');
var concatcss = require('gulp-concat-css');
var foreach = require('gulp-foreach');
var replace = require('gulp-replace-path');



gulp.task('copy-amsterdam-source', function() {
   return gulp
       .src('node_modules/gemeente-amsterdam-patterns/source/**/*.*')
       .pipe(gulp.dest('raw-source'))
});

gulp.task('build-css', function() {
  return gulp
    .src('src/css/**/*.scss')
    .pipe(sass({
      includePaths: ['node_modules/']
    }))
    .pipe(concatcss('ams-stijl.css'))
    .pipe(replace(/(background-image: url\(")(.*)(\/images\/)/g, 'background-image: url("../images/'))
    .pipe(replace(/(background: url\(")(.*)(\/images\/)/g, 'background: url("../images/'))
    .pipe(replace('../../node_modules/gemeente-amsterdam-patterns/source', '../raw-source'))
    .pipe(gulp.dest('css'))
});

gulp.task('build-sass', function() {
  return gulp
    .src('src/scss/**/*.scss')
    .pipe(foreach(function (stream, file) {
        return stream
            .pipe(replace('../../node_modules/gemeente-amsterdam-patterns/source', '../raw-source'))
            .pipe(gulp.dest('scss'))
    }))
});

gulp.task('build-images', function() {
  return gulp
    .src(['raw-source/images/**/*.*', 'src/images/**/*.*'])
    .pipe(gulp.dest('images'))
});

gulp.task('clean', function(){
  return del('tmp/**', {force:true});
});

gulp.task('default', gulp.series('copy-amsterdam-source', 'build-css', 'build-sass', 'build-images'));
