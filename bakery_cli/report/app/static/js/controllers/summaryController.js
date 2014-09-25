myApp.controller('summaryController', function($scope, $http, summaryApi, Mixins) {
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
    $scope.isReady = function() {
        return !Mixins.checkAll(
            null, $scope.metrics,
            $scope.table_sizes, $scope.autohint_sizes,
            $scope.fontaine_fonts, $scope.fonts_orthography
        )
    };
    console.log(Mixins.decodeHtmlEntity('&#329;'))
});