# Sports Prediction for CS:GO

An attempt at predicting match winners for the team-based game CS:GO using various machine learning/statistical learning methods, including linear regression, logistic regression, linear discriminant analysis, random forests and neural networks. A re-write to fix bugs and increase efficiency is currently underway. Using only a few features and with no parameter tuning, classification accuracy is at 61%. See histogram.png for an example of how inseparable the win/loss classes are.

Features (re-written):
- Average percentage of rounds won against all common opponents
- Number of high-profile games played in last ~100 days
- HLTV ranking
- Average HLTV 2.0 ratings over last ~50 days
- Percentage of rounds won on current map in last ~60 days

Features (to re-write):
- Interaction terms
- Standard deviation terms
- Percentage of CT rounds won * percentage of T rounds won against all common opponents
- Average HLTV 2.0 ratings over all common opponents
- Average percentage of rounds won in last ~60 days

All database files used have been removed for the public version, as HLTV forbids re-hosting of their (hard-earned) data.
