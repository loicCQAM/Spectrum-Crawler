var lastFM = require('./lastfm');
var genres = [];
var client = require('./client');
 
/**
 * @getSongs
 * Loops an array of genres
 * Foreach genre, calls the getSongsPerGenre method which 
 * returns an array of songs
 */
const getSongs = async () => {
  genres.forEach(async function (genre) {
    var result = await lastFM.getSongsPerGenre(genre, 1, []);
    console.log(result.length + ' songs for genre ' + genre);
    console.log('-------');
  });
};

/**
 * @connect
 * Connects to DB
 */
const connect = async () => {
  await client.connect();
  console.log('---------- Connected to DB ! ----------');
};

/**
 * @disconnect
 * Disconnects of DB
 */
const disconnect = async () => {
  await client.end();
  console.log('---------- Disconnected to DB ! ----------');
};

/**
 * @crawl
 * Starts the program
 */
const crawl = async () => {
  connect();
  console.log('');
  console.log('---------- Getting genres ----------');
  genres = await lastFM.getGenres();
  console.log('> Retrieved ' + genres.length + ' genres');
  console.log('');
  console.log('---------- Getting songs ----------');
  await getSongs();
};

crawl();