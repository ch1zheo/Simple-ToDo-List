# Simple ToDo List

Desktop notes application built with PyQt6, featuring a dark theme and interface language switching (Russian / English). Notes are stored in a local SQLite database - creating, editing, and deleting are written straight to the database file, with no cloud or syncing involved.

# How it works

1. **Launch.** On startup, the application connects to the `notes.db` file (created automatically next to `database.py` if it doesn't exist yet) and opens the main window with the list of notes.

2. **Notes list.** Notes are displayed as cards - a title and a date stamp. If a note has never been edited, it shows "Created: ..."; as soon as it's edited, the stamp changes to "Updated: ..." with the new time. If a note has a reminder enabled, the time of its next trigger is shown alongside it.

3. **Creating.** The "New note" button opens a dialog with title and content fields. An empty title isn't saved - a warning is shown instead.

4. **Viewing.** Double-clicking a note in the list opens a read-only window - the full text and the creation/update dates, with no risk of accidentally erasing something.

5. **Editing.** The "Edit" button opens the same dialog as creation, but pre-filled. Saving updates the record in the database along with the update date.

6. **Deleting.** The "Delete" button asks for confirmation (the action is irreversible) and removes the record from the database.

7. **Notifications.** When creating or editing a note, you can enable a reminder, set an exact date and time, and choose a repeat - no repeat, daily, weekly, or monthly. The application checks for due reminders every 30 seconds and shows a system notification through the tray. If a repeat is set, the time is automatically moved to the next trigger; if there's no repeat, the reminder is cleared after the first notification.

8. **Language switching.** The switcher in the top-right corner changes the entire interface on the fly - button labels, dialog titles, and the date format (`dd.mm.yyyy` for Russian, `yyyy-mm-dd` for English) - without restarting the application.

9. **Minimize to tray.** Closing the window (the X button, Alt+F4) doesn't quit the application - it minimizes it to the tray with a "Simple ToDo List minimized to tray!" notification, and the background reminder check keeps running. Clicking the tray icon restores the window; right-clicking opens an "Open" / "Exit" menu - only "Exit" actually closes the application.

# Structure

Simple ToDo List/

├── main.py            # Entry point: creates the application, applies the dark theme, shows the window

├── main_window.py       # Main window: notes list, action buttons, language switcher

├── note_dialog.py         # Create/edit dialog (with reminder fields) and the note view dialog

├── notifications.py         # Checking due reminders and system notifications through the tray

├── resources.py               # Path to the app icon (works when running from a packaged exe too)

├── logo.ico                     # Window and tray icon

├── database.py             # All SQLite work: table creation, CRUD operations, reminders

├── i18n.py                  # Interface texts in Russian and English

├── styles.py                 # Dark theme styling (QSS)

├── requirements.txt            # Python dependency list

├── LICENSE                       # MIT license text

└── notes.db                     # Created automatically after the first run

# Installation (Windows)

1. Install the exe file.

2. Run the program.

# Important note

If you find a bug, be sure to let the author know!

MIT License - please credit the author.

Author - Ch1zheo
