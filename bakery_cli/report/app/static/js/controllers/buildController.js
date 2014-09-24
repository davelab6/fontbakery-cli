angular.module('myApp').controller('buildController', function($scope, $http, buildApi) {
    buildApi.getBuildLog().then(function(response) {
        $scope.data = response.data;
    });
});