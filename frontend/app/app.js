'use strict';

angular.module("movieCatalogue", ["ngResource", "ngRoute"]);

angular
    .module("movieCatalogue")
    .config(
        ["$resourceProvider",
            function ($resourceProvider) {
                $resourceProvider.defaults.stripTrailingSlashes = false;
            }
        ]
    )
    .run(function ($rootScope, $location, messageService) {
        $rootScope.$on("$locationChangeStart", function () {
            messageService.clearMessages();
        })
    });
