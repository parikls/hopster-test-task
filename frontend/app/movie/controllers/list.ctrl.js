angular.module("movieCatalogue")
    .controller("MovieController", MovieController);

MovieController.$inject = ["movieService", "messageService"];

function MovieController(movieService, messageService) {

    var vm = this;

    activate();

    function activate() {
        vm.data = movieService.movieStorage;
        vm.messages = messageService.messages;

        // fetch movies on init
        movieService.fetchMovies();
    }
}