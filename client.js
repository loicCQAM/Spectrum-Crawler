var pg = require('pg');
var client = new pg.Client({
  user: "dlyloibzwzkiez",
  password: "5f4156a59e17f27e7026f84d9f9b8c02db75549424fb1d91b8f903662facd9df",
  database: "d3jaj8cgnql4go",
  port: 5432,
  host: "ec2-54-235-92-244.compute-1.amazonaws.com",
  ssl: true
});

module.exports = client;