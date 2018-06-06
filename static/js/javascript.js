function initMap() {
  // The location
  var location = {lat: latVal, lng: lngVal};
  // The map, centered at location
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 4, center: location});
  // The marker, positioned at location
  var marker = new google.maps.Marker({position: location, map: map});
}