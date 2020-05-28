#!/usr/bin env python3

"""
With this script you can simulate an algorithm recommending memes
It recommends meme from given cluster given type and asks user for rating.
After rating the meme probabilities are recalculed and based on them 
it recommends another meme

Usage:
    ./probabilities.py

ATTENTION!
Requires python3.6 or higher
"""

import random
import collections


NUM_OF_CLUSTERS = 3
TYPES_INSIDE_CLUSTER = ["with_text", "without_text"]

def calculate_probs(probs, cluster, liked):
    """
    This function recalculates probabilities of choosing meme from given clusters
    """
    if int(liked) == 1:
        print (f"image rated: {liked}, calculating probs...")
        probs[cluster] /= 0.99
        probs[cluster] = min(probs[cluster], 1)
        for key in probs:
            if key == cluster:
                continue
            probs[key] *= sum(probs.values())
            probs[key] = max(probs[key], 0)
    elif int(liked) == 0:
        print (f"image rated: {liked}, calculating probs...")
        pass
    elif int(liked) == -1:
        print (f"image rated: {liked}, calculating probs...")
        probs[cluster] *= 0.99
        probs[cluster] = max(probs[cluster], 0)
        for key in probs:
            if key == cluster:
                continue
            probs[key] /= sum(probs.values())
            probs[key] = min(probs[key], 1)
        pass
    else:
        print("This should not happen")
        pass
    return probs

clusters = range(NUM_OF_CLUSTERS)
probs = collections.OrderedDict()

for cluster_number in clusters:
    for cluster_type in TYPES_INSIDE_CLUSTER:
        probs[f"cluster_{cluster_number}_{cluster_type}"] = 1/(len(clusters)*len(TYPES_INSIDE_CLUSTER))

print(probs)
print(probs.keys())
print(probs.values())
while True:
    liked = None
    chosen_cluster = random.choices(list(probs.keys()), weights=list(probs.values()))[0]
    print(chosen_cluster)
    while liked not in ["-1", "0", "1"]:
        liked = input("Choose 1, 0 or -1 whether you like, neutral or dislike meme\n") 
    print(f"Image from {chosen_cluster} rated: {liked}")
    probs = calculate_probs(probs, chosen_cluster, liked)
    print(probs)
