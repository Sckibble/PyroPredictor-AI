# PyroPredictor-AI
This is PyroPredictor's repository. This is an ai that predicts a fire danger level for a given day with basic weather metrics.
Usage:
The available model and web page is trained on data from los angeles going back to 01/01/2000. When the user clicks the predict button the visual crossing api is called and returns data for the next 7 day forecast. This data includes the dates, max temps for each day, humidity, solar radiation, wind speed, wind gust, precipitation amount, and precipitation cover. Then the data is fed through the trained model and then returns a predicted fire danger level for each day.
