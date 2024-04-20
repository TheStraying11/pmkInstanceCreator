# pmkInstanceCreator
GUI/CLI tool to automatically create a new instance of the PalWorld Modding Kit, as per the instructions on the pwmodding wiki

Usage:
  - download the executable file for your operating system from the releases tab
  - CLI:
    - `pmkInstanceCreator --console <wwiseIntegrationPath> <wwiseSDKPath> <palworldModdingKitPath> <newInstancePath>`
  - GUI:
    - launch the executable
    - select the folders using the browse dialog buttons, or by typing the path
    - click create instance
    - pop-up dialogs will appear informing you of the progress of the instance creation, or, in the case of an error, what you have done wrong
    - If you see a pop-up with the title: "Unhandled Exception", make a bug report in the issues tab, with exactly what you did, and the error shown in the popup (you can screenshot it)

Run from source:
  - [Install python >= 3.11.3](https://www.python.org/downloads/)
  - [Install kivy >= 2.2.1](https://kivy.org/doc/stable/gettingstarted/installation.html)
  - clone the repository
  - run `python main.py`

Build from source:
  - follow the [instructions](https://kivy.org/doc/stable/guide/packaging-windows.html) for building a kivy app with pyinstaller 
