# Sports Prediction for CS:GO

An attempt at predicting match winners for the team-based game CS:GO using various machine learning/statistical learning methods, including linear regression, logistic regression, linear discriminant analysis, random forests and neural networks. A re-write to fix bugs and reduce feature generation time is currently underway. The old model classified winners with an accuracy of 67% - the current untuned model is at 61%. See histogram.png for an example of how intertwined the win/loss classes are.

CO = common opponents, H2H = head to head, Completeness = % of T rounds won * % of CT rounds won

Features (completed):
- Average round win percentages against all COs
- Number of high-profile games played in last ~100 days
- HLTV ranking points
- Average HLTV 2.0 ratings over last ~50 days
- Percentage of rounds won on current map in last ~60 days
- Days since last match

Features (to re-write or add): 
- Best of X dummy variable																																	
- Round win percentage/Completeness for last X days, historical and CO
- Average round win percentage for last X days, historical and CO
- Average round win percentage at halftime for last X days, historical and CO
- Start side dummy variable
- Round win percentage as T/CT for last X days, historical and CO
- Map
- Round win percentage for games starting as T/CT for last X days, historical and CO
- Change in ranking points over last X days
- Average player age
- Betting odds
- Time since last roster change
- Clutches for last X days, historical and CO
- Pistols won for last X days, historical and CO
- Round win percentage after 5/10/15/20/25 rounds in for last X days, historical and CO
- Map correlation as in tennis ML paper
- Add H2H. Curb no H2H matches by time discounting and dropping NA
- Whether a team has a stand-in
- Interaction terms
- Standard deviation terms

All database files have been removed out of respect for the company who collects it. A small sample is available in the root directory.
