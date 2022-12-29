
import pymemcache

mc = pymemcache.Client("localhost:11211")

mc.set('heatingUnit.0.target_temp_degc', 6)
mc.set('heatingUnit.1.target_temp_degc', 2)



