myApp.controller('reviewController', function($scope, $http, reviewApi) {
    $scope.missing_chars_hidden = false;
    $scope.toggleMissingGlyphs = function() {
        try {
            var glyphSpans = document.getElementById("glyphContainer").getElementsByTagName("span");
            for(var i=0; i < glyphSpans.length; i++) {
                var glyphSpan = glyphSpans[i];
                if(glyphSpan.getAttribute("class") == "missing-glyph") {
                    var parent_div = angular.element(glyphSpan.parentNode).parent();

                    if(glyphSpan.parentNode.style.display == "none") {

                        if (parent_div[0].style.display == "none") {
                            parent_div[0].style.display = "block";
                        }

                        glyphSpan.parentNode.style.display = "block";
                    } else {

                        if (parent_div[0].style.display == "block") {
                            parent_div[0].style.display = "none";
                        }

                        glyphSpan.parentNode.style.display = "none";
                    }
                }
            }
            $scope.missing_chars_hidden = !$scope.missing_chars_hidden;
        } catch(e){}
    };

    $scope.setClassOnParentDiv = function(val) {
        return val ? 'none' : 'block'
    };

    reviewApi.getFontsOrthography().then(function(response) {
        var fonts_orthography = response.data;
        $scope.glyphs = [];
        angular.forEach(fonts_orthography.fonts_info, function(info, subset) {
            angular.forEach(info, function(font_info) {
                angular.forEach(font_info.glyphs, function(glyph) {
                    $scope.glyphs.push({
                        'glyph': glyph,
                        'is_missing': font_info.missing_chars.indexOf(glyph) != -1
                    })
                })
            });
        });
    });

    reviewApi.getFontsOrthographySorted().then(function(response) {
        var fonts_orthography_sorted = response.data;
        $scope.glyphs_sorted = [];
        angular.forEach(fonts_orthography_sorted, function(fonts) {
            angular.forEach(fonts[1], function(glyph) {
                $scope.glyphs_sorted.push({
                    'glyph': glyph,
                    'is_missing': fonts[4].indexOf(glyph) != -1
                })
            });
        });
    });
});
