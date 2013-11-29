'use strict';

/* Controllers */

angular.module('millibApp.controllers', []).
  controller('DashboardCtrl', ['$http', '$scope', '$timeout', function($http, $scope, $timeout) {
        $scope.btcLogs = [];
        $scope.newBtcLogs = [];
        $scope.lastTimestamp = 0;

        var updateBtcLogs = function () {
            $http.post('/get_btc_logs', {since: $scope.lastTimestamp}).success(function(data) {
                console.log(data.btc_logs.length);
                if(data.btc_logs.length) {
                    var formatedBtcLogs = [];
                    angular.forEach(data.btc_logs, function(item) {
                        item.date = new Date(item.ts * 1000);
                        formatedBtcLogs.push(item);
                    });
                    $scope.newBtcLogs  = formatedBtcLogs;
                    $scope.lastTimestamp = $scope.newBtcLogs[$scope.newBtcLogs.length-1].ts;

                    var btcLogs = angular.copy($scope.btcLogs);
                    angular.forEach($scope.newBtcLogs, function(v) { btcLogs.push(v)});
                    $scope.btcLogs = btcLogs;
                }
            });

            $timeout(updateBtcLogs, 5000);
        };

        updateBtcLogs();

        var chartLines = ['24h_avg', 'ask', 'bid', 'last'];//, 'total_vol'];

        $scope.chartData = [
            {
                "key": "24H average",
                "values": []
            },
            {
                "key": "ask",
                "values": [],
                "area": true
            },
            {
                "key": "bid",
                "values": []
            },
            {
                "key": "last",
                "values": []
            }
            /*
            ,
            {
                "key": "total volume",
                "values": []
            }
            */
        ];

        $scope.$watch('newBtcLogs', function (value) {
            var newChartData = angular.copy($scope.chartData);
            angular.forEach(value, function(item) {
                angular.forEach(chartLines, function(line, place) {
                    var val = [item.ts, item[line]];
                    newChartData[place].values.push(val);
                });
            });
            $scope.chartData = newChartData;
        });

        $scope.xAxisTickFormatFunction = function(){
            return function(d){
                return d3.time.format('%b %d %I:%M %p')(moment.unix(d).toDate());
            }
        };

    }])
  .controller('AboutCtrl', [function() {

  }]);