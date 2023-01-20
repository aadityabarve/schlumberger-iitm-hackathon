//Contains APIs related to listing and submitting coding problems on front end

const express = require('express');
let router = express.Router();
const fs = require('fs');
const request = require('request');
const mysqlConnection = require('../db_connection');
var constants = require('../constants');
const languagesTable = constants.languagesTable;
const news_feed = constants.newsfeed;

router.get('/summary', function(req,res){
  const url = req.body.text;
  const runRequestBody = {
      text: text
  };

  request.post({
      url: "https://127.0.0.1:8000/text-summarizer/",
      json: runRequestBody
  },
  function(error, response, body){
    console.log("Error", error);
    JSON.stringify(body);
    console.log("Body", body);
    return res.status(200).json(body);
  });
})

router.get('/newsfeed', function(req,res){
  return res.status(200).send({news: news_feed});
})

router.get('/getdata/:id', function(req,res){
  var url = "";
  var id = req.params.id;
  console.log(id);
  for(var i=0;i<news_feed.length;i++)
  {
    if(news_feed[i].id == id)
    {
      url = news_feed[i].url;
      break;
    }
  }
  return res.status(200).send({url: url});
}
)
module.exports = router;
