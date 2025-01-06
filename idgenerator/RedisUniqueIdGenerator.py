import redis
from datetime import datetime, timedelta, timezone

secret_key = 'xxx'
azure_redis_host = 'xxx.redis.cache.windows.net'


# Lua script to increment the value of a key 
# up to an upper limit, then reset to 1
lua_script = """
local function increment_and_reset(key)
    local current_value = redis.call("INCR", key)
    --if current_value > 10000 then
    --    current_value = 1
    --    redis.call("SET", key, current_value)
    --end
    return current_value - 1
end
return increment_and_reset(KEYS[1])
"""

class RedisUniqueIdGenerator:
    format_with_mins = "%Y%m%d%H%M";
    format_with_secs = "%Y%m%d%H%M%S";

    def get_current_datetime(self):
        return datetime.now();

    def __init__(self, ais_pod_id):
        self.ais_pod_id = ais_pod_id;
        self.r = redis.Redis(host = azure_redis_host, password = secret_key);
    
    def delete_all_contents(self):
        print("Now deleting all keys & values");
        for key in self.r.scan_iter():
            self.r.delete(key);
            print(f"{key} deleted");

    def increment_in_range(self, key):
        result = self.r.eval(lua_script, 1, key);
        formatted_result = "{:04d}".format(result);
        return formatted_result;

    def get_next_id(self):
        current_datetime = self.get_current_datetime();
        current_dt_with_mins = current_datetime.strftime(self.format_with_mins)
        next_id = self.increment_in_range(current_dt_with_mins);
        asup_id_16chars = "{}{}".format(current_dt_with_mins, next_id);
        return next_id, asup_id_16chars, current_datetime.strftime(self.format_with_secs);

            
