from pathlib import Path 
from time import sleep

from watchdog.observers import Observer

from event_handler import EventHandler

if __name__ == '__main__':  #No está siendo importado el código
    watch_path = Path.home() / 'Downloads'
    destination_root = Path.home() / 'Downloads'
    event_handler = EventHandler(watch_path=watch_path, destination_root=destination_root)

    observer = Observer()
    observer.schedule(event_handler, f'{watch_path}', recursive=True)
    observer.start() #Observer watching for modifications
    
    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()