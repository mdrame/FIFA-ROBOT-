
var federation = 'EUFA'
var market = 'classic'


fetch(`https://football-prediction-api.p.rapidapi.com/api/v2/list-federations`, {
	"method": "GET",
	"headers": {
		"x-rapidapi-host": "football-prediction-api.p.rapidapi.com",
		"x-rapidapi-key": "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
	}
}).then(function(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  // Read the response as json.
  return response.json();
})
.then(function(responseAsJson) {
  // Do stuff with the JSON
  console.log(responseAsJson);
})
.catch(function(error) {
  console.log('Looks like there was a problem: \n', error);
});
