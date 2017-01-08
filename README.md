# NFL-PBP
A logistic regression algorithm designed to estimate the probability of a team winning a NFL game on a play by play basis.

## Resources:
* https://gallery.cortanaintelligence.com/Experiment/New-NFL-Play-by-Play-1
* [NFLSavant.com Dataset](http://nflsavant.com/about.php)



## Summary
First checkout this summary video.

I decided for this Data Science project, I would put together a logistic regression equation to estimate a team’s chances of winning on a play by play basis. What you are watching is the output of the algorithm as it adjusts after each play in the game.

This project started off using NFL Play by Play data provided by NFLsavant.com for the 2013-15 seasons. NFLsavant’s dataset is very rich providing a lot of detail on each play of the game, such as a which team currently possesses the ball and its location on the field. However, it lacked some information for my purposes such as the score of the game during each play. Therefore, I wrote a script(NFL_data_prep.py) to first to prepare the data which added columns to the dataset that I found useful. In addition to the score, the script added information on the amount of time since the start of the game, cumulative yards and number of plays for each teams.

With the updated dataset I used Microsoft’s Azure’s Machine Learning Studio to train a logistic regression algorithm. Use this [link]( https://gallery.cortanaintelligence.com/Experiment/New-NFL-Play-by-Play-1
) to copy the Azure experiment to your workspace. With the experiment setup you can view the output with NFL_view_game.py.
