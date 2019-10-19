Scrapes match and player data from HLTV, then removes unneeded data
Be careful of dependency of run order, playersParser drops matches which aren't in matches.csv, so run it after matchesParser
Uncertainty and time discounting has been removed for COs. Can consider increasing the CO parameters while using appropriate time discounting.
COs excludes matches where the CO is actually themselves. Could be useful to include, as has good predictive power, but could skew the reliability of the stat.
Interval is ignored in corw.py
Consider dropping first few samples in finished dataset, were made using incomplete data because scraping started too early for them