from butter import inotify

output = inotify.inotify_add_watch(event_notifier, "/usr/sbin", IN_ALL_EVENTS)
