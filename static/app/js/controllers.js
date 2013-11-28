'use strict';

/* Controllers */

angular.module('millibApp.controllers', []).
  controller('DashboardCtrl', ['$http', '$scope', function($http, $scope) {
        $scope.btcLogs = [];
        $scope.lastTimestamp = 0;
        $http.post('/get_btc_logs', {since: $scope.lastTimestamp}).success(function(data) {
            var formatedBtcLogs = [];
            angular.forEach(data.btc_logs, function(item) {
                item.date = new Date(item.ts * 1000);
                formatedBtcLogs.push(item);
            });
            $scope.btcLogs = formatedBtcLogs;
            $scope.lastTimestamp = $scope.btcLogs[$scope.btcLogs.length-1].ts;
        });

        var chartLines = ['24h_avg', 'ask', 'bid', 'last', 'total_vol'];

        $scope.chartData = [
            {
                "key": "24H average",
                "values": []
            },
            {
                "key": "ask",
                "values": []
            },
            {
                "key": "bid",
                "values": []
            },
            {
                "key": "last",
                "values": []
            },
            {
                "key": "total volume",
                "values": []
            }
        ];

        $scope.$watch('btcLogs', function (value) {
            var newChartData = angular.copy($scope.chartData);
            angular.forEach(value, function(item) {
                angular.forEach(chartLines, function(line, place) {
                    var val = [item.date, item[line]];
                    newChartData[place].values.push(val);
                });
            });
            $scope.chartData = newChartData;
        });

        $scope.xAxisTicksFunction = function(){
            console.log('xAxisTicksFunction');
            console.log(d3.svg.axis().ticks(d3.time.minutes, 5));
            return function(d){
                return d3.svg.axis().ticks(d3.time.minutes, 5);
            }
        };

        $scope.xAxisTickFormatFunction = function(){
            return function(d){
                return d3.time.format('%H:%M')(moment.unix(d).toDate());
            }
        };
    }])
  .controller('AboutCtrl', [function() {

  }]);