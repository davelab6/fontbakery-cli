angular.module('myApp').controller('descriptionController', function($scope, descriptionApi, EditorService) {
    descriptionApi.getDescriptionFile().then(function(response) {
        $scope.data = response.data;
    });
    $scope.aceLoaded = function(_editor) {
        EditorService.heightUpdateFunction(_editor, angular.element('#editor'), angular.element('#editor-section'));
        $scope.editor = _editor;
        angular.element('#preview').html($scope.editor.getSession().getValue());
    };

    $scope.aceChanged = function(_editor) {
        angular.element('#preview').html($scope.editor.getSession().getValue());
    };
});