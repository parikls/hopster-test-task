angular.module("movieCatalogue")
    .factory("authService", authService);

authService.$inject = ["$http", "$location", "messageService"];

function authService($http, $location, messageService) {
    var service = {};

    service.login = login;
    service.logout = logout;
    service.getAuthHeader = getAuthHeader;

    service.authHeader = null;

    return service;

    function login(credentials){
        $http({
            method: "POST",
            url: "/api/auth/login/",
            data: $.param(credentials),
            headers: {"Content-Type": "application/x-www-form-urlencoded"}
        }).then(function success(response){

            messageService.errorAuth(null);
            service.authHeader = "Bearer " + response.headers("JWT");
            localStorage.setItem("JWT", service.authHeader);
            $location.path("/movie")
        }, function error(response){
            messageService.errorAuth(response.data.message);
        })
    }

    function logout() {

    }

    function getAuthHeader(){

        if (!service.authHeader){
            var localStorageJWT = localStorage.getItem("JWT");
            if (localStorageJWT) {
                service.authHeader = localStorageJWT;
            }
        }
        return service.authHeader;
    }
}