import numpy as np
import StringIO
import base64
from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
import logging, itertools
import pandas as pd

logging.basicConfig(level=logging.INFO)
CLUSTER_COMPONENT_THRESHOLD = 5


class Cluster:
    def __init__(self, data):
        self.data = np.array(data).reshape(-1, 1)
        self.distance = None
        self.threshold = None
        self.lables = None

    def elbow_curve(self, num_cluster):
        img = StringIO.StringIO()
        X = self.data
        logging.info(len(X))
        num_cluster = num_cluster  if num_cluster <= len(X) else len(X)
        n_cluster = range(1, num_cluster)
        kmeans = [KMeans(n_clusters=i).fit(X) for i in n_cluster]
        scores = [kmeans[i].score(X) for i in range(len(kmeans))]

        # fig, ax = plt.subplots(figsize=(10, 6))
        # ax.plot(n_cluster, scores)
        # plt.xlabel('Number of Clusters')
        # plt.ylabel('Score')
        # plt.title('Elbow Curve')
        # plt.xticks(range(0, 20, 2))
        # plt.savefig(img, format='png')
        # plt.close()

        plot_url = base64.b64encode(img.getvalue())
        return plot_url

    def apply_kmeans(self, num_cluster):
        X = self.data
        num = num_cluster
        color_iter = itertools.cycle(['navy', 'turquoise', 'cornflowerblue',
                                      'darkorange'])
        kmeans = KMeans(num, random_state=0, init="k-means++")
        labels = kmeans.fit(X).predict(X)
        self.lables = labels
        # fig = plt.figure(1, figsize=(14, 14))
        for i, (ind, color) in enumerate(zip(range(num), color_iter)):
            l = X[labels == i, 0]
            # plt.scatter(np.array([i for j in range(len(l))]), l, 8, color=color)

        return kmeans

    def get_distance_threshold(self, model, outliers_fraction):
        def getDistanceByPoint(data, model):
            distance = pd.Series()
            for i in range(0, len(data)):
                Xa = data[i][0]
                Xb = model.cluster_centers_[model.predict(Xa)[0]]
                distance.set_value(i, np.linalg.norm(Xa - Xb))
            return distance
        # get the distance between each point and its nearest centroid. The biggest distances are considered as anomaly
        distance = getDistanceByPoint(self.data, model)
        number_of_outliers = int(outliers_fraction * len(distance))
        logging.info("number of outliers %s" % str(number_of_outliers))
        threshold = distance.nlargest(number_of_outliers).min()
        logging.info("threshold distance is %s" % str(threshold))
        self.threshold = threshold
        self.distance = distance
        return threshold

    def get_silhoutte_outliers(self):
        r = []
        for i in range(len(self.data)):
            if self.distance[i] >= self.threshold:
                print "anomaly %s %s" % (self.data[i], self.distance[i])
                r.append(self.data[i][0])
        return r

    def get_cluster_number_outliers(self):
        r = []
        cluster_to_component = self.get_cluster_components(self.lables)
        print len(cluster_to_component)
        for x in cluster_to_component:
            if len(cluster_to_component[x]) < CLUSTER_COMPONENT_THRESHOLD:
               print "outliers %s %s" % (str(len(cluster_to_component[x])), " ,".join([str(y) for y in cluster_to_component[x]]))
               r += map(lambda k: k[0], cluster_to_component[x])
        return r

    def get_outliers(self):
        outliers = self.get_silhoutte_outliers()
        outliers += self.get_cluster_number_outliers()
        return outliers

    def get_cluster_components(self, lables):
        max_l = max(lables) + 1
        print max_l
        clsuter_to_component = {}
        for i in range(max_l):
            tmp = self.data[lables == i]
            tmp_indexes = self.data[lables == i]
            x = np.array([k for k in range(len(tmp_indexes))])
            clsuter_to_component[i] = tmp
        return clsuter_to_component

    def remove_outliers(self):
        r = self.get_outliers()
        logging.info("length of outliers are %s" % len(r))
        logging.info("all outliers are\n %s" % " ,".join(map(str, r)))
        q = []
        cnt = 0
        for i in range(len(self.data)):
            if self.data[i][0] not in r:
               q.append(self.data[i][0])
               cnt += 1
        if len(q) != 0:
            price_range = [min(q), max(q)]
        else:
            price_range = [None, None]
        return price_range


if __name__ == "__main__":
    a = [395.0,
 1300.0,
 395.0,
 399.0,
 399.0,
 399.0,
 399.0,
 399.0,
 210.0,
 880.0,
 900.0,
 260.0,
 260.0,
 280.0,
 350.0,
 230.0,
 230.0,
 230.0,
 230.0,
 350.0,
 185.0,
 200.0,
 150.0,
 200.0,
 465.0,
 190.0,
 250.0,
 220.0,
 90.0,
 90.0,
 100.0,
 120.0,
 60.0,
 180.0,
 325.0,
 325.0,
 325.0,
 189.0,
 159.0,
 159.0,
 125.0,
 209.0,
 159.0,
 159.0,
 159.0,
 159.0,
 159.0,
 159.0,
 169.0,
 159.0,
 159.0,
 159.0,
 159.0,
 159.0,
 159.0,
 209.0,
 209.0,
 209.0,
 209.0,
 209.0,
 209.0,
 209.0,
 169.0,
 169.0,
 169.0,
 169.0,
 169.0,
 189.0,
 169.0,
 189.0,
 189.0,
 189.0,
 189.0,
 189.0,
 150.0,
 595.0,
 255.0,
 180.0,
 180.0,
 440.0,
 189.0,
 209.0,
 209.0,
 130.0,
 380.0,
 175.0,
 180.0,
 170.0,
 175.0,
 150.0,
 150.0,
 150.0,
 160.0,
 150.0,
 250.0,
 90.0,
 150.0,
 225.0,
 220.0,
 300.0,
 350.0,
 325.0,
 200.0,
 250.0,
 250.0,
 250.0,
 190.0,
 230.0,
 200.0,
 220.0,
 160.0,
 250.0,
 125.0,
 1900.0,
 220.0,
 250.0,
 250.0,
 50.0,
 50.0,
 50.0,
 225.0,
 200.0,
 650.0,
 150.0,
 258.0,
 250.0,
 82.0,
 165.0,
 300.0,
 250.0,
 280.0,
 250.0,
 300.0,
 250.0,
 250.0,
 300.0,
 250.0,
 250.0,
 250.0,
 195.0,
 100.0,
 139.0,
 179.0,
 179.0,
 225.0,
 200.0,
 175.0,
 550.0,
 325.0,
 600.0,
 140.0,
 240.0,
 48.0,
 240.0,
 350.0,
 210.0,
 220.0,
 349.0,
 270.0,
 270.0,
 250.0,
 600.0,
 160.0,
 200.0,
 650.0,
 200.0,
 400.0,
 299.0,
 350.0,
 250.0,
 270.0,
 270.0,
 270.0,
 70.0,
 120.0,
 120.0,
 140.0,
 250.0,
 200.0,
 120.0,
 120.0,
 250.0,
 399.0,
 170.0,
 165.0,
 999.0,
 165.0,
 190.0,
 180.0,
 250.0,
 135.0,
 299.0,
 165.0,
 180.0,
 270.0,
 150.0,
 270.0,
 370.0,
 350.0,
 245.0,
 155.0,
 290.0,
 290.0,
 370.0,
 290.0,
 200.0,
 490.0,
 405.0,
 175.0,
 825.0,
 160.0,
 200.0,
 200.0,
 399.0,
 285.0,
 725.0,
 580.0,
 550.0,
 125.0,
 375.0,
 1635.0,
 195.0,
 90.0,
 240.0,
 160.0,
 170.0,
 650.0,
 225.0,
 250.0,
 950.0,
 140.0,
 200.0,
 200.0,
 300.0,
 200.0,
 200.0,
 130.0,
 240.0,
 340.0,
 1100.0,
 250.0,
 195.0,
 150.0,
 120.0,
 150.0,
 150.0,
 480.0,
 1285.0,
 195.0,
 352.0,
 800.0,
 350.0,
 175.0,
 270.0,
 185.0,
 110.0,
 250.0,
 250.0,
 160.0,
 340.0,
 300.0,
 370.0,
 370.0,
 300.0,
 300.0,
 350.0,
 210.0,
 300.0,
 799.0,
 150.0,
 220.0,
 150.0,
 4000.0,
 230.0,
 200.0,
 200.0,
 235.0,
 220.0,
 160.0,
 150.0,
 155.0,
 160.0,
 135.0,
 160.0,
 200.0,
 399.0,
 160.0,
 145.0,
 50.0,
 149.0,
 100.0,
 75.0,
 75.0,
 300.0,
 300.0,
 300.0,
 170.0,
 95.0,
 160.0,
 250.0,
 160.0,
 180.0,
 250.0,
 250.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 270.0,
 300.0,
 300.0,
 300.0,
 300.0,
 300.0,
 250.0,
 370.0,
 350.0,
 240.0,
 370.0,
 240.0,
 250.0,
 250.0,
 269.0,
 195.0,
 325.0,
 180.0,
 240.0,
 170.0,
 420.0,
 320.0,
 205.0,
 128.0,
 270.0,
 300.0,
 250.0,
 370.0,
 370.0,
 270.0,
 250.0,
 280.0,
 270.0,
 250.0,
 300.0,
 250.0,
 270.0,
 280.0,
 250.0,
 389.0,
 389.0,
 290.0,
 180.0,
 250.0,
 180.0,
 99.0,
 180.0,
 180.0,
 180.0,
 641.25,
 1999.0,
 245.0,
 295.0,
 50.0,
 260.0,
 325.0,
 260.0,
 400.0,
 170.0,
 320.0,
 320.0,
 320.0,
 320.0,
 320.0,
 320.0,
 180.0,
 699.0,
 200.0,
 160.0,
 160.0,
 160.0,
 140.0,
 200.0,
 260.0,
 170.0,
 899.0,
 250.0,
 199.0,
 1.0,
 999.0,
 505.0,
 160.0,
 350.0,
 225.0,
 225.0,
 300.0,
 345.0,
 300.0,
 140.0,
 200.0,
 275.0,
 275.0,
 350.0,
 700.0,
 350.0,
 150.0,
 350.0,
 350.0,
 350.0,
 120.0,
 250.0,
 160.0,
 250.0,
 160.0,
 135.0,
 210.0,
 350.0,
 350.0,
 350.0,
 350.0,
 199.0,
 165.0,
 199.0,
 150.0,
 150.0,
 250.0,
 300.0,
 300.0,
 180.0,
 345.0,
 200.0,
 325.0,
 200.0,
 200.0,
 200.0,
 200.0,
 599.0,
 2000.0,
 350.0,
 280.0,
 500.0,
 180.0,
 125.0,
 325.0,
 325.0,
 250.0,
 235.0,
 235.0,
 250.0,
 350.0,
 350.0,
 410.0,
 235.0,
 370.0,
 405.0,
 1495.0,
 225.0,
 225.0,
 320.0,
 270.0,
 320.0,
 260.0,
 270.0,
 150.0,
 150.0,
 258.0,
 250.0,
 160.0,
 250.0,
 160.0,
 150.0,
 330.0,
 210.0,
 474.0,
 370.0,
 150.0,
 255.0,
 300.0,
 300.0,
 300.0,
 125.0,
 100.0,
 275.0,
 300.0,
 65.0,
 249.0,
 150.0,
 150.0,
 130.0,
 130.0,
 130.0,
 130.0,
 330.0,
 324.0,
 324.0,
 285.0,
 285.0,
 280.0,
 260.0,
 200.0,
 350.0,
 220.0,
 180.0,
 200.0,
 140.0,
 260.0,
 725.0,
 300.0,
 300.0,
 300.0,
 300.0,
 150.0,
 150.0,
 300.0,
 95.0,
 150.0,
 150.0,
 150.0,
 150.0,
 150.0,
 150.0,
 150.0,
 150.0,
 150.0,
 150.0,
 150.0,
 125.0,
 105.0,
 175.0,
 370.0,
 350.0,
 120.0,
 140.0,
 200.0,
 225.0,
 160.0,
 160.0,
 160.0,
 430.0,
 220.0,
 120.0,
 190.0,
 270.0,
 300.0,
 370.0,
 230.0,
 270.0,
 370.0,
 370.0,
 370.0,
 370.0,
 370.0,
 370.0,
 260.0,
 370.0,
 249.0,
 230.0,
 370.0,
 370.0,
 249.0,
 195.0,
 399.0,
 999.0,
 130.0,
 325.0,
 130.0,
 325.0,
 130.0,
 140.0,
 230.0,
 230.0,
 230.0,
 250.0,
 150.0,
 260.0,
 140.0,
 140.0,
 240.0,
 140.0,
 240.0,
 140.0,
 299.0,
 190.0,
 300.0,
 150.0,
 200.0,
 150.0,
 150.0,
 150.0,
 300.0,
 170.0,
 575.0,
 170.0,
 575.0,
 140.0,
 155.0,
 110.0,
 140.0,
 200.0,
 250.0,
 250.0,
 250.0,
 250.0,
 300.0,
 300.0,
 300.0,
 270.0,
 265.0,
 550.0,
 349.0,
 299.0,
 349.0,
 349.0,
 150.0,
 150.0,
 150.0,
 210.0,
 170.0,
 220.0,
 145.0,
 235.0,
 130.0,
 300.0,
 290.0,
 425.0,
 380.0,
 150.0,
 125.0,
 185.0,
 150.0,
 150.0,
 150.0,
 150.0,
 200.0,
 250.0,
 190.0,
 425.0,
 700.0,
 425.0,
 300.0,
 1300.0,
 150.0,
 100.0,
 150.0,
 150.0,
 150.0,
 150.0,
 138.0,
 121.0,
 150.0,
 150.0,
 110.0,
 550.0,
 250.0,
 525.0,
 525.0,
 150.0,
 1200.0,
 600.0,
 600.0,
 550.0,
 195.0,
 245.0,
 499.0,
 240.0,
 170.0,
 165.0,
 237.0,
 300.0,
 250.0,
 300.0,
 250.0,
 80.0,
 230.0,
 250.0,
 350.0,
 171.0,
 140.0,
 125.0,
 399.0,
 140.0,
 140.0,
 650.0,
 260.0,
 525.0,
 525.0,
 475.0,
 299.0,
 299.0,
 500.0,
 500.0,
 500.0,
 440.0,
 395.0,
 195.0,
 210.0,
 160.0,
 250.0,
 160.0,
 750.0,
 299.0,
 200.0,
 380.0,
 90.0,
 250.0,
 199.0,
 199.0,
 550.0,
 300.0,
 120.0,
 550.0,
 550.0,
 550.0,
 550.0,
 550.0,
 550.0,
 550.0,
 260.0,
 275.0,
 225.0,
 225.0,
 350.0,
 350.0,
 250.0,
 220.0,
 299.0,
 350.0,
 220.0,
 350.0,
 210.0,
 450.0,
 449.0,
 499.0,
 499.0,
 449.0,
 450.0,
 185.0,
 150.0,
 275.0,
 799.0,
 495.0,
 999.0,
 495.0,
 740.0,
 375.0,
 320.0,
 200.0,
 350.0,
 650.0,
 120.0,
 220.0,
 300.0,
 220.0,
 220.0,
 220.0,
 195.0,
 470.0,
 250.0,
 115.0,
 750.0,
 650.0,
 650.0,
 650.0,
 650.0,
 650.0,
 120.0,
 400.0,
 400.0,
 180.0,
 199.0,
 180.0,
 200.0,
 200.0,
 75.0,
 299.0,
 425.0,
 369.0,
 499.0,
 320.0,
 499.0,
 175.0,
 350.0,
 350.0,
 350.0,
 350.0,
 350.0,
 195.0,
 300.0,
 300.0,
 300.0,
 195.0,
 195.0,
 3303.0,
 700.0,
 150.0,
 115.0,
 465.0,
 550.0,
 365.0,
 250.0,
 630.0,
 325.0,
 650.0,
 650.0,
 185.0,
 150.0,
 185.0,
 120.0,
 120.0,
 280.0,
 163.0,
 230.0,
 179.0,
 240.0,
 175.0,
 750.0,
 175.0,
 995.0,
 100.0]

    c = Cluster(a)
    kmeans = c.apply_kmeans(21)
    c.get_distance_threshold(kmeans, 0.01)