function calcDistance(coords1, coords2) {
  const toRad = (x) => (x * Math.PI) / 180;

  const lat1 = coords1.lat;
  const lon1 = coords1.lng;
  const lat2 = coords2.lat;
  const lon2 = coords2.lng;

  const R = 6371; // Radius of the Earth in kilometers
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) *
      Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c; // Distance in kilometers

  return distance;
}

export default function getNClosestLocations(locations, userCoords, n=3) {
  console.log("getnclosestlocations")
  // insert distance to fire from user coords
  for (let i=0; i<locations.length;i++)
  {
    locations[i].proximity = calcDistance(userCoords, locations[i])
  }

  return locations.sort((a, b) => {
    return a.proximity - b.proximity; // Sort by closest distance
  }).slice(0, n);
}