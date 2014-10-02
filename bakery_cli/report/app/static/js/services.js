angular.module('myApp').service('Mixins', [function() {
    this.checkAll = function() {
        var compare_to = arguments[0];
        function boolFilter(element, index, array) {
            return element === compare_to;
        }
        var args = Array.prototype.slice.call(arguments, 1);
        return args.every(boolFilter);
    };

    //<div ng-bind-html="&#item;"></div>
    //fails because of
    //https://github.com/angular/angular.js/pull/4747
    //https://github.com/angular/angular.js/pull/7485#issuecomment-43722719
    //https://github.com/angular/angular.js/issues/2174

    // encode(decode) html text into html entity
    this.decodeHtmlEntity = function(str) {
        return str.replace(/&#(\d+);/g, function(match, dec) {
            return String.fromCharCode(dec);
        });
    };

    this.encodeHtmlEntity = function(str) {
        var buf = [];
        for (var i=str.length-1;i>=0;i--) {
            buf.unshift(['&#', str[i].charCodeAt(), ';'].join(''));
        }
        return buf.join('');
    };
}]);

// helper service to build paths
angular.module('myApp').service('PathBuilder', ['appConfig', function(appConfig) {
    //#TODO should be some built-in solution
    this.buildPath = function() {
        var args = [];
        angular.forEach(arguments, function(item) {
            args.push(item);
        });
        return args.join('/')
    };
    this.buildDataPath = function() {
        var args = [appConfig.data_dir];
        angular.forEach(arguments, function(item) {
            args.push(item);
        });
        return args.join('/');
    };
    this.buildPagesPath = function() {
        var args = [appConfig.data_dir, appConfig.pages_dir];
        angular.forEach(arguments, function(item) {
            args.push(item);
        });
        return args.join('/');
    };
}]);

//API services
angular.module('myApp').service('appApi', ['$http', '$q', 'PathBuilder', 'appConfig', function($http, $q, PathBuilder, appConfig) {
    this.getAppInfo = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.app));
    };

    this.getRepoInfo = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.repo));
    };

    this.getMetadata = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata));
    };
}]);

angular.module('myApp').service('metadataApi', ['$http', '$q', 'PathBuilder', 'appConfig', function($http, $q, PathBuilder, appConfig) {
    var name = 'metadata',
        metadata_new = 'METADATA.json.new';

    this.getMetadata = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata));
    };

    this.getMetadataNew = function() {
        return $http.get(PathBuilder.buildPagesPath(name, metadata_new));
    };

    this.getMetadataRaw = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata), {transformResponse: []});
    };

    this.getMetadataNewRaw = function() {
        return $http.get(PathBuilder.buildPagesPath(name, metadata_new), {transformResponse: []});
    };
    this.getRawFiles = function(urls_list) {
        var urls = urls_list || [{url: PathBuilder.buildDataPath(appConfig.metadata)},
                                 {url: PathBuilder.buildPagesPath(name, metadata_new)}];
        var deferred = $q.defer();
        var urlCalls = [];
        angular.forEach(urls, function(url) {
            urlCalls.push($http.get(url.url, {transformResponse: []}));
        });
        // they may, in fact, all be done, but this
        // executes the callbacks in then, once they are
        // completely finished.
        $q.all(urlCalls).then(
            function(results) {
                deferred.resolve(results)
            },
            function(errors) {
                deferred.reject(errors);
            },
            function(updates) {
                deferred.update(updates);
            });
        return deferred.promise;
    };

    this.getTests = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'tests.json'));
    };
}]);

angular.module('myApp').service('testsApi', ['$http', '$q', 'PathBuilder', function($http, $q, PathBuilder) {
    var name = 'tests';

    this.getTests = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'tests.json'));
    };

}]);

angular.module('myApp').service('summaryApi', ['$http', '$q', 'PathBuilder', function($http, $q, PathBuilder) {
    var name = 'summary';
    this.getMetrics = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'metrics.json'));
    };
    this.getTableSizes = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'table_sizes.json'));
    };
    this.getAutohintSizes = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'autohint_sizes.json'));
    };
    this.getFontaineFonts = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'fontaine_fonts.json'));
    };
    this.getFontsOrthography = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'fonts_orthography.json'));
    };
    this.getTests = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'tests.json'));
    };
    this.getFontsTableGrouped = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'fonts_tables_grouped.json'));
    };
}]);

angular.module('myApp').service('checksApi', ['$http', '$q', 'PathBuilder', function($http, $q, PathBuilder) {
    var name = 'checks';
    this.getTests = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'tests.json'));
    };

    this.getUpstreamYamlFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'upstream.yaml'));
    };
}]);

angular.module('myApp').service('buildApi', ['$http', '$q', 'PathBuilder', function($http, $q, PathBuilder) {
    var name = 'build';
    this.getBuildLog = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'buildlog.txt'));
    };
}]);

angular.module('myApp').service('bakeryYamlApi', ['$http', '$q', 'PathBuilder', function($http, $q, PathBuilder) {
    var name = 'bakery-yaml';
    this.getYamlFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'bakery.yaml'));
    };
}]);

angular.module('myApp').service('descriptionApi', ['$http', '$q', 'PathBuilder', function($http, $q, PathBuilder) {
    var name = 'description';
    this.getDescriptionFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'DESCRIPTION.en_us.html'), {transformResponse: []});
    };
}]);

angular.module('myApp').service('reviewApi', ['$http', '$q', 'PathBuilder', function($http, $q, PathBuilder) {
    var name = 'review';
    this.getOrthography = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'orthography.json'));
    };
}]);
