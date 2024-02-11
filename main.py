import sys, os
import common_vars as cv
from PyQt5.QtWidgets import QApplication
from pc_components.desktop.desktop_main import MainDesktop


def delete_all_files_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted {file_path}")
            elif os.path.isdir(file_path):
                print(f"Skipping directory: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def main():
    delete_all_files_in_folder(cv.notes_path)
    app = QApplication(sys.argv)
    window = MainDesktop()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
