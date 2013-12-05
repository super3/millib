'use strict';

/* Controllers */

angular.module('millibApp.controllers', []).
  controller('DashboardCtrl', ['$http', '$scope', '$timeout', function($http, $scope, $timeout) {
        $scope.btcLogs = [];

        $scope.newBtcLogs = [];
        $scope.lastTimestamp = 0;
        $scope.currencyPairs = [
            {
                name: "BTC/USD",
                rate: 1,
                roundDigits: 2
            },
            {
                name: "mBTC/USD",
                rate: 0.001,
                roundDigits: 4
            }
        ];

        $scope.currencyPair = $scope.currencyPairs[0];

        var updateBtcLogs = function () {
            $http.post('/get_btc_logs', {since: $scope.lastTimestamp}).success(function(data) {
                console.log(data.btc_logs.length);
                if(data.btc_logs.length) {
                    var formatedBtcLogs = [];
                    angular.forEach(data.btc_logs, function(item) {
                        item.date = new Date(item.ts * 1000);
                        formatedBtcLogs.push(item);
                    });
                    $scope.newBtcLogs = formatedBtcLogs;
                    var btcLogs = angular.copy($scope.btcLogs);
                    angular.forEach($scope.newBtcLogs, function(v) { btcLogs.push(v)});
                    $scope.btcLogs = btcLogs;
                    $scope.btcLogsConverted = convertData($scope.btcLogs, $scope.currencyPair);
                }
            });

            $timeout(updateBtcLogs, 5000);
        };

        updateBtcLogs();

        var currencyFields = ['ask', 'bid', 'last'];//, 'total_vol'];

        var initialChartData = [
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

        $scope.$watch('btcLogsConverted', function (value) {
            if(value && value.length) {
                $scope.lastBtcLog = value[value.length-1];
                $scope.lastTimestamp = $scope.lastBtcLog.ts;

                var newChartData = angular.copy(initialChartData) ;
                angular.forEach(value, function(item) {
                    angular.forEach(currencyFields, function(field, place) {
                        var val = [item.ts, item[field]];
                        newChartData[place].values.push(val);
                    });
                });
                $scope.chartData = newChartData;
            }
        });

        var convertData = function (data, currency) {
            var convertedData = [];
            angular.forEach(angular.copy(data), function(item) {
                angular.forEach(currencyFields, function(field, place) {
                    var val = item[field] * currency.rate;
                    item[field] = parseFloat(val.toFixed(currency.roundDigits));
                });
                convertedData.push(item);
            });
            return convertedData;
        }

        $scope.$watch('currencyPair', function (val) {
            if ($scope.btcLogs.length && val) {
                $scope.btcLogsConverted = convertData($scope.btcLogs, val);
            }
        });

        $scope.xAxisTickFormatFunction = function(){
            return function(d){
                return d3.time.format('%I:%M %p')(moment.unix(d).toDate());
            }
        };

    }])
  .controller('AboutCtrl', [function() {

  }]);