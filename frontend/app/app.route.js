angular.module('movieCatalogue')
    .config(function ($routeProvider) {

        $routeProvider
            .when('/movie', {
                templateUrl: 'angular-templates/movie.html',
                controller: 'MovieController',
                controllerAs: 'vm'
            })
            .when('/movie/create', {
                templateUrl: 'angular-templates/movie-create.html',
                controller: 'MovieCreationController',
                controllerAs: 'vm'
            })
            .when('/movie/:movieId/', {
                templateUrl: 'angular-templates/movie-details.html',
                controller: 'MovieDetailsController',
                controllerAs: 'vm'
            })
            .when('/login', {
                templateUrl: 'angular-templates/login.html',
                controller: 'LoginController',
                controllerAs: 'vm'
            })
            .otherwise({
                redirectTo: '/login'
            });
    });