'use strict';

/* Filters */

angular.module('millibApp.filters', []).
    filter('reverse', function() {
        return function(items) {
            if (items && items.length) {
                return items.slice().reverse();
            } else {
                return items;
            }
        };
});