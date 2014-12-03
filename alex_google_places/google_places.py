from googleplaces import GooglePlaces, types, lang, GooglePlacesError

YOUR_API_KEY = 'AIzaSyAiFpFd85eMtfbvmVNEYuNds5TEF9FjIPI'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.nearby_search(
    location='London, England', keyword='Fish and Chips',
    radius=20000, types=[types.TYPE_FOOD])

if query_result.has_attributions:
    print query_result.html_attributions


for place in query_result.places:
    # Returned places from a query are place summaries.
    print place.name
    print place.geo_location
    print place.reference

    # The following method has to make a further API call.
    place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    print place.details # A dict matching the JSON response from Google.
    print place.local_phone_number
    print place.international_phone_number
    print place.website
    print place.url

    # Getting place photos

    for photo in place.photos:
        # 'maxheight' or 'maxwidth' is required
        photo.get(maxheight=500, maxwidth=500)
        # MIME-type, e.g. 'image/jpeg'
        photo.mimetype
        # Image URL
        photo.url
        # Original filename (optional)
        photo.filename
        # Raw image data
        photo.data


# Adding and deleting a place
try:
    added_place = google_places.add_place(name='Mom and Pop local store',
                                          lat_lng={'lat': 51.501984, 'lng': -0.141792},
                                          accuracy=100,
                                          types=types.TYPE_HOME_GOODS_STORE,
                                          language=lang.ENGLISH_GREAT_BRITAIN)
    print added_place.reference # The Google Places reference - Important!
    print added_place.id

    # Delete the place that you've just added.
    google_places.delete_place(added_place.reference)
except GooglePlacesError as error_detail:
    # You've passed in parameter values that the Places API doesn't like..
    print error_detail