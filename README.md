# anomaly-detection

__This repo solves a problem given by India Mart hackathon. Problem is described as__

Recently a trend has been observed in the online marketplace that a lot of weight is given by the user to the price point of products in searches. In the USA, due to price transparency and ease of shopping, Amazon has taken over to become the default search engine for product discovery (surpassing Google).

Price acquisition at IndiaMART was started in 2015. Currently, there are 1lac categories with ~1.5cr Products in IndiaMART with the price. With such great coverage, comes the issue of accuracy.

Currently, due to the UGC content on Indiamart, we have a range of prices listed using a variety of units. We are looking for a working prototype solution to gauge the appropriate price range per unit for each of the categories listed on Indiamart.

Find hackathon link - https://www.hackerearth.com/challenges/hackathon/indiamart-hackathon/#themes

### The working app is installed on heroku. Find it [here](https://price-range-app1.herokuapp.com/price-range?cat=ladies%20palazzo)
#### APIs available on app are
* https://price-range-app1.herokuapp.com/price-range?cat=ladies%20palazzo

    gives price range for given main category
* https://price-range-app1.herokuapp.com/elbow-curve?cat=ladies%20palazzo

    gives elbow curve for given category to identify number of clusters
