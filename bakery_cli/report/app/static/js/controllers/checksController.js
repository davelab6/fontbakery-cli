myApp.controller('checksController', function($scope, $http, checksApi) {
    $scope.charts = [];
    $scope.average_chart = null;
    $scope.dataLoaded = false;

    checksApi.getDataFile().then(function(response) {
        $scope.tests = response.data;
        $scope.dataLoaded = true;
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
        // build chart of average values if we have more than 1 font
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
    });
});

