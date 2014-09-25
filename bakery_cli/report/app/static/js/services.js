// service to work with ACE editor
angular.module('myApp').service('EditorService', function() {
    this.heightUpdateFunction = function(editor, editor_div, editor_section) {
        var newHeight =
            editor.getSession().getScreenLength()
                * editor.renderer.lineHeight
                + editor.renderer.scrollBar.getWidth();
        editor_div.height(newHeight.toString() + "px");
        editor_section.height(newHeight.toString() + "px");
        // This call is required for the editor to fix all
        // of its inner structure for adapting to a change in size
        editor.resize();
    };

    this.doDiff = function(editor1, editor2, result_of_diff) {
        return function () {
            var left = JSON.parse(editor1.getValue());
            var right = JSON.parse(editor2.getValue());

            var instance = jsondiffpatch.create({
                objectHash: function (obj) {
                    return '';
                }
            });

            var delta = instance.diff(left, right);

            var visualdiff = document.getElementById(result_of_diff);
            if (visualdiff) {
                visualdiff.innerHTML = jsondiffpatch.formatters.html.format(delta, left);

                var scripts = visualdiff.querySelectorAll('script');
                for (var i = 0; i < scripts.length; i++) {
                    var s = scripts[i];
                    /* jshint evil: true */
                    eval(s.innerHTML);
                }
            }
            angular.element(visualdiff).find('div').first().find('pre')
                .each(function (i) {
                    angular.element(this).css("background-color", "transparent").css("border", "0");
                })
        };
    };
});

// helper service to build paths
angular.module('myApp').service('PathBuilder', function(appConfig) {
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
});

//API services
angular.module('myApp').service('appApi', function($http, $q, PathBuilder, appConfig) {
    this.getAppInfo = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.app));
    };

    this.getRepoInfo = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.repo));
    };

    this.getMetadata = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata));
    };
});

angular.module('myApp').service('metadataApi', function($http, $q, PathBuilder, appConfig) {
    var name = 'metadata',
        metadata_new = 'METADATA.json.new';

    this.getMetadata = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata));
    };

    this.getMetadataNew = function() {
        return $http.get(PathBuilder.buildDataPath(metadata_new));
    };

    this.getMetadataRaw = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata), {transformResponse: []});
    };

    this.getMetadataNewRaw = function() {
        return $http.get(PathBuilder.buildDataPath(metadata_new), {transformResponse: []});
    };
    this.getRawFiles = function(urls_list) {
        var urls = urls_list || [{url: PathBuilder.buildDataPath(appConfig.metadata)},
                                 {url: PathBuilder.buildDataPath(metadata_new)}];
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

    this.getMetadataResults = function() {
        return $http.get(PathBuilder.buildPagesPath(name, appConfig.metadata));
    };
});

angular.module('myApp').service('testsApi', function($http, $q, PathBuilder, appConfig) {
    var name = 'tests';
    this.getDataFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'data.json'));
    };

    this.getTestsFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'tests.json'));
    };

    this.getFiles = function(urls_list) {
        var urls = urls_list || [{url: PathBuilder.buildPagesPath(name, 'tests.json')},
                                 {url: PathBuilder.buildPagesPath(name, 'data.json')}];
        var deferred = $q.defer();
        var urlCalls = [];
        angular.forEach(urls, function(url) {
            urlCalls.push($http.get(url.url));
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
});

angular.module('myApp').service('checksApi', function($http, $q, PathBuilder) {
    var name = 'checks';
    this.getDataFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'data.json'));
    };

    this.getUpstreamYamlFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'upstream.yaml'));
    };
});

angular.module('myApp').service('buildApi', function($http, $q, PathBuilder) {
    var name = 'build';
    this.getBuildLog = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'buildlog.txt'));
    };
});

angular.module('myApp').service('bakeryYamlApi', function($http, $q, PathBuilder) {
    var name = 'bakery-yaml';
    this.getYamlFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'bakery.yaml'));
    };
});

angular.module('myApp').service('descriptionApi', function($http, $q, PathBuilder) {
    var name = 'description';
    this.getDescriptionFile = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'DESCRIPTION.en_us.html'), {transformResponse: []});
    };
});
