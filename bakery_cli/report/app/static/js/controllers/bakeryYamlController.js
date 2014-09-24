myApp.controller('bakeryYamlController', function($scope, $http, bakeryYamlApi, EditorService) {
    bakeryYamlApi.getYamlFile().then(function(response) {
        $scope.data = response.data;
    });
    $scope.aceLoaded = function(_editor) {
        EditorService.heightUpdateFunction(_editor, angular.element('#editor'), angular.element('#editor-section'));
    };
});
