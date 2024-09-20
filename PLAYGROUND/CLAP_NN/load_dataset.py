import os
import torch
import torchaudio
from torch.utils.data import Dataset
from torchvision.transforms import Resize
import torchaudio.transforms as T

def get_wav_files(directory: str) -> list:
    """
    Get a list of WAV file paths in the given directory.

    Args:
        directory (str): Path to the directory containing WAV files.

    Returns:
        list: List of WAV file paths.
    """
    return [
        os.path.join(directory, filename)
        for filename in os.listdir(directory)
        if filename.endswith(".wav")
    ]

class AudioDataset(Dataset):
    """
    Dataset for audio classification.
    """
    def __init__(self, noise_dir: str, clap_dir: str) -> None:
        """
        Initializes the AudioDataset.

        Args:
            noise_dir (str): Path to the directory containing noise audio files.
            clap_dir (str): Path to the directory containing clap audio files.
        """
        noise_files = get_wav_files(noise_dir)
        clap_files = get_wav_files(clap_dir)

        self.noise_dir = noise_dir
        self.clap_dir = clap_dir
        self.file_list = noise_files + clap_files
        self.labels = [0] * len(os.listdir(noise_dir)) + [1] * len(os.listdir(clap_dir))

    def __len__(self) -> int:
        """
        Returns the total number of samples in the dataset.
        """
        return len(self.file_list)

    def __getitem__(self, idx: int, n_mels: int = 64, n_fft: int = 400, hop_length: int = 200) -> tuple:
        """
        Gets the item at the specified index.

        Args:
            idx (int): Index of the sample to retrieve.
            n_mels (int, optional): Number of mel frequency channels. Defaults to 64.
            n_fft (int, optional): Size of FFT. Defaults to 400.
            hop_length (int, optional): Hop length of the STFT. Defaults to 200.

        Returns:
            tuple: A tuple containing the spectrogram and the label.
        """
        waveform, sample_rate = torchaudio.load(self.file_list[idx])
        spec = T.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=n_fft,
            win_length=n_fft,
            hop_length=hop_length,
            n_mels=n_mels,
        )(waveform)
        spec = Resize((256, 256))(spec)
        spec = (spec - spec.mean()) / spec.std()  # normalize the spectrogram
        label = self.labels[idx]
        return spec, torch.tensor(label)
