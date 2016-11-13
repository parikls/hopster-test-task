angular.module("movieCatalogue")
    .controller("MovieController", MovieController);

MovieController.$inject = ["movieService"];

function MovieController(movieService) {

    var vm = this;

    activate();

    function activate() {
        vm.data = movieService.movieStorage;

        // fetch movies on init
        movieService.fetchMovies();
    }
}