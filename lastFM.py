import sys
import requests

api_key = "496a61caa0ce335911b9cbea2d15e1c9"
base_url = "http://ws.audioscrobbler.com/2.0/"
signature = "&api_key=" + api_key + "&format=json"


def get_genres(max_genres):
    genres = []
    # construct query
    query = "?method=tag.getTopTags&num_res=" + str(max_genres)

    # call API
    request = requests.get(base_url + query + signature)

    # manage response
    if (request.status_code != 200):
        sys.exit("Error: Code " + str(request.status_code))
    else:
        if (request.json()['toptags']['tag']):
            for genre in request.json()['toptags']['tag']:
                genres.append(genre['name'])
    return genres


def get_songs_per_genre(genre, songs, page, songs_per_genre):
    # construct query
    query = "?method=tag.gettoptracks&tag=" + genre + "&page=" + str(page)

    # call API
    request = requests.get(base_url + query + signature)

    # manage response
    if (request.status_code != 200):
        sys.exit("Error: Code " + str(request.status_code))
    else:
        if (request.json()['tracks']['track']):
            # attributes
            attributes = request.json()['tracks']['@attr']
            currentPage = attributes['page']
            isLastPage = currentPage == attributes['totalPages']

            # loop songs
            for track in request.json()['tracks']['track']:
                if (len(songs) < songs_per_genre):
                    song = {}
                    song['title'] = track['name']
                    song['artist'] = track['artist']['name']
                    song['genre'] = genre
                    songs.append(song)

            # recursive part of the algorithm
            if (len(songs) < songs_per_genre and not isLastPage):
                nextPage = int(currentPage) + 1
                return get_songs_per_genre(genre, songs, nextPage, songs_per_genre)
            else:
                return songs


'''
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
          //client.query("INSERT INTO genre(genre) values($1)", [song.genre]);
          //client.query("INSERT INTO song(title,artist,id_genre) values($1,$2,$3)", [song.title,song.artist,1]);
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
'''
