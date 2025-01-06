import redis
import time
import random
import concurrent.futures

secret_key = 'xxx'
azure_redis_host = 'xxx.redis.cache.windows.net'

# Lua script to increment the value of a key 
# up to an upper limit, then reset to 0
lua_script = """
local function increment_and_reset(key)
    local current_value = redis.call("INCR", key)
    if current_value > 99 then
        redis.call("SET", key, 0)
        return 0
    end
    return current_value
end
return increment_and_reset(KEYS[1])
"""

def increment_in_range(r, thread_id, key):
    for x in range(55):
        result = r.eval(lua_script, 1, key);
        print(f"{thread_id}-{x}: result is {result} for key {key}");
        time.sleep(random.randrange(500)/1000)
    return True;

def main():
    r = redis.Redis(host = azure_redis_host, password = secret_key);
    
    print("Now deleting all keys & values");
    for key in r.scan_iter():
        r.delete(key);
        print(f"{key} deleted");

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for x in range(8):
            val = "0{:04d}".format(x);
            futures.append(executor.submit(increment_in_range, r, x, 'my_key'))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    print("Now printing all keys & values");
    for key in r.scan_iter():
        val = r.get(key);
        print(f"{key} -> {val}");

if __name__ == "__main__":
    main()






