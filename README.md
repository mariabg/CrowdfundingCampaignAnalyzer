# Crowdfunding Campaign Analyser

Will your crowdfunding campaign succeed? This code cleans [Kickstarter](kickstarter.com) data and outputs a .csv file ready to analyse. Here is how a row of this cleaned file looks in json:
```
{
  "name": "Into My Escape",
  "id": 235996108,
  "blurb": "Help us take London a little step closer to well being and happiness!",
  "category": "Art",
  "pledged": 27.92,
  "backers": 2,
  "countryName": "United Kingdom",
  "goal": 1329.48669,
  "success": 0,
  "length": 21,
  "launchedMonth": 9,
  "launched_at": 5-9-2016,
  "deadline": 26-9-2016,
}
```
Note that the currencies vary over the country, so they are converted all to USD using the exchange rate at the launch moment. The length is given in days.

### Play with the code

Projects data was obtained from [here](https://webrobots.io/kickstarter-datasets/). Download the latest files and put them into the data directory. If you want to use Plotly, don't forget to include your username and apikey at the beginning of the file. Now you are ready to go!

### Results

The [results slides](slides/Final%20Results.pdf) include visual representation of the data with [Plotly](https://plot.ly), [Carto](carto.com) and [Graphext](graphext.com), along with the most interesting results.

### To Dos

* Include a sentiment analysis of the description of the campaigns. I thought about using [this](https://github.com/clemtoy/WNAffect) code.
* Build a Neural Network to predict if a campaign will be successful – I am currently completing this task.

Any cool idea? Open an issue and we will discuss it.

### Contributing

Feel free to contribute to this project by working any of the to dos or including support to other crowdfunding websites – some are already available at https://webrobots.io, so there is no need to scrape the sites.

### Acknowledgments

This project was offered to the students of [Knowledge Discovery and Data Mining 1](http://kti.tugraz.at/staff/denis/courses/kddm1/). The lecture course covered all the theoretical concepts behind this topic and we were given some projects to put them freely into practice. The results of every project were shared with the other students who also decided to participate in the challenge.
