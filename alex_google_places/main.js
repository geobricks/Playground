
var repository = '//fenixapps.fao.org/repository/js/';

var fnx_modules = 'src/fenix_modules/';



require.config({

    baseUrl: '',

    paths: {

        "google_places": 'GooglePlaces',
        "google_places_api": '//maps.googleapis.com/maps/api/js?libraries=places',
        "jquery" :   '//fenixapps.fao.org/repository/js/jquery/1.10.2/jquery-1.10.2.min'
    }

});

require(['jquery', 'google_places'], function($, GooglePlaces) {
    var g = new GooglePlaces()
    g.get_places();
});