var AWS = window.AWS;
var parser = document.createElement('a');
parser.href = window.location.href;
var raw_code = parser.search;
var auth_code = raw_code.slice(6,);
console.log("parser = ", parser);

console.log("raw_code = ", raw_code);
console.log("auth_code = ", auth_code);
var token_response = "";
var settings = {
    "async": false,
    "crossDomain": true,
    "url": "https://YOUR_DOMAIN.auth.us-east-1.amazoncognito.com/oauth2/token",
    "method": "POST",
    "headers": {
        "content-type": "application/x-www-form-urlencoded"
    },
    "data": {
        "grant_type": "authorization_code",
        "client_id": "",
        "redirect_uri": "https://dkqtjjobwip8d.cloudfront.net/dining_chat.html",
        "code": auth_code
    }
}
$.ajax(settings).done(function (response) {
    token_response = response;
});

var messages = [],
lastUserMessage = "",
talking = true;
$.when($.when(firstStep()).then(secondStep)).then(thirdStep);

function firstStep() {
  AWS.config.region = 'us-east-1';
  var token_response_id_token = token_response.id_token;
  var refresh_token = token_response.refresh_token;
  console.log("token response = ")
  console.log(token_response)

  AWS.config.credentials = new AWS.CognitoIdentityCredentials({
      IdentityPoolId: '',
      // format: https://cognito-idp.{region}.amazonaws.com/{userPoolId}.
      Logins: {'cognito-idp.us-east-1.amazonaws.com/us-east-????????': token_response_id_token}
  });
}

function secondStep() {
  AWS.config.credentials.refresh((error) => {
      if (error) {
        console.log(error);
      } else {
        console.log('logged in');
      }
  });
}

function thirdStep() {
  AWS.config.credentials.get(function(err) {
    if (!err) {
      var accessKeyId = AWS.config.credentials.accessKeyId;
      var secretAccessKey = AWS.config.credentials.secretAccessKey;
      var sessionToken = AWS.config.credentials.sessionToken;
      AWS.config.update({
          accessKeyId: accessKeyId,
          secretAccessKey: secretAccessKey,
          sessionToken: sessionToken
      })
      sdk = apigClientFactory.newClient({
        apiKey: "",
        accessKey: AWS.config.credentials.accessKeyId,
        secretKey: AWS.config.credentials.secretAccessKey,
        sessionToken: AWS.config.credentials.sessionToken
      }); 
    }
  });
}

function chatbotResponse() { 
  var params = {};
  console.log(JSON.stringify({text:lastUserMessage}));
  var body = {text: lastUserMessage};
  var additionalParams = {};
  chatbot_name = "Pops"
      
  console.log(params, body, additionalParams);
  sdk.chatbotPost(params, body, additionalParams)
    .then(function(result){
        received = JSON.parse(result.data.body).message;
        bot_message = received;
        messages.push("<b>" + chatbot_name + ":</b> " + bot_message);
        for (var i = 1; i < 8; i++) {
        if (messages[messages.length - i])
           document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
       }
    }
 )
}

function newEntry() {
//if the message from the user isn't empty then run 
if (document.getElementById("chatbox").value != "") {
    lastUserMessage = document.getElementById("chatbox").value;
    document.getElementById("chatbox").value = "";
    //adds the value of the chatbox to the array messages
    messages.push("<b>" + "You" + ":</b> " + lastUserMessage);
    chatbotResponse();
    //add the chatbot's name and message to the array messages
  }
}

//runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3 || key == 66) {
    //runs this function when enter is pressed
    newEntry();
  }
}

function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
} 