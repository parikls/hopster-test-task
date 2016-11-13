angular.module("movieCatalogue")
    .factory("messageService", messageService);


function messageService() {

    var service = {};

    service.errorAuth = errorAuth;
    service.errorMovie = errorMovie;

    service.messages = {
        movieErrorMessage: null,
        authErrorMessage: null
    };

    return service;

    function errorAuth(message){
        service.messages.authErrorMessage = message;
    }

    function errorMovie(message){
        service.messages.movieErrorMessage = message;
    }
}