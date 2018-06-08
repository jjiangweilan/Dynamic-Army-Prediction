# StarCraft Project: Tactical Path Planning for Reconnaissance

-------------

| Group Member     | Email Address            | SID       |
| ---------------- | ------------------------ | --------- |
| Jiehong Jiang    | jjhjiang@ucdavis.edu     | 914974552 |
| Colin Beardshear | crbeardshear@ucdavis.edu | 914385840 |
| Malini Pathakota | mmpathakota@ucdavis.edu  | 913241367 |
| Hoseung Lee      | hoslee@ucdavis.edu       | 914001975 |
| Lacey Campbell   | lbcampbell@ucdavis.edu   | 912170808 |
| Sri Kavya Dindu  | sdindu@ucdavis.edu       | 650804061 |

-------------

## Introduction
#### Problem

StarCraft II is a RTS game where players gather resources and strategically
spend them on units, buildings, and research in order to achieve the ultimate
goal of overpowering the opponent and winning.
Because this game relies heavily on choosing the right strategy early in the
game, being able to predict the enemy's army formation becomes a very valuable
skill.
Current army prediction algorithms learn from data gathered from gameplays on
build orders, amount of resources, and current army formation to predict which
strategy the enemy is using.
However, in addition to determining the strategy the enemy is using, being able
to predict every specific build the enemy makes during certain periods of time
during the game drastically increases the player’s chance of victory.
If the player can correctly predict the exact units that are coming for them at
specific times during the game, they can make better decisions on how to
counter the enemy.
Our objective is to create an algorithm that predicts the enemy’s army
composition given the information that’s been gathered by scouts, including
construction units, buildings, and current army formation.
We call this _Dynamic Army Prediction_.

There are currently many algorithms that predict the strategy the enemy will
utilize based on their army composition and information gathered from the
scouts; however, there are no algorithms specifically aiming to predict what
the enemy will build next based on the units they already possess, thus making
our solution to the problem of army prediction unique.

One such algorithm that predicts the enemy’s overall strategy rather than
immediate builds is a Bayesian Model for Opening Prediction.
This project predicts the enemy’s opening strategy and its possible technology
trees; however, it differs from our approach in two main ways.
First, the model predicts a strategy, whereas we focus on current army
composition and, ultimately, future army composition.
Secondly, it predicts the strategy at the beginning of the game, whereas as our
solution is a dynamic/real time implementation.
Another similar project is Combat Prediction based upon the Lanchester
Attribution Laws.
This project uses the above mentioned model to hypothesize about the enemy
army’s combat strategies, technology, and resources.
It addresses a much wider scope than our solution, and, unlike the previously
stated project, Combat Prediction aims to work in real time.

Link to enemy strategy prediction algorithm:

[https://hal.archives-ouvertes.fr/hal-00607277/file/OpeningPrediction.pdf](https://hal.archives-ouvertes.fr/hal-00607277/file/OpeningPrediction.pdf "Enemy Strategy Prediction Algorithm")

Dynamic army prediction is a very interesting problem to solve because, to our
knowledge, not many attempts have already been made to solve this specifically.
Most prediction models focus on the overall strategy the enemy will utilize
based on their opening build order, while we want to focus on immediate builds
at any point during the game.
This problem is also technically interesting because it is difficult to
determine the relationships between every unit created as well determine how
these relationships evolve as time progresses within the game.
This requires a large amount of training and implementing approaches, such as
linear regression.

-------------

## Aspiration
#### Solution

We will mainly use a statistical approach to analyze the relationships between
two units.
We will extract data from the replay files regarding the amount of units made
and what time they were made, analyze every pair of different units to evaluate
whether the units even have a relationship, and then determine the regression
model that best fits the pair.
We will also evaluate how the relationship between each pair of units changes
as the game progresses.
Then, we will use the multiple regression models determined for each pair to
predict what units will be created in the future, given what units had already
been created in the game.
Moreover, since the method is only based on the amount of units that are
created throughout the match, we may also use machine learning methods to
process the data to dig hidden relationships.
Although the goals of the projects aren’t completely similar, we can use the
model mentioned earlier that predicts an opponent’s opening build order using a
Bayesian Model to provide a baseline for how the accuracy of our prediction
model compares to existing models.

Neural and Bayesian networks would be able to solve our problem; however,
because many units seem to have linear relationships with each other, the
simpler solution of linear regression can be utilized.
Linear regression is the most easily understandable and approachable among all
solutions we have thought of so far.
Linear regression is also the most doable solution for this problem within our
restricted time frame.
Most of the other workable machine learning approaches that we thought of are
supervised, and accurately labeling all our data within this timeframe seemed
infeasible.

This algorithm will contribute to solving the problem of dynamic army
prediction, as no similar prediction algorithms exist thus far.
However, many improvements can still be made to this algorithm to make it more
accurate.
The algorithm can be expanded not just to learn from data involving units being
created, but also learn from data involving the layout of the map being played
on and data on which resources were being gathered.
It can also be further trained with replays with different factions because the
algorithm’s observation of features is based on the general concept of
StarCraft II rather than specifics, such as knowing the tech tree of one
faction first.
This algorithm can ultimately be utilized by other gameplay bots to make
predictions in real time in order to assist the player.
Our algorithm would provide a starting point for others to add to in order to
eventually develop a highly accurate army prediction model.

-------------

## Plan
#### Design and Technical Approach

We propose using Linear Regression or some other statistical model to predict
the amounts of complementing units over time.
For instance, Mutalisks and Zerglings are commonly used together, so we will
form a regression model which predicts their exact correlation.
In addition, we plan to use another model to dynamically predict the enemy’s
army composition from the available data (obtained by scouting).
In general, Linear Regression is effective for highly correlated data members.
Thus, we believe using it for selected complementary units would result in
accurate predictions of future unit builds.
However, it may fall short in dynamic army prediction, since game unit
compositions vary more widely during the later parts of the game.
For instance, predicting based on buildings would be ineffective because both
players are likely to have all of the buildings; late game scenarios diverge
from generic build orders, creating a much larger problem space.
As later in the game, a single model’s accuracy would decrease significantly,
we propose using several separately calibrated models for the different
partitions of game time.
For example, minute 0-10, 10-20, 20-30 would have their own unique linear
regression models for each unit pair.
The partition boundaries may vary as we experiment with different partition
sizes.

#### Technology Stack

Our team will work on both Linux and the MAC OS.
Since we have chosen the SC2 API and numpy/mathplotlib as our mathematical
computing package, the main languages we will use are C++ and Python.

We will first extract data using the s2client-api from the provided replay
files in a JSON format containing information on the type of unit created, the
amount of unit created, and what times in seconds they were created, for both
the player and the enemy.
The extracted data will be in this form:
“Zerg” : [1, 10, 43, 89].

Once the JSON file has been created, we will use Matplotlib and numpy (a
scientific computing package based in Python) to identify the specific
relationships between the every pair of units. We will also form different
linear regression models based on which partition of the game the player is in
using a similar approach.
Finally, we will design the final mathematical model based on these previous
models to be able to dynamically predict the enemy’s army formation.

Since our solution requires training from large sets of data in order to find
the best possible correlation, we will use Numba (a numpy aware compiler) to
reduce execution time by implementing numpy arrays.
If time permits, we will use SK-Learn for a more machine learning approach to
this problem.
We will use this to data mine and create linear regression models as well as
more complex mathematical models.

Finally, for testing, we’ll be using Valgrind for catching memory issues.
Since we are working with a large data set and aim for a dynamically productive
solution, Valgrind allows us to automatically detect any issues connected to
memory management and treading bugs and will profile our programs in detail to
help us see where exactly we went wrong.
We will also be implementing C++ unit testing as we develop to ensure each part
is working as it should separately and can be integrated into the larger
solution smoothly.

Although not officially part of our technology stack, GitHub plays a major role in the development of our solution.
Many of the APIs we are using are sourced from GitHub (i.e SC2 and Numpy).
We will primarily be using sc2-api to carry out our goals.
The sc2-api provides access to in-game state observation and unit control.
Other Starcraft II AI resources are on GitHub as well, so if we plan on using
something other than the CommandCenter, GitHub will be essential for carrying
out our project.
Also, we plan to use GitHub to document our own code.
At the end of our project, all our code will be committed, along with a
detailed explanation of the solution as well as an implementation guide.
Last but not least, GitHub will be a major part of how our team divvies up the
tasks and communicates about each other’s code contributions.

#### Evaluation

We will use k-fold cross-validation testing in other to evaluate the success of
our dynamic army prediction algorithm.
We will randomly split the data we extracted from the replay files into 10
equal subsets.
9/10ths of this data will be used for training the army predictor, while the
leftover data is held as the validation set for the model.
The predictions the model makes will be compared to the data and patterns
within the validation set in order to determine the model’s accuracy.
This process will be repeated 10 times so that each piece of data is used in
the validation set exactly once, and then we will average the accuracy
determined from each test to obtain a final percentage of the accuracy of our
model.

# Setting Up the Program

#### Data Extraction
How to:

  1. Replace your s2client-api/examples/replay.cc file
  
  2. Open the replay.cc file and go to line 21. There should be a line of code that looks something like this : 
  
  const char* kReplayFolder = "C:/Program Files (x86)/StarCraft II/Replays/Used/";
  
  This is where the replay files should be located for data extraction.
  
  3. If you wish to change the replay directory, replace the code inside of the quotations marks with your desired directory.
  
  4. Get Microsoft Visual Studio and Build s2client-api 
  (Install api : https://github.com/Blizzard/s2client-api/blob/master/docs/building.md)
  
  5. run replay.exe (just type this in and press enter on terminal or cmd)
  
  6. At the end of every match, the terminal/cmd should output a json formatted unit count to the screen.
  
  7. At the end of the first game, a file called "data.json" should be created in your s2client-api/build/bin folder
  
  8. Every time the json formatted unit count gets printed on to the terminal/cmd, the data.json file will be updated with the new data
  
  9. This will continue until the program has run through ALL of the replays in the replay directory. So if you just want to analyze one game, make sure that there is only one game in your replay directory. 
  
  10. If you wish to rerun this program delete your prior data.json or move it out of the bin folder, then you can run replay.exe again. 
  
  #### Data Visualization 
  
# Additional Programs
#### UnitLog branch
  In the UnitLog folder of this repository there are several zip files. Some of these are prototypes of the data extraction replay.cc program. The programs in these zip files are similar to the main replay.cc file in that it prints out data into the bin folder, but it is just a build order txt file instead of the json unit log file. There is also a tutorial.cc file that can log the build order for live games. More details are in the README inside these zip files. 
  
  UnitLog.zip : Live Games
  
  UnitLogReplays.zip : Build orders for replays
  
#### Win Prediction Program 
Data Extraction for Win Loss Prediction

Win Loss requires specific data and therefore requires additional data collection. 


How to:

1. Replace the s2client-api/examples/sc2_coordinator with the coordinator file sc2-Coordinator from the WinLoss prediction repo. 


2. This file will extract the enemy data


3. Now replace the pre-existing s2client-api/examples/replay.cc file with the replay.cc file found in WinLoss prediction. 


4.Make sure to change the paths for kReplayFolder to the location of your file
	a.This file extracts health information along with the number of 	units created at current moment in time. 


5.Follow the same steps as stated above for normal data extraction into the JSON file. 


6.Convert this JSON into a .txt file and run this file with win_loss_parser.py to compute and extract the necessary data to run with Predict.py. 


Predict.py Instructions
Loading Input File: 


1.Launch Microsoft Excel and click on the parsed .txt file and select “import” to display the Text Import Wizard.


2. Select “Fixed Width” and click “Next”.


3.Click on the line in the data preview to create the necessary field break lines. Each break line should be created to separate one field from the other, then click “Next”.


4.Click “Finish”, “Ok”, then import the data


5.Save your file, select “CSV(Comma delimited)”.


Running Predict.py
1.To run Predict.py, you will need to have Python installed on your system along with the dependencies such as Numpy, Pandas etc. 
	a.We used Enthought’s python IDE Canopy which supports all the		dependencies.

	Link: https://www.enthought.com/product/canopy/. 


2.Be sure to replace the following path in Predict.py to where your specific data file islocated 


3.Now simply, if using Canopy, run your files by pressing the build green arrow at the top of the interface.








