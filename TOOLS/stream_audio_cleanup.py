import os
import shutil

def delete_stream_audio_files(folder_path='ASSETS/STREAM_AUDIOS') -> None:
    """
    Deletes all files inside the ASSETS/STREAM_AUDIOS folder.

    This function is intended to be used to clean up temporary audio files
    stored in the STREAM_AUDIOS folder. It recursively deletes all files
    in the folder, leaving the folder structure intact.

    :return: None
    """
    folder_path = os.path.join(os.getcwd(), folder_path)
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except OSError as e:
                print(f"Error deleting file: {e.filename} - {e.strerror}.")
                continue
    else:
        print(f"Folder {folder_path} does not exist.")


delete_stream_audio_files()