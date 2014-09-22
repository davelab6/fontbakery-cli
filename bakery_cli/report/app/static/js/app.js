// app.js

// create module and include dependencies
var myApp = angular.module('myApp', ['ngRoute', 'btford.markdown', 'ui.bootstrap']);

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

// either use $rootScope to have app wide variables, or use factories
// #TODO
myApp.factory('DataSource', function() {
    return {};
});

myApp.service('FilesService', function() {
    //#TODO should be some built-in solution
    this.buildPath = function(parts) {
        var path_chunks = ['data'];
        if (Array.isArray(parts)) {
            parts.forEach(function(item) {path_chunks.push(item)}, path_chunks);
        } else {
            path_chunks.push(parts)
        }
        return path_chunks.join('/')
    }
});

// use separate services to read files, eg METADATA.json
// this service gets some common for all pages data
myApp.service('DataService', function($http, FilesService) {
//    delete $http.defaults.headers.common['X-Requested-With'];
    this.getMetadata = function() {
        return $http.get(FilesService.buildPath('METADATA.json'));
    };
    this.getAppInfo = function() {
        return $http.get(FilesService.buildPath('app.json'));
    };
    this.getRepoInfo = function() {
        return $http.get(FilesService.buildPath('repo.json'));
    };
});


// create the controllers and inject Angular's $scope etc

myApp.controller('mainController', function($scope, $http, DataService, alertsFactory) {
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

myApp.controller('buildLogController', function($scope, $http, FilesService) {
    $http.get(FilesService.buildPath('buildlog.txt'))
        .success(function(data, status, headers, config) {
            $scope.data = data;
        });
});

myApp.controller('metadataController', function($scope, $http, FilesService) {
    // we already have METADATA.json parsed into object in `mainController`
    // and here we need raw file, do not deserialize it using a JSON parser.
    $http.get(FilesService.buildPath('METADATA.json'), {transformResponse: []})
        .success(function(data, status, headers, config) {
            $scope.metadata_raw = data;
        });

    $http.get(FilesService.buildPath('METADATA.json.new'), {transformResponse: []})
        .success(function(data, status, headers, config) {
            $scope.metadata_new_raw = data;
        });
    angular.element(document).ready(function () {
        console.log('Document ready!');
    });
});

myApp.controller('bakeryYamlController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from bakeryYamlController!';
});

myApp.controller('descriptionController', function($scope) {
    $scope.message = 'This is message from descriptionController!';
});
