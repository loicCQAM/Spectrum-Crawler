// INCLUDES
var axios = require('axios');
var config = require('./config');
var signature = '&api_key=' + config.lastFM.key + '&format=json';

/**
* @getSongsPerGenre
* Recursive function that calls the lastFM API to get an array of songs
* based on a given genre. The function calls itself until the number
* of songs retrieved is equal to the maxPerGenre config
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

  return axios.get(config.lastFM.baseURL + query + signature).then(response => {
    if (response.data.tracks.track) {
      response.data.tracks.track.forEach(function (track) {
        if (songs.length < config.crawler.maxPerGenre) { // TODO: check if song already retrieved (in another genre also)
          var song = {
            title: track.name,
            artist: track.artist.name,
            genre: genre
          }
          songs.push(song);
        }
      });

      // Check if we have less than the maximum
      if (songs.length < config.crawler.maxPerGenre) {
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
* Uses config maxGenres to specify how many genres
* must be returned 
*/
async function getGenres() {
  var genres = [];
  // Construct query
  var query = '?method=tag.getTopTags&num_res=' + config.crawler.maxGenres;
  return axios.get(config.lastFM.baseURL + query + signature).then(response => {
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
