<div align="center">
  <img src="https://img.shields.io/badge/JARVIS-AGI-red?style=for-the-badge&logo=huggingface" alt="Jarvis AGI Badge">

  <p>
    <a href="https://github.com/SreejanPersonal/JARVIS-AGI/stargazers">
      <img alt="GitHub stars" src="https://img.shields.io/github/stars/SreejanPersonal/JARVIS-AGI?style=social">
    </a>
    <a href="https://github.com/SreejanPersonal/JARVIS-AGI/network/members">
      <img alt="GitHub forks" src="https://img.shields.io/github/forks/SreejanPersonal/JARVIS-AGI?style=social">
    </a>
    <a href="https://github.com/SreejanPersonal/JARVIS-AGI/issues">
      <img alt="GitHub issues" src="https://img.shields.io/github/issues/SreejanPersonal/JARVIS-AGI?style=social">
    </a>
  </p>
</div>

<div align="center">
  <!-- Replace `#` with your actual links -->
  <a href="https://youtube.com/@devsdocode"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
  <a href="https://t.me/devsdocode"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  <a href="https://www.instagram.com/sree.shades_/"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/developer-sreejan/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://buymeacoffee.com/devsdocode"><img alt="Buy Me A Coffee" src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black"></a>
</div>

# JARVIS AGI

Jarvis is an AI Python voice assistant designed to streamline daily tasks and enhance user productivity. Named after the iconic AI assistant from popular culture, Jarvis is built with cutting-edge natural language processing capabilities, allowing users to interact with it through voice commands. Whether it's checking the weather, setting reminders, managing calendars, or searching the web, Jarvis is equipped to handle a wide range of tasks efficiently and effectively. With its intuitive interface and robust functionality, Jarvis aims to revolutionize the way users engage with technology, making everyday tasks simpler and more convenient.

## Devs Do Code

Made With 💓 By - Sree ( Devs Do Code )
- YouTube Channel: [Devs Do Code](https://www.youtube.com/@devsdocode)

For any questions or concerns, reach out to us via our social media handles.
Our top choice for contact is Telegram: [Devs Do Code Telegram](https://t.me/devsdocode)
You can also find us on other platforms listed above. We're here to help!

- YouTube Channel: [Devs Do Code](https://www.youtube.com/@DevsDoCode)
- Telegram Group: [Devs Do Code Telegram](https://t.me/devsdocode)
- Discord Server: [Devs Do Code Discord](https://discord.gg/ehwfVtsAts)
- Instagram:
  - Personal: [Sree](https://www.instagram.com/sree.shades_/)
  - Channel: [Devs Do Code](https://www.instagram.com/devsdocode_/)

---

Dive into the world of coding with Devs Do Code - where passion meets programming!
Make sure to hit that Subscribe button to stay tuned for exciting content!

Pro Tip: For optimal performance and a seamless experience, we recommend using
the default library versions demonstrated in this demo. Your coding journey just
got even better! Happy coding!

---

Sure, here's how you can integrate the installation steps for Vosk speech recognition models into your README:


## Installation

To run this project locally, follow these steps:

1. Download the Project from Youtube Description

2. Navigate to the project directory.

```bash
cd <your-main-project-directory>
```

3. Install the required dependencies using `requirements.txt`.

```bash
pip install -r requirements.txt
```


4. `(Optional)` Install Vosk Speech Recognition Models:
   
   Vosk provides pre-trained models for various languages. To install the models for your desired language, follow these steps:

   - Go to the Vosk GitHub repository releases page: [Vosk GitHub Releases](https://github.com/alphacep/vosk-api/releases)
   - Download the model folder for your language. For example, if you want English models, download the folder named `vosk-model-en-us-aspire-0.2`.
   - Extract the contents of the folder into a directory named `ASSETS` in your project directory.
   - Ensure that the extracted model folder is directly under the `ASSETS` directory, without any additional nesting.
   - Now, you should have a structure like this: `<your-main-project-directory>/ASSETS/vosk-model-en-us-aspire-0.2`.
   - Modify the `main.py` or any relevant script to point to the model directory. For example:
     ```python
     from ENGINE.STT.vosk_recog import speech_to_text

     for speech in speech_to_text(model_path="ASSETS/Vosk/vosk-model-small-en-us-0.15"):
        if speech != "":
            print("Human >>", speech)
      ```

5. Run the `main.py` file.

```bash
python main.py
```

Now you're all set to explore the Devs Do Code's project! Enjoy coding!

<div align="center">
  <!-- Replace `#` with your actual links -->
  <a href="https://youtube.com/@devsdocode"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
  <a href="https://t.me/devsdocode"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  <a href="https://www.instagram.com/sree.shades_/"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/developer-sreejan/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://buymeacoffee.com/devsdocode"><img alt="Buy Me A Coffee" src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black"></a>
</div>