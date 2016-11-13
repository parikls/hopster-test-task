angular.module("movieCatalogue")
    .controller("MovieCreationController", MovieCreationController);

MovieCreationController.$inject = ["movieService", "messageService"];

function MovieCreationController(movieService, messageService) {

    var vm = this;

    activate();

    function activate() {
        vm.submitForm = submitForm;
        vm.movieStorage = movieService.movieStorage;
        vm.messages = messageService.messages;
    }

    function submitForm() {
        if (vm.movie){
            movieService.createMovie(vm.movie);
        } else {
            messageService.errorMovie("Name and description fields must be filled");
        }
    }
}