from time import sleep
from libs import watcher

_run = False
watcherObject = watcher.Watcher()
watcherObject.create_currency_objects()


while _run is False:
    watcherObject.update_top_currencies()
    sleep(300)
