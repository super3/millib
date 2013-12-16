'use strict';

angular.module('millibApp', [
    'nvd3ChartDirectives',
    'ngRoute',
    'millibApp.filters',
    'millibApp.services',
    'millibApp.directives',
    'millibApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/dashboard', {templateUrl: '/app/partials/dashboard.html', controller: 'DashboardCtrl'});
    $routeProvider.when('/about', {templateUrl: '/app/partials/about.html', controller: 'AboutCtrl'});
    $routeProvider.otherwise({redirectTo: '/dashboard'});
}]).run(function($rootScope, $location) {

    $rootScope.$location = $location;
});

$('.dropdown-toggle').dropdown();