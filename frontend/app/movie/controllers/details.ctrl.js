angular.module("movieCatalogue")
    .controller("MovieDetailsController", MovieDetailsController);

MovieDetailsController.$inject = ["movieService", "$routeParams"];

function MovieDetailsController(movieService, $routeParams) {

    var vm = this;

    activate();

    function activate() {
        vm.editor = false;
        vm.data = movieService.movieStorage;

        vm.toggleEditor = toggleEditor;
        vm.deleteMovie = deleteMovie;
        vm.updateMovie = updateMovie;
        movieService.fetchMovieDetails($routeParams.movieId);
    }

    function deleteMovie(){
        movieService.deleteMovie($routeParams.movieId);
    }

    function updateMovie(){
        movieService.updateMovie($routeParams.movieId, vm.editedMovie);
    }

    function toggleEditor(){
        // operate with a copy of movie from MovieStorage
        vm.editedMovie = {
            id: vm.data.movie.id,
            name: vm.data.movie.name,
            description: vm.data.movie.description,
            add_timestamp: vm.data.movie.add_timestamp

        };
        vm.editor = !vm.editor;
    }
}