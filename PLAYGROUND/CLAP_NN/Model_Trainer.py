import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from load_dataset import AudioDataset 
from cnn_sound_model import AudioClassifier 
from typing import Tuple, List

class AudioClassifierTrainer:
    """
    Trainer class for the AudioClassifier model.
    """
    def __init__(self, noise_dir: str, clap_dir: str, device: torch.device) -> None:
        """
        Initializes the AudioClassifierTrainer.

        Args:
            noise_dir (str): Path to the directory containing noise audio files.
            clap_dir (str): Path to the directory containing clap audio files.
            device (torch.device): Device to use for training (CPU or CUDA).
        """
        self.device = device
        self.dataset = AudioDataset(noise_dir, clap_dir)
        self.train_dataloader, self.val_dataloader = self.prepare_dataloaders()
        self.model = AudioClassifier().to(self.device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-5, weight_decay=0.02)

    def prepare_dataloaders(self) -> Tuple[DataLoader, DataLoader]:
        """
        Prepares the training and validation dataloaders.

        Returns:
            Tuple[DataLoader, DataLoader]: Training and validation dataloaders.
        """
        train_size = int(0.95 * len(self.dataset))
        val_size = len(self.dataset) - train_size
        train_dataset, val_dataset = random_split(self.dataset, [train_size, val_size])
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        return train_loader, val_loader

    def train(self, num_epochs: int) -> None:
        """
        Trains the model for the specified number of epochs.

        Args:
            num_epochs (int): Number of epochs to train.
        """
        for epoch in range(num_epochs):
            train_loss, train_accuracy = self.run_epoch(self.train_dataloader, training=True)
            val_loss, val_accuracy = self.run_epoch(self.val_dataloader, training=False)
            print(f"Epoch {epoch + 1}/{num_epochs}, Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.4f}")
        self.save_model("Clap_Detect_Model.pth")

    def run_epoch(self, dataloader: DataLoader, training: bool) -> Tuple[float, float]:
        """
        Runs one epoch of training or validation.

        Args:
            dataloader (DataLoader): Data loader for the current epoch.
            training (bool): Flag indicating training or validation mode.

        Returns:
            Tuple[float, float]: Average loss and accuracy for the epoch.
        """
        if training:
            self.model.train()
        else:
            self.model.eval()

        epoch_loss = 0
        correct_predictions = 0
        total_predictions = 0

        with torch.set_grad_enabled(training):
            for inputs, labels in dataloader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)

                if training:
                    self.optimizer.zero_grad()
                    loss.backward()
                    self.optimizer.step()

                epoch_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                total_predictions += labels.size(0)
                correct_predictions += (predicted == labels).sum().item()

        avg_loss = epoch_loss / len(dataloader)
        accuracy = correct_predictions / total_predictions
        return avg_loss, accuracy

    def save_model(self, path: str) -> None:
        """
        Saves the trained model to a file.

        Args:
            path (str): Path to save the model.
        """
        torch.save(self.model.state_dict(), path)

if __name__ == "__main__":
    torch.manual_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    trainer = AudioClassifierTrainer("PLAYGROUND/CLAP_NN/DATASETS/noise2", "PLAYGROUND/CLAP_NN/DATASETS/claps", device)
    trainer.train(num_epochs=5)
