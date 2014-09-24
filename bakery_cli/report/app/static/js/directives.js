// directive to handle class attr of navigation menu items (eg, set/rm "active")
// #TODO make navigation menu as a separate component
angular.module('myApp').directive('navMenu', function($location) {
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
