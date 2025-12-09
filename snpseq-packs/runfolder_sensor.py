# language: python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# from flytekit.remote import FlyteRemote
# from test_automation_engine_stackstorm.arteria.arteria.models.config import Config
from run_checkqc import fetch_workflow 

# Flyte remote configuration
# flyte_remote = FlyteRemote(config_file="config.yaml")

class FileCreatedHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        # Trigger Flyte workflow
        print(f"New file detected: {event.src_path}")
        url = "http://localhost:9992/qc/200624_A00834_0183_BHMTFYTINY?useClosestReadLength&downgrade=ReadsPerSampleHandler"
        res= fetch_workflow(url=url)  # adjust input as needed
        print(res)

if __name__ == "__main__":
    monitored_directories = ["/home/nelnk861/Documents/code/arteria_lab/flyte/test_automation_engine_stackstorm/test_data"]
    for path_to_watch in monitored_directories:
        # path_to_watch = "/path/to/directory"
        event_handler = FileCreatedHandler()
        observer = Observer()
        observer.schedule(event_handler, path=f"{path_to_watch}", recursive=True)
        observer.start()
        print(f"Monitoring {path_to_watch} for new files...")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()