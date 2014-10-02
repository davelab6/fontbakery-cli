angular.module('myApp').controller('descriptionController', function($scope, descriptionApi) {
    $scope.dataLoaded = false;

    descriptionApi.getDescriptionFile().then(function(response) {
        $scope.data = response.data;
        $scope.dataLoaded = true;
        angular.element('#preview').html($scope.editor.getSession().getValue());
    });

    $scope.aceLoaded = function(_editor) {
        $scope.editor = _editor;
        angular.element('#preview').html($scope.editor.getSession().getValue());
    };

    $scope.aceChanged = function(_editor) {
        angular.element('#preview').html($scope.editor.getSession().getValue());
    };

    $scope.$on('$viewContentLoaded', function() {
        angular.element('#preview').html($scope.editor.getSession().getValue());
    });
});