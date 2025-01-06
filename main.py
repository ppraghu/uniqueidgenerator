import time
import sys
import random
import os
import concurrent.futures
from datetime import datetime
from idgenerator.UniqueIdGenerator import UniqueIdGenerator
from idgenerator.RedisUniqueIdGenerator import RedisUniqueIdGenerator

#idgen = RedisUniqueIdGenerator(0);

num_pods = 20

outputFolder = 'output/'
    
def get_current_datetime():
    return datetime.now();

def keep_incrementing(processNumber, pod_id):
    idgen = UniqueIdGenerator(num_pods, pod_id);
    out_file = open(f"{outputFolder}/unique_ids_{processNumber}_{pod_id}.csv", "w");
    output_list = []
    for x in range(100):
        next_id, asup_id_16chars, served_date_time = idgen.get_next_id();
        #print("Count: {:05d} - POD {} {} at {} - {}".format(x, pod_id, next_id, served_date_time, asup_id_16chars));
        text = "Count: {:05d}, Process {}, POD {:02}, {}, {}, {}".format(x, processNumber, pod_id, next_id, served_date_time, asup_id_16chars);
        print(text);
        output_list.append(text);
        out_file.writelines(f"{text}\n");
        sleep_time = random.randrange(100);
        time.sleep(sleep_time/1000);
    out_file.close();
    return output_list;

def main(argv):
    if len(argv) < 1:
        print(f"Process number nout found")
        sys.exit(1)
    processNumber = argv[0]
    #if not os.path.exists(outputFolder):
    #    os.makedirs(outputFolder)
    print(f"Process number: {processNumber}")
    print("First, delete all contents from Redis")
    #idgen.delete_all_contents()
    served_date_time = get_current_datetime();

    print("Simulate few AIS pods via multiple threads and request unique ids")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for pod_id in range(num_pods):
            futures.append(executor.submit(keep_incrementing, processNumber, pod_id))
        for future in concurrent.futures.as_completed(futures):
            output_list = future.result();
            #out_file.writelines([f"{a_line}\n" for a_line in output_list]);
        #out_file.close();

if __name__ == "__main__":
    main(sys.argv[1:])





