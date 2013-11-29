'use strict';

/* Filters */

angular.module('millibApp.filters', []).
    filter('reverse', function() {
        return function(items) {
            return items.slice().reverse();
        };
});