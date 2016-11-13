angular.module("movieCatalogue")
    .factory("movieService", movieService);

movieService.$inject = ["$http", "$location", "authService", "messageService"];

function movieService($http, $location, authService, messageService) {
    var service = {};

    service.fetchMovies = fetchMovies;
    service.fetchMovieDetails = fetchMovieDetails;
    service.createMovie = createMovie;
    service.updateMovie = updateMovie;
    service.deleteMovie = deleteMovie;

    service.initalized = false;
    service.movieStorage = {
        movieList: [],
        movie: null
    };

    return service;

    function fetchMovies() {
        if (!(service.initalized)) {
            $http({
                method: "GET",
                url: "/api/movie/",
                headers: {"Authorization": authService.getAuthHeader()}
            }).then(function success(response) {
                service.movieStorage.movieList = response.data;
                service.initalized = true;
            }, function error(response) {
                if (response.status == 401) {
                    messageService.errorAuth("Session expired!");
                    $location.path("/login")
                }
            })
        }

    }

    function fetchMovieDetails(movieId) {
        $http({
            method: "GET",
            url: "/api/movie/" + movieId + "/",
            headers: {"Authorization": authService.getAuthHeader()}
        }).then(function success(response) {
            service.movieStorage.movie = response.data;
        }, function error(response) {
            // handle 401 here
            if (response.status == 401) {
                messageService.errorAuth("Session expired!");
                $location.path("/login")
            }
        })
    }

    function createMovie(movie) {
        console.log("http");
        $http({
            method: "POST",
            url: "/api/movie/",
            data: $.param(movie),
            headers: {
                "Authorization": authService.getAuthHeader(),
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }).then(function success(response) {

            if (response.status == 201) {
                // add movie to storage on 201 response
                service.movieStorage.movieList.unshift(response.data);
                messageService.errorMovie(null);
            }

            $location.path("/movie")
        }, function error(response) {
            if (response.status == 401) {
                messageService.errorAuth("Session expired!");
                $location.path("/login")
            } else {
                messageService.errorMovie(response.data.message);
            }
        })
    }

    function deleteMovie(movieId) {
        $http({
            method: "DELETE",
            url: "/api/movie/" + movieId + "/",
            headers: {"Authorization": authService.getAuthHeader()}
        }).then(function success(response) {
            for (var i=0; i<service.movieStorage.movieList.length; i++){
                if (service.movieStorage.movieList[i].id == movieId){
                    service.movieStorage.movieList.splice(i, 1);
                }
            }
            $location.path("/movie");
        }, function error(response) {
            if (response.status == 401) {
                messageService.errorAuth("Session expired!");
                $location.path("/login")
            }
        })
    }

    function updateMovie(movieId, movie) {
        console.log(movie);
        $http({
            method: "POST",
            url: "/api/movie/" + movieId + "/",
            data: $.param(movie),
            headers: {
                "Authorization": authService.getAuthHeader(),
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }).then(function success(response) {
            for (var i=0; i<service.movieStorage.movieList.length; i++){
                if (service.movieStorage.movieList[i].id == movieId){
                    service.movieStorage.movieList[i] = movie;
                }
            }
            messageService.errorMovie(null);
            $location.path("/movie");
        }, function error(response) {
            if (response.status == 401) {
                messageService.errorAuth("Session expired!");
                $location.path("/login")
            }
        })
    }

}