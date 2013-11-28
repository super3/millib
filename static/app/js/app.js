'use strict';


// Declare app level module which depends on filters, and services
angular.module('millibApp', [
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
}]);
