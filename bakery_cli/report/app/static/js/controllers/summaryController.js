myApp.controller('summaryController', function($scope, $http, summaryApi) {
    summaryApi.getMetrics().then(function(response) {
        $scope.metrics = response.data;
    });
    summaryApi.getTableSizes().then(function(response) {
        $scope.table_sizes = response.data;
    });
});