import pickle
import numpy as np
from sklearn.cluster import KMeans

def main():
    file_handle  = open("feature_name_array.npy", "rb")
    feature_name_list = np.load(file_handle, allow_pickle=True)
    feature_list = np.stack(feature_name_list[:,0], axis=0) # make 2D array from array of 1D arrays
    kmeans = KMeans(n_clusters=3, random_state=0).fit(feature_list)
    for i, label in enumerate(kmeans.labels_) :
        print("%s %s" %(label, feature_name_list[i,1]))
    
    pickle.dump(kmeans, open("kmeans_fitted.pkl", "wb"))

if __name__ == "__main__":
    main()
