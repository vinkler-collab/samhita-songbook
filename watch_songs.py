import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SongHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.pro'):
            self.run_generator()

    def on_created(self, event):
        if event.src_path.endswith('.pro'):
            self.run_generator()

    def on_moved(self, event):
        if event.dest_path.endswith('.pro'):
            self.run_generator()

    def run_generator(self):
        print("Zjištěna změna v 'songs/'. Aktualizuji songs.json...")
        subprocess.run(["python3", "generate_json.py"])

if __name__ == "__main__":
    path = "songs/"  # Sledujeme pouze ostrou složku
    event_handler = SongHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print(f"Sleduji složku {path}... (Ukončíš pomocí Ctrl+C)")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()