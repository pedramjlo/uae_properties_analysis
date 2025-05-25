import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class ClusterAnalysis:
    """
    A general-purpose class for clustering analysis.
    Provides reusable tools like the Elbow Method, scaling, and KMeans fitting.
    """
    def __init__(self, data):
        """
        Initializes with a CSV file path or a pandas DataFrame.
        """
        if isinstance(data, str):
            self.data = pd.read_csv(data)
        elif isinstance(data, pd.DataFrame):
            self.data = data.copy()
        else:
            raise ValueError("data must be a path to CSV or a pandas DataFrame.")

    def scale_features(self, features):
        """
        Scales numeric features using StandardScaler.
        Returns a NumPy array of scaled data.
        """
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.data[features])
        return scaled_data

    def elbow_method(self, features, max_clusters=10):
        """
        Applies the Elbow Method on selected features.
        Plots inertia vs. number of clusters to help determine optimal k.
        """
        scaled_data = self.scale_features(features)
        inertia_values = []

        for k in range(1, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(scaled_data)
            inertia_values.append(kmeans.inertia_)

        # Plot the elbow curve
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, max_clusters + 1), inertia_values, marker='o', linestyle='--')
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Inertia")
        plt.title("Elbow Method for Optimal k")
        plt.grid(True)
        plt.show()

        return inertia_values

    def fit_kmeans(self, features, k):
        """
        Fits KMeans to selected features using specified number of clusters.
        Returns the model and predictions.
        """
        scaled_data = self.scale_features(features)
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(scaled_data)
        self.data["Cluster"] = labels
        return kmeans, labels

    def get_data(self):
        """
        Returns the internal dataset, including clusters if assigned.
        """
        return self.data.copy()


a = ClusterAnalysis(data='./dataset/cleaned_data/cleaned_uae_properties_data.csv')
print(a.elbow_method(features=["Rent"]))