README
StarCraft Project: Dynamic Army Prediction

Jiehong Jiang		jjhjiang@ucdavis.edu		914974552
Colin Beardshear	crbeardshear@ucdavis.edu	914385840
Malini Pathakota	mmpathakota@ucdavis.edu		913241367
Hoseung Lee		hoslee@ucdavis.edu		914001975
Lacey Campbell		lbcampbell@ucdavis.edu		912170808
Sri Kavya Dindu		sdindu@ucdavis.edu		650804061

Introduction
Our goal is to predict the enemy’s army formation by scouting and using the
gathered information about the number of buildings, construction units, and
army units they have. If the player can correctly predict what’s coming for
them, they can make a better strategic decision about how to beat their
opponent.

Aspiration
A dynamic army prediction algorithm could ultimately be utilized by gameplay
bots in real games. Since the algorithm was built to observe general features
in StarCraft, instead of being given the tech tree for a specific faction
first, it can be easily trained to predict the actions of opponents in
different factions.

Plan
To make our methods understandable and approachable, we mainly use linear
regression as a statistical approach to analyze the relationship between every
pair of two units; in order to predict a specific unit, we use its relationship
with all the others. The initial model is less effective as the game
progresses, so we partition the game into ten minute sections that each get
their own linear regression model. We compare this to a Bayesian Model
predicting the opponent’s opening build to determine how our prediction
accuracy compares to other models.

