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

import collections
import logging
import random
import time


logging.basicConfig(level=logging.INFO)
NUM_OF_CLUSTERS = 3
TYPES_INSIDE_CLUSTER = ["with_text", "without_text"]
# PROBS FACTOR MUST BE GREATER THAN 1
PROBS_FACTOR = 1.001


def dictionary_sum(dictionary):
    """
    This function returns the sum of dictionary
    where all values are just numbers using
    kahan sumation algorithm which minimizes numerical errors
    """
    dictionary_sum = 0
    kahansum_compensation = 0
    for key in dictionary:
        y = dictionary[key] - kahansum_compensation
        t = dictionary_sum + y
        kahansum_compensation = (t - dictionary_sum) - y
        dictionary_sum = t

    return dictionary_sum

def check_probs(probs):
    """
    This function checks if probabilites sums to 1
    """
    probs_sum = dictionary_sum(probs)
    assert probs_sum == 1

def normalize(dictionary):
    """
    This function normalize dictionary with numerical values
    so that they all sums up to 1
    """
    initial_sum = dictionary_sum(dictionary)
    for key in dictionary:
        probs[key] /= initial_sum

    return dictionary

def calculate_probs(probs, cluster, liked):
    """
    This function recalculates probabilities of choosing meme from given clusters
    probs - map of probabilities for all clusters
    probs[cluster] - probability of choosing next sample from given cluster
    cluster - sample from this cluster was rated
    liked - rate of the sample
    """
    if int(liked) == 1:
        logging.info(f"image rated: {liked}, calculating probs...")
        for key in probs:
            if key == cluster:
                continue
            else:
               probs[key] /= PROBS_FACTOR
        sum_of_probs_without_given_cluster = dictionary_sum({key:probs[key] for key in probs if key != cluster})
        probs[cluster] = 1 - sum_of_probs_without_given_cluster
    elif int(liked) == 0:
        logging.info(f"image rated: {liked}, calculating probs...")
        pass
    elif int(liked) == -1:
        logging.info(f"image rated: {liked}, calculating probs...")
        probs[cluster] /= PROBS_FACTOR
        sum_of_probs_without_given_cluster = dictionary_sum({key:probs[key] for key in probs if key != cluster})
        for key in probs:
            if key == cluster:
                logging.debug(f"cluster is {cluster} key is: {key}, value is {probs[key]}")
                continue
            else:
                probs[key] *= (1-probs[cluster]/PROBS_FACTOR)/sum_of_probs_without_given_cluster
                logging.debug(f"cluster is {cluster} key is: {key}, value is {probs[key]}")
    else:
        logging.error("Invalid Rate. This should not happen")
        pass
    while dictionary_sum(probs) != 1:
        probs = normalize(probs)
    check_probs(probs)
    return probs

def autodemotest(chosen_cluster, desired_decision):
    if chosen_cluster == list(probs.keys())[0]:
        return desired_decision
    else:
        return "0"

clusters = range(NUM_OF_CLUSTERS)
probs = collections.OrderedDict()

for cluster_number in clusters:
    for cluster_type in TYPES_INSIDE_CLUSTER:
        probs[f"cluster_{cluster_number}_{cluster_type}"] = 1/(len(clusters)*len(TYPES_INSIDE_CLUSTER))

while True:
    liked = None
    chosen_cluster = random.choices(list(probs.keys()), weights=list(probs.values()))[0]
    logging.debug(f"Chosen cluster is {chosen_cluster}")
    while liked not in ["-1", "0", "1"]:
        liked = input("Choose 1, 0 or -1 whether you like, neutral or dislike meme\n") 
#        liked = autodemotest(chosen_cluster, "-1")
#        liked = autodemotest(chosen_cluster, "0")
#        liked = autodemotest(chosen_cluster, "1")
#        liked = autodemotest(chosen_cluster, random.choice(["-1", "0", "1"])
        time.sleep(0.001)
    logging.info(f"Image from {chosen_cluster} rated: {liked}")
    probs = calculate_probs(probs, chosen_cluster, liked)
    logging.info(f"Probabilities: {probs}")

