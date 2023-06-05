var map = null;
var marker = null;


function initMap() {
  map = L.map('map').setView([51.505, -0.09], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
  }).addTo(map);
  marker = L.marker([0, 0]).addTo(map);
  map.on('click', function(e) {
    document.getElementById('latitude').value = e.latlng.lat;
    document.getElementById('longitude').value = e.latlng.lng;
    marker.setLatLng(e.latlng);
  });
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  document.getElementById('latitude').value = position.coords.latitude;
  document.getElementById('longitude').value = position.coords.longitude;
  map.setView([position.coords.latitude, position.coords.longitude], 13);
  marker.setLatLng([position.coords.latitude, position.coords.longitude]);
}

function showraisecomplaint() {
  document.getElementById("raise-complaint").style.display = "block";
  document.getElementById("view-complaints").style.display = "none";
}

function showcomplaints() {
  document.getElementById("view-complaints").style.display = "block";
  document.getElementById("raise-complaint").style.display = "none";
}

document.getElementById("get-location-button").addEventListener("click", getLocation);
document.getElementById("raise").addEventListener("click", showraisecomplaint);
document.getElementById("view").addEventListener("click", showcomplaints);

initMap();