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
    data_dir: 'data',
    pages_dir: 'pages',

    metadata: 'METADATA.json',
    metadata_new: 'METADATA.json.new',
    app: 'app.json',
    repo: 'repo.json',

    statusMap: {'success': 'OK', 'failure': 'FAIL', 'error': 'ERROR', 'fixed': 'FIXED'},
    resultMap: {'success': 'success', 'failure': 'danger', 'error': 'warning', 'fixed': 'info'}
});

myApp.service('PathBuilder', function(appConfig) {
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

myApp.service('appApi', function($http, $q, PathBuilder, appConfig) {
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

myApp.service('metadataApi', function($http, $q, PathBuilder, appConfig) {
    var name = 'metadata';
    this.getMetadata = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata));
    };

    this.getMetadataNew = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata_new));
    };

    this.getMetadataRaw = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata), {transformResponse: []});
    };

    this.getMetadataNewRaw = function() {
        return $http.get(PathBuilder.buildDataPath(appConfig.metadata_new), {transformResponse: []});
    };
    this.getRawFiles = function(urls_list) {
        var urls = urls_list || [{url: PathBuilder.buildDataPath(appConfig.metadata)},
                                 {url: PathBuilder.buildDataPath(appConfig.metadata_new)}];
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

myApp.service('buildApi', function($http, $q, PathBuilder) {
    var name = 'build';
    this.getBuildLog = function() {
        return $http.get(PathBuilder.buildPagesPath(name, 'buildlog.txt'));
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

myApp.controller('mainController', function($scope, $http, appApi, alertsFactory, appConfig) {
    appApi.getAppInfo().then(function(dataResponse) {
        $scope.version = dataResponse.data;
    });
    appApi.getRepoInfo().then(function(dataResponse) {
        $scope.repo = dataResponse.data;
    });
    appApi.getMetadata().then(function(dataResponse) {
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

myApp.controller('buildLogController', function($scope, $http, buildApi) {
    buildApi.getBuildLog().then(function(response) {
        $scope.data = response.data;
    });
});

myApp.controller('metadataController', function($scope, $http, $q, metadataApi, EditorService, PathBuilder, appConfig) {

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
    });

//    metadataApi.getMetadataRaw().then(function(response) {
//        $scope.metadata1 = response.data;
//    });
//
//    metadataApi.getMetadataNewRaw().then(function(response) {
//        $scope.metadata2 = response.data;
//    });
//    OR

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

myApp.controller('bakeryYamlController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from bakeryYamlController!';
});

myApp.controller('descriptionController', function($scope) {
    $scope.message = 'This is message from descriptionController!';
});
