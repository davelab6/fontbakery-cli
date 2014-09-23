// app.js

// create module and include dependencies
var myApp = angular.module(
    'myApp', ['ngRoute', 'btford.markdown', 'ui.bootstrap', 'ui.ace']
);

myApp.factory('alertsFactory', function () {
    var alerts = [];
    return {
        getAlerts: function () {
            return alerts;
        },
        addAlert: function (msg, type) {
            alerts.push({ msg: msg , type: type || 'danger'});
        },
        closeAlert: function (index) {
            alerts.splice(index, 1);
        }
    }
});

// interceptor of http calls
myApp.factory('httpInterceptor', function($q, $location, alertsFactory) {
    var _config = {};
    return {
        // optional method
        'request': function(config) {
            // do something on success
            _config = config || $q.when(config);
            return _config;
        },

        // optional method
        'requestError': function(rejection) {
            // do something on error
            return $q.reject(rejection);
        },

        // optional method
        'response': function(response) {
            // do something on success
             return response || $q.when(response);
        },

        // optional method
        'responseError': function(rejection) {
            // add alert for every error
            alertsFactory.addAlert(rejection.status + " - " + rejection.statusText + ": " + _config.url);
            return $q.reject(rejection);
        }
    };
});

// configure our app
myApp.config(function($routeProvider, $httpProvider) {
    // configure routes
    $routeProvider
        // route for the summary page
        .when('/', {
            title: 'Summary',
            templateUrl : 'pages/summary.html',
            controller  : 'summaryController'
        })

        // route for the review page
        .when('/review', {
            title: 'Review',
            templateUrl : 'pages/review.html',
            controller  : 'reviewController'
        })

        // route for the checks page
        .when('/checks', {
            title: 'Pre-Build Checks',
            templateUrl : 'pages/checks.html',
            controller  : 'checksController'
        })

        // route for the tests page
        .when('/tests', {
            title: 'Tests',
            templateUrl : 'pages/tests.html',
            controller  : 'testsController'
        })

        // route for the build log page
        .when('/build-log', {
            title: 'Build Log',
            templateUrl : 'pages/build-log.html',
            controller  : 'buildLogController'
        })

        // route for the metadata page
        .when('/metadata', {
            title: 'Metadata',
            templateUrl : 'pages/metadata.html',
            controller  : 'metadataController'
        })

        // route for the bakery yaml page
        .when('/bakery-yaml', {
            title: 'Metadata',
            templateUrl : 'pages/bakery-yaml.html',
            controller  : 'bakeryYamlController'
        })

        // route for the description page
        .when('/description', {
            title: 'Contact',
            templateUrl : 'pages/description.html',
            controller  : 'descriptionController'
        });

    // #TODO: switch to custom cache factory
    // Current caching mechanism brings unexpected results.
    // The response will be stored in a cache named "$http".
    // This cache is created by Angular's $cacheFactory as the default
    // cache for the $http service when Angular boots up.
    // Such behaviour does not fit our needs as it will use the same
    // cache across all fonts opened in one browser.

    // enable default caching
    $httpProvider.defaults.cache = true;
    // intercept http calls
    $httpProvider.interceptors.push('httpInterceptor');
});

// directive to handle class attr of navigation menu items (eg, set/rm "active")
// #TODO make navigation menu as a separate component
myApp.directive('navMenu', function($location) {
    function activeLink(scope, element, attrs) {
        var links = element.find('a'),
            activeClass = attrs.navMenu || 'active',
            routePattern,
            link,
            url,
            currentLink,
            urlMap = {},
            i;
        if (!$location.$$html5) {
            routePattern = /^#[^/]*/;
        }

        for (i = 0; i < links.length; i++) {
            link = angular.element(links[i]);
            url = link.attr('href');

            if ($location.$$html5) {
                urlMap[url] = link;
            } else {
                urlMap[url.replace(routePattern, '')] = link;
            }
        }

        scope.$on('$routeChangeStart', function() {
            var pathLink = urlMap[$location.path()];
            if (pathLink) {
                if (currentLink) {
                    currentLink.parent('li').removeClass(activeClass);
                }
                currentLink = pathLink;
                currentLink.parent('li').addClass(activeClass);
            }
        });
    }
    return {
        link: activeLink
    }
});

// change <title> of the pages at runtime
myApp.run(['$location', '$rootScope', function($location, $rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $rootScope.title = current.$$route.title;
    });
}]);

// #TODO it would be better to get it from .json conf file once and use later.
// Allows to not change code, but rather external file
myApp.constant("appConfig", {
    files: {
        metadata: 'METADATA.json',
        metadata1: 'metadata1.json',
        metadata_new: 'METADATA.json.new',
        app: 'app.json',
        buildlog: 'buildlog.txt',
        repo: 'repo.json'
    },
    statusMap: {'success': 'OK', 'failure': 'FAIL', 'error': 'ERROR', 'fixed': 'FIXED'},
    resultMap: {'success': 'success', 'failure': 'danger', 'error': 'warning', 'fixed': 'info'}
});

myApp.service('FilesService', function() {
    //#TODO should be some built-in solution
    this.buildPath = function() {
        var path_chunks = ['data'];
        angular.forEach(arguments, function(item) {
            path_chunks.push(item);
        });
        return path_chunks.join('/')
    };
});

myApp.service('UrlsService', function() {
    //#TODO should be some built-in solution
    this.buildUrl = function() {
        var path_chunks = [];
        angular.forEach(arguments, function(item) {
            path_chunks.push(item);
        });
        return path_chunks.join('/')
    }
});

// use this service to get files, eg METADATA.json
myApp.service('DataService', function($http, $q, FilesService, appConfig) {
//    delete $http.defaults.headers.common['X-Requested-With'];
    this.getAppInfo = function() {
        return $http.get(FilesService.buildPath(appConfig.files.app));
    };

    this.getRepoInfo = function() {
        return $http.get(FilesService.buildPath(appConfig.files.repo));
    };

    this.getMetadata = function() {
        return $http.get(FilesService.buildPath(appConfig.files.metadata));
    };

    this.getMetadataNew = function() {
        return $http.get(FilesService.buildPath(appConfig.files.metadata_new));
    };

    this.getMetadataRaw = function() {
        return $http.get(FilesService.buildPath(appConfig.files.metadata), {transformResponse: []});
    };

    this.getMetadataNewRaw = function() {
        return $http.get(FilesService.buildPath(appConfig.files.metadata_new), {transformResponse: []});
    };

    this.getBuildLog = function() {
        return $http.get(FilesService.buildPath(appConfig.files.buildlog));
    };

    this.getRawFiles = function(urls_list) {
        var urls = urls_list || [{url: FilesService.buildPath(appConfig.files.metadata)},
                                 {url: FilesService.buildPath(appConfig.files.metadata_new)}];
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

    this.getMetadata1 = function() {
        return $http.get(FilesService.buildPath(appConfig.files.metadata1));
    };

});

myApp.service('EditorService', function() {
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
//            angular.element(visualdiff).empty();
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

// create the controllers and inject Angular's $scope etc

myApp.controller('mainController', function($scope, $http, DataService, alertsFactory, appConfig) {
    DataService.getAppInfo().then(function(dataResponse) {
        $scope.version = dataResponse.data;
    });
    DataService.getRepoInfo().then(function(dataResponse) {
        $scope.repo = dataResponse.data;
    });
    DataService.getMetadata().then(function(dataResponse) {
        $scope.metadata = dataResponse.data;
    });
    // current controller is on top level, so all http
    // errors should come through it
    $scope.alerts = alertsFactory;
    $scope.statusMap = appConfig.statusMap;
    $scope.resultMap = appConfig.resultMap;
});

myApp.controller('summaryController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from summaryController!';
});

myApp.controller('reviewController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from reviewController!';
});

myApp.controller('checksController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from checksController!';
});

myApp.controller('testsController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from testsController!';
});

myApp.controller('buildLogController', function($scope, $http, DataService) {
    DataService.getBuildLog().then(function(response) {
        $scope.data = response.data;
    });
});

myApp.controller('metadataController', function($scope, $http, $q, DataService, EditorService, UrlsService, appConfig) {

    $scope.dataLoaded = false;
    $scope._editor = null;
    $scope._editor_new = null;

    $scope.view_url = UrlsService.buildUrl($scope.repo.url, 'blob', 'master', appConfig.files.metadata);
    $scope.edit_url = UrlsService.buildUrl($scope.repo.url, 'edit', 'master', appConfig.files.metadata);

    $scope.$watch('dataLoaded', function() {
        if ($scope.dataLoaded) {
            angular.element('.tablesorter').tablesorter();
            if ($scope._editor && $scope._editor_new) {
                EditorService.heightUpdateFunction($scope._editor, angular.element('#editor-new'), angular.element('#editor-new-section'));
                EditorService.heightUpdateFunction($scope._editor_new, angular.element('#editor-new'), angular.element('#editor-new-section'));
                $scope.doDiff = EditorService.doDiff($scope._editor.getSession(), $scope._editor_new.getSession(), 'visualdiff');
//                $scope.doDiff();
            }
        }
    });

    DataService.getMetadata1().then(function(response) {
        $scope.all_fonts = response.data;
    });

//    DataService.getMetadataRaw().then(function(response) {
//        $scope.metadata_raw = response.data;
//    });
//
//    DataService.getMetadataNewRaw().then(function(response) {
//        $scope.metadata_new_raw = response.data;
//    });
//    OR

    DataService.getRawFiles().then(function(responses) {
        $scope.metadata_raw = responses[0].data;
        $scope.metadata_new_raw = responses[1].data;
        $scope.dataLoaded = true;
    });

    $scope.aceLoaded = function(_editor) {
        EditorService.heightUpdateFunction(_editor, angular.element('#editor'), angular.element('#editor-section'));
        $scope._editor = _editor;
    };

    $scope.aceChanged = function(_editor) {
//        $scope._editor = _editor;
    };

    $scope.aceLoadedNew = function(_editor) {
        EditorService.heightUpdateFunction(_editor, angular.element('#editor-new'), angular.element('#editor-new-section'));
        $scope._editor_new = _editor;
    };

    $scope.aceChangedNew = function(_editor) {
//        $scope._editor_new = _editor;
    };

    if ($scope.dataLoaded && $scope._editor && $scope._editor_new) {
        $scope.doDiff = EditorService.doDiff($scope._editor.getSession(), $scope._editor_new.getSession(), 'visualdiff');
        $scope.doDiff();
    }
});

myApp.controller('bakeryYamlController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from bakeryYamlController!';
});

myApp.controller('descriptionController', function($scope) {
    $scope.message = 'This is message from descriptionController!';
});
