import requests
import base64
from typing import Tuple, Optional
import os
from dotenv import load_dotenv; load_dotenv() # Load environment variables from .env file

def generate(prompt: str, seed: int=1800647681, width: int=1024, height: int=576, steps: int=4, enhance: bool=True, safety_filter: bool=True, image_path: str="ASSETS/image.jpg") -> Tuple[bool, Optional[str]]:
    """
    Generates an image based on the given parameters and saves it to a file.

    Parameters:
    - prompt (str): Description of the image to generate.
    - seed (int): Seed for the image generation process.
    - width (int): Width of the generated image.
    - height (int): Height of the generated image.
    - steps (int): Number of steps for the image generation process. More the Steps More Clear and Realistic Image 
    - enhance (bool): Whether to enhance the image quality.
    - safety_filter (bool): Whether to apply a safety filter to the image.

    - For Square Image Size: 768x768
    - For Portrait Image Size: 1024x576
    - For Landscape Image Size: 576x1024

    Returns:
    - Tuple[bool, Optional[str]]: A tuple containing a boolean indicating the success of the API call,
      and an optional string with the file path where the image is saved if successful.
    """

    # Define the URL and headers for the API call
    url = "https://turbo.decohere.ai/generate/turbo"
    headers = {
        "Authorization": f"Bearer {os.environ.get('DECOHERE_AI')}",
    }

    # Define the payload for the POST request
    payload = {
        "prompt": prompt,
        "seed": seed,
        "width": width,
        "height": height, 
        "steps": steps,
        "enhance": enhance,
        "safety_filter": safety_filter,
    }

    # Make the POST request to the API
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code
    if response.status_code == 200:
        # Extract base64 encoded image data
        base64_image_data = response.json().get('image', '')
        # Decode base64 encoded image data to bytes
        image_bytes = base64.b64decode(base64_image_data)
        # Write the bytes to a file as an image
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        return True, image_path
    else:
        print(f"API call failed with status code {response.status_code}")
        return False, response.text
    
# Example usage:
if __name__ == "__main__":
    # prompt = "Picture an alien landscape, with strange, otherworldly plants and a sky filled with unfamiliar constellations. The scene is shot in a cinematic style, with the alien flora and starry sky providing a surreal backdrop. The image is taken with a high-resolution camera, capturing the intricate details of the alien plants and the twinkling stars. The lighting is a mix of the soft, alien sunlight and the glow from the stars. The final image is a hyper-realistic, ultra-detailed snapshot of this extraterrestrial concept art. –ar 16:9 –v 5.2 –style raw "

    # prompt = "ultra high-definition photo of a Japanese Instagram influencer"

    # prompt = "Envision a futuristic cityscape, where towering skyscrapers are interwoven with advanced technology. The scene is shot in a cinematic style, with the city’s neon lights reflecting off the sleek, metallic buildings. The image is taken with a high-resolution camera, capturing the intricate details of the futuristic architecture and the glowing city lights. The lighting is a mix of artificial neon lights and the natural light of the setting sun. The final image is a hyper-realistic, ultra-detailed depiction of this sci-fi concept art"

    # prompt = "Imagine a fantasy landscape, with towering castles and mythical creatures. The scene is shot in a cinematic style, with the majestic castles and fantastical creatures providing a magical backdrop. The image is taken with a high-resolution camera, capturing the intricate details of the stone castles and the mythical creatures. The lighting is a mix of the soft, natural light of dusk and the glow from the castle’s many torches. The final image is a hyper-realistic, ultra-detailed snapshot of this fantasy concept art"

    # prompt = "Imagine a young woman standing outdoors in a sunlit garden. She has long, wavy chestnut hair that cascades down her back. Her eyes are a mesmerizing shade of deep green, reflecting the surrounding nature. Her skin is flawless, with a natural glow, and she wears a soft, peach-colored sundress that flutters gently in the breeze. The garden is filled with vibrant flowers—roses, daisies, and lavender. Sunlight filters through the leaves, creating dappled patterns on the ground. Birds chirp happily in the background, and a gentle stream flows nearby. The girl’s expression is serene and content. She gazes into the distance, lost in thought, with a hint of a smile playing on her lips. Her posture is graceful, and she holds a delicate wildflower in one hand. The overall atmosphere is dreamy and romantic. The warm sunlight bathes everything in a soft glow, and the air smells of blooming flowers. It’s a moment frozen in time—a tranquil oasis of beauty and peace. Feel free to adjust or add any specific details to make the image even more enchanting"

    # prompt = "Imagine a cutting-edge quantum mechanics laboratory. The room is dimly lit, with banks of computers lining the walls. In the center, a large apparatus hums softly—a complex entanglement experiment. A laser beam splits into two paths, creating interference patterns on a distant screen. The air crackles with anticipation as researchers adjust delicate mirrors and detectors. Describe the scene, capturing the tension and excitement of probing the quantum realm."

    # prompt = "Deep within a crumbling stone tower lies the Ancient Library of Arcane Lore. Dusty tomes line the shelves, their leather covers embossed with faded symbols. A lone scholar, candlelight flickering, pores over a scroll containing forgotten spells. Describe the library’s scent—aged parchment and dried herbs. What secrets lie within those yellowed pages? And what consequences might unravel when a forbidden incantation is spoken?"

    # prompt = "Beneath the waves, a coral amphitheater hosts a magical event. Mermaids with iridescent tails gather—an orchestra of sea creatures. Their instruments include conch shells, seaweed harps, and dolphin whistles. The audience, a mix of fish and curious humans, sits on luminescent rocks. The conductor raises a trident, and the music begins—a haunting melody that resonates through the water. Describe the colors, the harmonies, and the sense of wonder."

    prompt = "Picture a massive steampunk airship sailing through the skies. Its brass hull gleams in the sunlight, adorned with gears, pipes, and ornate rivets. The crew—mechanics, sky pirates, and explorers—hustle about. The captain stands on the bridge, one hand on the wheel, scanning the horizon for hidden islands or rival vessels. The engines hiss and clank, propelling the ship forward. Write a vivid scene aboard this fantastical vessel."

    prompt = "The neon-lit streets of Neo-Tokyo stretch out before you. Hovercars whiz past, leaving trails of light. Holographic billboards advertise cybernetic enhancements and virtual reality experiences. On a rooftop, a lone hacker in a trench coat plugs into the city’s mainframe, seeking hidden truths. Capture the gritty atmosphere—the rain-slicked pavement, the distant hum of machinery, and the flickering holograms."

    prompt = "Tucked away on a cobblestone street, the “ChronoTea” shop defies time itself. The bell jingles as you enter, and the aroma of exotic teas envelops you. The walls are adorned with antique clocks, each showing a different era. The barista, a mysterious figure with mismatched eyes, offers you a cup of “Eternal Jasmine.” As you sip, memories from your past and glimpses of your future swirl together. Describe the cozy nooks, the ticking clocks, and the taste of eternity."

    prompt = "Deep within the Whispering Woods lies a sacred glade. Ancient oaks form a protective circle, their leaves shimmering with magic. At midnight, druids gather—their robes embroidered with moon phases. They chant in an ancient language, invoking the spirits of earth, air, fire, and water. In the center, a silver cauldron steams, filled with herbs and moonlit dew. Describe the energy—the crackling ley lines, the rustling leaves, and the sense of balance restored."

    prompt = "In the heart of a cosmic nebula, an art gallery floats—a celestial masterpiece. Each exhibit is a swirling galaxy, its colors shifting with emotion. Visitors wear shimmering spacesuits, their helmets reflecting constellations. The curator, an android with silver tendrils, explains the meaning behind a star-cluster sculpture. Describe the ethereal beauty—the sound of solar winds, the taste of stardust, and the way the art seems to sing across light-years."

    prompt = "Ravenswood Manor stands atop a fog-shrouded hill. Its turrets and gables loom like silent sentinels. Inside, candelabras flicker, casting elongated shadows on velvet wallpaper. A ghostly pianist plays a mournful melody in the ballroom, while a spectral lady in white drifts down the grand staircase. Describe the chill in the air, the scent of old roses, and the secrets hidden in the dusty library."



    success, file_path = generate(prompt)
    if success: print(f"Image saved at {file_path}")
    else: print("Failed to generate the image.")
