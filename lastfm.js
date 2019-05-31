// INCLUDES
var axios = require('axios');

// LAST FM
var API_KEY = '496a61caa0ce335911b9cbea2d15e1c9';
var baseURL = 'http://ws.audioscrobbler.com/2.0/';
var signature = '&api_key=' + API_KEY + '&format=json';

// CONSTANTS
var MAX_GENRES = 75;
var MAX_PER_GENRE = 100;


/**
* @getSongsPerGenre
* Recursive function that calls the lastFM API to get an array of songs
* based on a given genre. The function calls itself until the number
* of songs retrieved is equal to the MAX_PER_GENRE constant
*
* @param {string} genre the genre of the songs to retrieve 
* @param {number} page page parameter of lastFM API
* @param {Array} songs the array containing the retrieved songs
*/
async function getSongsPerGenre(genre, page, songs) {
  // Set page to 1 if not defined
  page = (page === undefined) ? 1 : page;

  // Construct query
  var query = '?method=tag.gettoptracks&tag=' + genre + '&page=' + page;

  return axios.get(baseURL + query + signature).then(response => {
    if (response.data.tracks.track) {
      response.data.tracks.track.forEach(function (track) {
        if (songs.length < MAX_PER_GENRE) { // TODO: check if song already retrieved (in another genre also)
          var song = {
            title: track.name,
            artist: track.artist.name,
            genre: genre
          }
          songs.push(song);
        }
      });

      // Check if we have less than the maximum
      if (songs.length < MAX_PER_GENRE) {
        // Recursive call
        return getSongsPerGenre(genre, page + 1, songs);
      } else {
        // End of recursion
        return songs;
      }
    }
  }).catch(error => {
    console.log(error);
    return false;
  });
}

/**
* @getGenres
* Calls the lastFM API to get the top genres
* Uses constant MAX_GENRES to specify how many genres
* must be returned 
*/
async function getGenres() {
  var genres = [];
  // Construct query
  var query = '?method=tag.getTopTags&num_res=' + MAX_GENRES;
  return axios.get(baseURL + query + signature).then(response => {
    if (response.data.toptags.tag) {
      response.data.toptags.tag.forEach(function (genre) {
        genres.push(genre.name);
      });
      return genres;
    }
  }).catch(error => {
    console.log(error);
    return false;
  });
}

// Exports
module.exports.getSongsPerGenre = getSongsPerGenre;
module.exports.getGenres = getGenres;
