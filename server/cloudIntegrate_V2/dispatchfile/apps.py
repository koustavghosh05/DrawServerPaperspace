from django.apps import AppConfig

# from .task import start_watcher
import threading
import sys

class DispatchfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dispatchfile'

    def ready(self):
        # Only start the watcher when the Django server is running
        if 'runserver' in sys.argv:
            # Run the watcher in a separate thread to not block the main thread
            from .task import start_watcher
            watcher_thread = threading.Thread(target=start_watcher, daemon=True)
            watcher_thread.start()


# YourAppConfig
# Can be deleted later
# class dispatchfileAppConfig(AppConfig):
#     name = 'dispatchfile'

#     def ready(self):
#         # Run the watcher in a separate thread to not block the main thread
#         from .task import start_watcher
#         watcher_thread = threading.Thread(target=start_watcher, daemon=True)
#         watcher_thread.start()
