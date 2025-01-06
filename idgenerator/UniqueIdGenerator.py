import math
import time
from datetime import datetime, timedelta, timezone

MAX_VALUE = 10000

class UniqueIdGenerator:
    format_with_mins = "%Y%m%d%H%M";
    format_with_secs = "%Y%m%d%H%M%S";

    def delete_all_contents():
        print("Dummy implementation of delete_all_contents...");

    def get_current_datetime(self):
        return datetime.now(timezone.utc);

    def calculate_min_max_range(self):
        bucket_size = (int)(MAX_VALUE / self.num_pods);
        self.min = self.ais_pod_id * bucket_size;
        self.max = self.min + bucket_size - 1;
        print("No. of pods: {}, pod_id: {}, min: {}, max: {}".format(self.num_pods, self.ais_pod_id, self.min, self.max)); 

    def do_id_reset(self):
        self.next_id = self.min;
        self.id_reset_time = self.get_current_datetime();
    
    def __init__(self, num_pods, ais_pod_id):
        self.num_pods = num_pods;
        self.ais_pod_id = ais_pod_id;
        self.calculate_min_max_range();
        self.do_id_reset();
    
    def sleep_remaining_seconds(self):
        current_datetime = self.get_current_datetime();
        datetime_rounded_to_next_min = \
            current_datetime.replace(second=0, microsecond=0) + timedelta(minutes=1)
        timediff = datetime_rounded_to_next_min - current_datetime;
        timediff_secs = math.ceil(timediff.total_seconds());
        print(f"Sleeping for {timediff_secs} secs");
        time.sleep(timediff_secs);

    def still_in_current_minute(self):
        current_datetime = self.get_current_datetime();
        current_minutes = int(current_datetime.strftime(self.format_with_mins));
        id_reset_minutes = int(self.id_reset_time.strftime(self.format_with_mins));
        print(f"Current time {current_datetime}, Previous reset time {self.id_reset_time}");
        return (current_minutes == id_reset_minutes);

    def get_next_id(self):
        current_datetime = self.get_current_datetime();
        if (self.next_id > self.max):
            if (self.still_in_current_minute()):
                self.sleep_remaining_seconds();
            else:
                print("No need to sleep");
            self.do_id_reset();
        current_datetime = self.get_current_datetime();
        asup_id_last4chars = "{:04d}".format(self.next_id);
        asup_id_16chars = "{}{}".format(current_datetime.strftime(self.format_with_mins),
                asup_id_last4chars);
        self.next_id = self.next_id + 1;
        return asup_id_last4chars, asup_id_16chars, current_datetime.strftime(self.format_with_secs);
