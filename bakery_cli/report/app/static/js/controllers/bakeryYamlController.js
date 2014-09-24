myApp.controller('bakeryYamlController', function($scope, $http, bakeryYamlApi, EditorService, PathBuilder) {
    var bakery_yaml = 'bakery.yaml';
    bakeryYamlApi.getYamlFile().then(function(response) {
        $scope.data = response.data;
    });
    $scope.aceLoaded = function(_editor) {
        EditorService.heightUpdateFunction(_editor, angular.element('#editor'), angular.element('#editor-section'));
    };
    $scope.view_url = PathBuilder.buildPath($scope.repo.url, 'blob', 'master', bakery_yaml);
    $scope.edit_url = PathBuilder.buildPath($scope.repo.url, 'edit', 'master', bakery_yaml);
});
