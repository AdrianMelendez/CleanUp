import shutil
from datetime import date
from pathlib import Path

from watchdog.events import FileSystemEventHandler

from extensions import extension_paths


def add_date_to_path(path : Path):
    #Adds date to the destination path and creates it if not.

    dated_path = path / f'{date.today().year}' / f'{date.today().month:02d}'
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path


def rename_file(source : Path, destination_path : Path):
    #Add number if file with the same name already exists.

    if Path(destination_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / f'{source.stem}_{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name


class EventHandler(FileSystemEventHandler):

    def __init__(self, watch_path : Path, destination_root : Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()


    def on_modified(self, event):
        for element in self.watch_path.iterdir():
            if element.is_file():
                if element.suffix.lower() in extension_paths:
                    destination_path = self.destination_root / extension_paths[element.suffix.lower()]
                else:
                    destination_path = self.destination_root / 'other/not known'
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=element, destination_path=destination_path)
                shutil.move(src=element, dst=destination_path)
