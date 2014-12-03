define(["jquery"], function ($) {

    'use strict';

    function GooglePlaces() {
        this.o = {
            id: 'map',

            upper_left: [41.874861, 12.521721],
            lower_right: [41.873726, 12.526635],
            increase_step: 0.000415, //increase from the upper to lower (500m 0.0043? - 0.00083 100m - 0.000415 50m)
            radius: '50', // meters

            // research places
            types:['restaurant'],

            // Timeout of google API request (see anonymous limits)
            timeout: 1400
        };
    }

    GooglePlaces.prototype.get_places = function(o) {
        this.o =  $.extend(true, {}, this.o, o);
        var start_point = new google.maps.LatLng(this.o.upper_left[0], this.o.upper_left[1]);
        this.o.map = new google.maps.Map(document.getElementById('map'), {
            center: start_point,
            zoom: 15
        });
        this.createGoogleAPIRequests(this.o)
    }

    GooglePlaces.prototype.createGoogleAPIRequests = function(o) {
        this.o.index_request = 0;
        this.o.total_requests = 0;
        this.o.total_results = [];
        var _this = this;
        for ( var x = o.lower_right[0]; x <= o.upper_left[0]; x += o.increase_step) {
            for ( var y = o.upper_left[1]; y <= o.lower_right[1]; y += o.increase_step) {
                for (var k = 0; k < o.types.length; k++) {
                    var type = o.types[k]
                    var x = x;
                    var y = y;
                    this.o.total_requests++;
                    setTimeout(function(x, y, type) {
                        var p = new google.maps.LatLng(x, y);
                        var request = {
                            location: p,
                            radius: o.radius,
                            types: [type]
                        };
                        var service = new google.maps.places.PlacesService(o.map).nearbySearch(request, parseGoogleAPIResults);
                    }, this.o.timeout*(this.o.total_requests), x, y, type);
                }
            }
        }

        function parseGoogleAPIResults(results, status) {
            var total_requests = _this.o.total_requests;
            var index_request  = ++_this.o.index_request;
            console.log("requests: " + index_request + "/" + total_requests);

            if (status == google.maps.places.PlacesServiceStatus.OK) {
                for (var i = 0; i < results.length; i++) {
                    var place = results[i];
                    //console.log(place);
                    _this.o.total_results.push(place)

                    // save in db?
                }
            }
            else {
                console.log(status);
            }

            if (index_request == total_requests) {
                var a = document.createElement('a');
                a.href = 'data:text/csv;charset=utf-8,\n' + encodeURIComponent(_this.createCSV(_this.o.total_results));
                a.target = '_blank';
                a.download = 'country_data.csv';
                document.body.appendChild(a);
                a.click();
            }
        }
    }

    GooglePlaces.prototype.createCSV = function(total_results) {
        var finalVal =''
        var content = []
        for(var i=0; i < total_results.length; i++) {
            var c = []
            var types = ""
            for (var j = 0; j < total_results[i].types.length; j++) {
                types += total_results[i].types[j] + ","
            }
            types = types.slice(0, -1)

            var lat = total_results[i].geometry.location.lat()
            var lng = total_results[i].geometry.location.lng()

            var innerValue = total_results[i].name;
            var result = innerValue.replace(/"/g, '""');
            if (result.search(/("|,|\n)/g) >= 0)
                result = '"' + result + '"';
            finalVal += result;

            var innerValue = types;
            var result = innerValue.replace(/"/g, '""');
            if (result.search(/("|,|\n)/g) >= 0)
                result = '"' + result + '"';
            if (j > 0)
                finalVal += ',';
            finalVal += result;

            var innerValue = lat.toString();
            var result = innerValue.replace(/"/g, '""');
            if (result.search(/("|,|\n)/g) >= 0)
                result = '"' + result + '"';
            if (j > 0)
                finalVal += ',';
            finalVal += result;

            var innerValue = lng.toString();
            var result = innerValue.replace(/"/g, '""');
            if (result.search(/("|,|\n)/g) >= 0)
                result = '"' + result + '"';
            if (j > 0)
                finalVal += ',';
            finalVal += result;

            finalVal += '\n';
        }
        return finalVal;
    }

    return GooglePlaces;
});