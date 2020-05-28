#!/bin/env python3
import subprocess

"""
This script takes clusters_and_names.txt output and group files
into declared clusters
It has to be run in the same directory as memes directories/memes directories links

Usage: ./map.py

"""
stats = {
        "cluster_0": {"dank": 0, "newalternative": 0, "regular": 0},
        "cluster_1": {"dank": 0, "newalternative": 0, "regular": 0},
        "cluster_2": {"dank": 0, "newalternative": 0, "regular": 0}
        }

for key in stats:
    subprocess.call(["mkdir", "-p", key])

with open("outputs_and_models/clusters_and_names.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        try:
            cluster, filename = line.split(' ')
            if "dankmemes" in filename:
                stats["cluster_{}".format(cluster)]["dank"] += 1
            elif "newalternative" in filename:
                stats["cluster_{}".format(cluster)]["newalternative"] += 1
            elif "regularmemes" in filename:
                stats["cluster_{}".format(cluster)]["regular"] += 1
            else:
                print ("unknown meme type")
            print("Copying {0} to cluter {1}...".format(filename, cluster))
            subprocess.call(["cp", str(filename.strip()), "cluster_{}".format(str(cluster))])
        except Exception as e:
            print ("Error while copying: {}".format(e))
print(stats)

