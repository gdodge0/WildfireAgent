export default function promptUserLocation(callback)
{
    let userCoords;
    console.log("geolocating")
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            // Successful response, set user's latitude and longitude
            userCoords = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            console.log("success coords")
              console.log(userCoords)
            callback(userCoords)
          },
          (error) => {
            // Handle the error case
            switch (error.code) {
                case error.PERMISSION_DENIED:
                console.log("User denied the request for Geolocation.")
                break;
              case error.POSITION_UNAVAILABLE:
                console.log("Location information is unavailable.")
                break;
              case error.TIMEOUT:
                console.log("The request to get user location timed out.")
                break;
              case error.UNKNOWN_ERROR:
                console.log("An unknown error occurred.")
                break;
            }
          }
        );
    } else {
        errorMessage.value = "Geolocation is not supported by this browser.";
    }

}
