import time
import sys
import random
import os
import concurrent.futures
from datetime import datetime
from idgenerator.UniqueIdGenerator import UniqueIdGenerator
from idgenerator.RedisUniqueIdGenerator import RedisUniqueIdGenerator

#idgen = RedisUniqueIdGenerator(0);

totalNumPods = -1

outputFolder = 'output/'

def get_current_datetime():
    return datetime.now();

def keep_incrementing(totalNumPods, specificPodId):
    idgen = UniqueIdGenerator(totalNumPods, specificPodId);
    out_file = open(f"{outputFolder}/unique_ids_{specificPodId:02d}.csv", "w");
    output_list = []
    for x in range(20000):
        next_id, asup_id_16chars, served_date_time = idgen.get_next_id();
        #print("Count: {:05d} - POD {} {} at {} - {}".format(x, pod_id, next_id, served_date_time, asup_id_16chars));
        text = "Count: {:05d}, totalNumPods {:02}, POD {:02}, {}, {}, {}".format(x, totalNumPods, specificPodId, next_id, served_date_time, asup_id_16chars);
        print(text);
        output_list.append(text);
        out_file.writelines(f"{text}\n");
        sleep_time = random.randrange(100);
        time.sleep(sleep_time/1000);
    out_file.close();
    return output_list;

def main(argv):
    """
    Expected arguments:
    1st: Total number of pods
    2nd: Specific Pod ID
    """
    if len(argv) < 2:
        print(f"Total number of pods or specific pod id not found")
        sys.exit(1)
    totalNumPods = int(argv[0])
    specificPodId = int(argv[1])
    #if not os.path.exists(outputFolder):
    #    os.makedirs(outputFolder)
    print(f"Starting this POD with Specific Pod ID as {specificPodId} out of the total number of PODs: {totalNumPods}")
    served_date_time = get_current_datetime();

    print("Simulate few AIS pods via multiple threads and request unique ids")
    keep_incrementing(totalNumPods, specificPodId)

if __name__ == "__main__":
    main(sys.argv[1:])





