'use strict';

angular.module("movieCatalogue", ["ngResource", "ngRoute"]);

angular
    .module("movieCatalogue")
    .config(
        ["$resourceProvider",
        function($resourceProvider){
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }
        ]
    );
