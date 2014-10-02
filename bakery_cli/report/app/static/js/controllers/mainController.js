angular.module('myApp').controller('mainController', function($scope, $rootScope, $http, appApi, alertsFactory, appConfig, Mixins) {
    appApi.getAppInfo().then(function(dataResponse) {
        $scope.app_info = dataResponse.data;
    });
    appApi.getRepoInfo().then(function(dataResponse) {
        $scope.repo_info = dataResponse.data;
    });
    appApi.getMetadata().then(function(dataResponse) {
//        $scope.metadata = dataResponse.data;
        $rootScope.metadata = dataResponse.data;
    });
    // current controller is on top level, so all http
    // errors should come through it
    $scope.alerts = alertsFactory;

    $scope.mixins = Mixins;
    $scope.statusMap = appConfig.statusMap;
    $scope.resultMap = appConfig.resultMap;
    $scope.pangram = appConfig.pangram;
});