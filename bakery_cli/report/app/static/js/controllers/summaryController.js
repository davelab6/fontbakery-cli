myApp.controller('summaryController', function($scope, $http, summaryApi, Mixins) {
    $scope.tests = null;
    $scope.metrics = null;
    $scope.table_sizes = null;
    $scope.autohint_sizes = null;
    $scope.fontaine_fonts = null;
    $scope.fonts_orthography = null;
    $scope.fontSupportToStyle = {
        'full': 'success',
        'partial': 'info',
        'fragmentary': 'warning',
        'unsupported': 'danger'
    };

    summaryApi.getMetrics().then(function(response) {
        $scope.metrics = response.data;
    });
    summaryApi.getTableSizes().then(function(response) {
        $scope.table_sizes = response.data;
    });
    summaryApi.getAutohintSizes().then(function(response) {
        $scope.autohint_sizes = response.data;
    });
    summaryApi.getFontaineFonts().then(function(response) {
        $scope.fontaine_fonts = response.data;
    });
    summaryApi.getFontsOrthography().then(function(response) {
        $scope.fonts_orthography = response.data;
    });
    summaryApi.getTests().then(function(response) {
        $scope.tests = response.data;
        $scope.blockers = {};
        var watch_list = ['error', 'failure', 'fixed'];
        var watch_tag = 'required';
        angular.forEach($scope.tests, function(results, font) {
            $scope.blockers[font] = {};
            angular.forEach(results, function(values, name) {
                if (watch_list.indexOf(name) != -1) {
                    var items = [];
                    angular.forEach(values, function(item) {
                        if (item.tags.indexOf(watch_tag) != -1) {
                            items.push(item)
                        }
                        $scope.blockers[font][name] = items;
                    })
                }
            });
        });
    });

    $scope.isReady = function() {
        return !Mixins.checkAll(
            null, $scope.metrics, $scope.tests,
            $scope.table_sizes, $scope.autohint_sizes,
            $scope.fontaine_fonts, $scope.fonts_orthography
        )
    };

    $scope.$on('$viewContentLoaded', function() {
        console.log("$viewContentLoaded");
    });
});