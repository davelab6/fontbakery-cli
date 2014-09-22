// script.js

// create the module and name it myApp
// also include ngRoute for all our routing needs
var myApp = angular.module('myApp', ['ngRoute', 'btford.markdown']);

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
    // enable default caching
    $httpProvider.defaults.cache = true;
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
myApp.factory('DataSource', function() {
    return {
        metadata: {json: 'data/METADATA.json'},
        // the data below should be fetched via DataService once and then cached
        version: {commit: 'some#fake#commit#1', date: new Date()},
        repo: {
            gh_pages: 'http://fake.com/this/should/be/real/url/to/gh_pages',
            url: 'http://fake.com/this/should/be/real/url'
        }
    };
});

// use separate services to read files, eg METADATA.json
myApp.service('DataService', function($http, DataSource) {
//    delete $http.defaults.headers.common['X-Requested-With'];
    this.getMetadata = function() {
        return $http({method: 'GET', url: DataSource.metadata.json});
    };
    this.getVersion = function() {
        return DataSource.version;
    };
    this.getRepo = function() {
        return DataSource.repo;
    };
});


// create the controllers and inject Angular's $scope etc

myApp.controller('mainController', function($scope, $http, DataService) {
    // create a message to display in our view
    $scope.message = 'This is message from mainController!';

    $scope.version = DataService.getVersion();
    $scope.repo = DataService.getRepo();
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

myApp.controller('buildLogController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from buildLogController!';
    $http.get('data/buildlog.txt')
        .success(function(data, status, headers, config) {
            $scope.data = data;
        })
        .error(function(data, status, headers, config) {
            // #TODO make common area for errors across all pages
            console.log("ERROR");
        });
});

myApp.controller('metadataController', function($scope, $http, DataService) {
    // create a message to display in our view
    $scope.message = 'This is message from metadataController!';

    $scope.metadata = null;
    DataService.getMetadata().then(function(dataResponse) {
        $scope.metadata = dataResponse;
    });
});

myApp.controller('bakeryYamlController', function($scope, $http) {
    // create a message to display in our view
    $scope.message = 'This is message from bakeryYamlController!';
});

myApp.controller('descriptionController', function($scope) {
    $scope.message = 'This is message from descriptionController!';
});
