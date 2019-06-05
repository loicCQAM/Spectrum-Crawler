// INCLUDES
var axios = require('axios');
var config = require('./config');
var signature = '&api_key=' + config.lastFM.key + '&format=json';
var client = require('./client');

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
      // Attributes
      const attributes = response.data.tracks['@attr'];
      const currentPage = parseInt(attributes.page);
      const isLastPage = currentPage === parseInt(attributes.totalPages);

      // Loop songs retrieved
      response.data.tracks.track.forEach(function (track) {
        if (songs.length < config.crawler.maxPerGenre) { // TODO: check if song already retrieved (in another genre also)
          var song = {
            title: track.name,
            artist: track.artist.name,
            genre: genre
          }
          client.query("INSERT INTO genre(genre) values($1)", [song.genre]);
          client.query("INSERT INTO song(title,artist,id_genre) values($1,$2,$3)", [song.title,song.artist,1]);
          songs.push(song);
        }
      });

      // Check if we have less than the maximum and we have more songs to retrieve
      if (songs.length < config.crawler.maxPerGenre && !isLastPage) {
        // Recursive call
        return getSongsPerGenre(genre, currentPage + 1, songs);
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
