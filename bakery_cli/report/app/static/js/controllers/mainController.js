angular.module('myApp').controller('mainController', function($scope, $http, appApi, alertsFactory, appConfig, Mixins) {
    $scope.mixins = Mixins;
    appApi.getAppInfo().then(function(dataResponse) {
        $scope.version = dataResponse.data;
    });
    appApi.getRepoInfo().then(function(dataResponse) {
        $scope.repo = dataResponse.data;
    });
    appApi.getMetadata().then(function(dataResponse) {
        $scope.metadata = dataResponse.data;
    });
    // current controller is on top level, so all http
    // errors should come through it
    $scope.alerts = alertsFactory;
    $scope.statusMap = appConfig.statusMap;
    $scope.resultMap = appConfig.resultMap;
    $scope.pangram = appConfig.pangram;
});