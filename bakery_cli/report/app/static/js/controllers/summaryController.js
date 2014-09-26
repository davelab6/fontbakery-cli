myApp.controller('summaryController', function($scope, $http, summaryApi, Mixins) {
    $scope.charts = [];
    $scope.average_chart = null;
    $scope.tests = null;
    $scope.metrics = null;
    $scope.table_sizes = null;
    $scope.autohint_sizes = null;
    $scope.fontaine_fonts = null;
    $scope.fonts_orthography = null;
    $scope.fontSupportToStyle = {
        'full': 'success',
        'partial': 'info',
        'fragmentary': 'warning',
        'unsupported': 'danger'
    };

    summaryApi.getMetrics().then(function(response) {
        $scope.metrics = response.data;
    });
    summaryApi.getTableSizes().then(function(response) {
        $scope.table_sizes = response.data;
    });
    summaryApi.getAutohintSizes().then(function(response) {
        $scope.autohint_sizes = response.data;
    });
    summaryApi.getFontaineFonts().then(function(response) {
        $scope.fontaine_fonts = response.data;
    });
    summaryApi.getFontsOrthography().then(function(response) {
        $scope.fonts_orthography = response.data;
    });
    summaryApi.getTests().then(function(response) {
        $scope.tests = response.data;
        var chartsum = {"success": 0, "failure": 0, "fixed": 0, "error": 0};
        angular.forEach($scope.tests, function(results, test) {
            var success_len = results['success'].length,
                fixed_len = results['fixed'].length,
                failure_len = results['failure'].length,
                error_len = results['error'].length,
                data = google.visualization.arrayToDataTable([
                    ['Tests', '#'],
                    ['Success '+success_len, success_len],
                    ['Fixed '+fixed_len, fixed_len],
                    ['Failed '+failure_len, failure_len],
                    ['Error '+error_len, error_len]
                ]),
                options = {
                    title: test,
                    is3D: true,
                    colors: ['#468847', '#3a87ad', '#b94a48', '#c09853']
                };
            $scope.charts.push({data: data, options: options, type: "PieChart", displayed: true});
            chartsum = {
                "success": chartsum.success + success_len,
                "error": error_len,
                "failure": chartsum.failure + failure_len,
                "fixed": chartsum.fixed + fixed_len
            }
        });
        if (Object.keys($scope.tests).length > 1) {
            var success_len = chartsum.success,
                fixed_len = chartsum.fixed,
                failure_len = chartsum.failure,
                error_len = chartsum.error,
                data = google.visualization.arrayToDataTable([
                    ['Tests', '#'],
                    ['Success '+success_len, success_len],
                    ['Fixed '+fixed_len, fixed_len],
                    ['Failed '+failure_len, failure_len],
                    ['Error '+error_len, error_len]
                ]),
                options = {
                    title: "Average",
                    is3D: true,
                    colors: ['#468847', '#3a87ad', '#b94a48', '#c09853']
                };
            $scope.average_chart = {data: data, options: options, type: "PieChart", displayed: true};
        }


        $scope.blockers = {};
        var watch_list = ['error', 'failure', 'fixed'];
        var watch_tag = 'required';
        angular.forEach($scope.tests, function(results, font) {
            $scope.blockers[font] = {};
            angular.forEach(results, function(values, name) {
                if (watch_list.indexOf(name) != -1) {
                    var items = [];
                    angular.forEach(values, function(item) {
                        if (item.tags.indexOf(watch_tag) != -1) {
                            items.push(item)
                        }
                        $scope.blockers[font][name] = items;
                    })
                }
            });
        });
    });

    $scope.isReady = function() {
        return !Mixins.checkAll(
            null, $scope.metrics, $scope.tests,
            $scope.table_sizes, $scope.autohint_sizes,
            $scope.fontaine_fonts, $scope.fonts_orthography
        )
    };

    $scope.$on('$viewContentLoaded', function() {
        console.log("$viewContentLoaded");
    });
});