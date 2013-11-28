'use strict';

/* Controllers */

angular.module('millibApp.controllers', []).
  controller('DashboardCtrl', [function() {

        /* Inspired by Lee Byron's test data generator. */
        function stream_layers(n, m, o) {
            if (arguments.length < 3) o = 0;
            function bump(a) {
                var x = 1 / (.1 + Math.random()),
                    y = 2 * Math.random() - .5,
                    z = 10 / (.1 + Math.random());
                for (var i = 0; i < m; i++) {
                    var w = (i / m - y) * z;
                    a[i] += x * Math.exp(-w * w);
                }
            }
            return d3.range(n).map(function() {
                var a = [], i;
                for (i = 0; i < m; i++) a[i] = o + o * Math.random();
                for (i = 0; i < 5; i++) bump(a);
                return a.map(stream_index);
            });
        }


        /* Another layer generator using gamma distributions. */
        function stream_waves(n, m) {
            return d3.range(n).map(function(i) {
                return d3.range(m).map(function(j) {
                    var x = 20 * j / m - i / 3;
                    return 2 * x * Math.exp(-.5 * x);
                }).map(stream_index);
            });
        }

        function stream_index(d, i) {
            return {x: i, y: Math.max(0, d)};
        }


        function testData(stream_names, points_count) {
            var now = new Date().getTime(),
                day = 1000 * 60 * 60 * 24, //milliseconds
                days_ago_count = 60,
                days_ago = days_ago_count * day,
                days_ago_date = now - days_ago,
                points_count = points_count || 45, //less for better performance
                day_per_point = days_ago_count / points_count;
            return stream_layers(stream_names.length, points_count, .1).map(function(data, i) {
                return {
                    key: stream_names[i],
                    values: data.map(function(d,j){
                        return {
                            x: days_ago_date + d.x * day * day_per_point,
                            y: Math.floor(d.y * 100) //just a coefficient
                        }
                    })
                };
            });
        }


        nv.addGraph(function() {
            var chart = nv.models.lineChart()
                .margin({top: 0, bottom: 25, left: 25, right: 0})
                //.showLegend(false)
                .color([
                    '#cf6d51', '#618fb0', '#61b082'
                ]);

            chart.legend.margin({top: 3});

            chart.yAxis
                .showMaxMin(false)
                .tickFormat(d3.format(',.f'));

            chart.xAxis
                .showMaxMin(false)
                .tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)) });
            var data = testData(['24h average', 'ask', 'bid', 'last', 'total volume'], 30);
            data[0].area = true;
            d3.select('#visits-chart svg')
                .datum(data)
                .transition().duration(500)
                .call(chart);

            nv.utils.windowResize(chart.update);
            return chart;
        });

    }])
  .controller('AboutCtrl', [function() {

  }]);