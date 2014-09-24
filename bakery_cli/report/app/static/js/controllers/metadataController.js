angular.module('myApp').controller('metadataController', function($scope, $http, $q, metadataApi, EditorService, PathBuilder, appConfig) {
    $scope.charts = [];
    $scope.dataLoaded = false;
    $scope.editor1 = null;
    $scope.editor2 = null;

    $scope.view_url = PathBuilder.buildPath($scope.repo.url, 'blob', 'master', appConfig.metadata);
    $scope.edit_url = PathBuilder.buildPath($scope.repo.url, 'edit', 'master', appConfig.metadata);

    $scope.$watch('dataLoaded', function() {
        if ($scope.dataLoaded) {
            angular.element('.tablesorter').tablesorter();
            if ($scope.editor1 && $scope.editor2) {
                EditorService.heightUpdateFunction($scope.editor1, angular.element('#editor-new'), angular.element('#editor-new-section'));
//                $scope.editor1.resize();
//                $scope.editor1.renderer.updateFull();
                EditorService.heightUpdateFunction($scope.editor2, angular.element('#editor-new'), angular.element('#editor-new-section'));
                $scope.doDiff = EditorService.doDiff($scope.editor1.getSession(), $scope.editor2.getSession(), 'visualdiff');
//                $scope.doDiff();
            }
        }
    });

    metadataApi.getMetadataResults().then(function(response) {
        $scope.tests = response.data;
        angular.forEach($scope.tests, function(results, test) {
            var success_len = results['success'].length;
            var fixed_len = results['fixed'].length;
            var failure_len = results['failure'].length;
            var error_len = results['error'].length;
            var data = google.visualization.arrayToDataTable([
                ['Tests', '#'],
                ['Success '+success_len, success_len],
                ['Fixed '+fixed_len, fixed_len],
                ['Failed '+failure_len, failure_len],
                ['Error '+error_len, error_len]
            ]);
            var options = {
                title: test,
                is3D: true,
                colors: ['#468847', '#3a87ad', '#b94a48', '#c09853']
            };
            $scope.charts.push({data: data, options: options, type: "PieChart", displayed: true});
        });
    });

    metadataApi.getRawFiles().then(function(responses) {
        $scope.metadata1 = responses[0].data;
        $scope.metadata2 = responses[1].data;
        $scope.dataLoaded = true;
    });

    $scope.aceLoaded1 = function(_editor) {
        EditorService.heightUpdateFunction(_editor, angular.element('#editor'), angular.element('#editor-section'));
        $scope.editor1 = _editor;
    };

    $scope.aceChanged1 = function(_editor) {
//        $scope.editor1 = _editor;
    };

    $scope.aceLoaded2 = function(_editor) {
        EditorService.heightUpdateFunction(_editor, angular.element('#editor-new'), angular.element('#editor-new-section'));
        $scope.editor2 = _editor;
    };

    $scope.aceChanged2 = function(_editor) {
//        $scope.editor2 = _editor;
    };

    if ($scope.dataLoaded && $scope.editor1 && $scope.editor2) {
        $scope.doDiff = EditorService.doDiff($scope.editor1.getSession(), $scope.editor2.getSession(), 'visualdiff');
        $scope.doDiff();
    }
});