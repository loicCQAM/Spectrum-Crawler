var pg = require('pg');
var client = new pg.Client({
  user: "gitpzsppghvqgu",
  password: "55f14664f66f91418ae522dcfbd815bc5a8ef9d59ef14868366e0bd73ddea686",
  database: "dekslnf5ran5pl",
  port: 5432,
  host: "ec2-174-129-242-183.compute-1.amazonaws.com",
  ssl: true
});

module.exports = client;