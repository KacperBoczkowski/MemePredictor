
import collections
import logging
import random
import time

module_logger = logging.getLogger("meme_engine")
logging.basicConfig(level=logging.INFO)
NUM_OF_CLUSTERS = 3
TYPES_INSIDE_CLUSTER = []
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
        module_logger.info(f"image from cluster: {cluster} rated: {liked}, calculating probs...")
        for key in probs:
            if key == cluster:
                continue
            else:
               probs[key] /= PROBS_FACTOR
        sum_of_probs_without_given_cluster = dictionary_sum({key:probs[key] for key in probs if key != cluster})
        probs[cluster] = 1 - sum_of_probs_without_given_cluster
    elif int(liked) == 0:
        module_logger.info(f"image rated: {liked}, calculating probs...")
        pass
    elif int(liked) == -1:
        module_logger.info(f"image rated: {liked}, calculating probs...")
        probs[cluster] /= PROBS_FACTOR
        sum_of_probs_without_given_cluster = dictionary_sum({key:probs[key] for key in probs if key != cluster})
        for key in probs:
            if key == cluster:
                module_logger.debug(f"cluster is {cluster} key is: {key}, value is {probs[key]}")
                continue
            else:
                probs[key] *= (1-probs[cluster]/PROBS_FACTOR)/sum_of_probs_without_given_cluster
                module_logger.debug(f"cluster is {cluster} key is: {key}, value is {probs[key]}")
    else:
        module_logger.error("Invalid Rate. This should not happen")
        pass
    while dictionary_sum(probs) != 1:
        probs = normalize(probs)
    check_probs(probs)
    module_logger.info(f"Returning probabilities: {probs}")
    return probs


clusters = range(NUM_OF_CLUSTERS)
probs = collections.OrderedDict()

for cluster_number in clusters:
    if TYPES_INSIDE_CLUSTER:
        for cluster_type in TYPES_INSIDE_CLUSTER:
            probs[f"cluster_{cluster_number}_{cluster_type}"] = 1/(len(clusters)*len(TYPES_INSIDE_CLUSTER))
    else:
        probs[f"cluster_{cluster_number}"] = 1/(len(clusters))


