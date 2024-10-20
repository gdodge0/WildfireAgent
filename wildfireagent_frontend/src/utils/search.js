// Helper function to deeply search through an object
export default function deepSearchObject(obj, searchTerm) {
  for (let key in obj) {
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      // Recursively search nested objects
      if (deepSearchObject(obj[key], searchTerm)) {
        return true;
      }
    } else if (String(obj[key]).toLowerCase().includes(searchTerm)) {
      // Convert the value to string and check if it includes the search term
      return true;
    }
  }
  return false;
}