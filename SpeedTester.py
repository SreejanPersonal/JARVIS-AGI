from ENGINE.TTS.hearling import Async_HearlingAudioGenerator, HearlingAudioGenerator, Partial_Async_HearlingAudioGenerator
import time

async_generator = Async_HearlingAudioGenerator()
partial_async_generator = Partial_Async_HearlingAudioGenerator()
generator = HearlingAudioGenerator()


text = 'सूरज की किरणें धीरे-धीरे  पेड़ों के पत्तों के बीच से झाँक रही थीं'

# text = '''सूरज की किरणें धीरे-धीरे  पेड़ों के पत्तों के बीच से झाँक रही थीं। हवा में ताज़ी खुशबू तैर रही थी, जैसे ज़मीन से उठी हो।  पक्षियों के चहचहाने से सन्नाटा टूट गया था, और  जंगल जीवन के साथ गूंज उठा था।  एक छोटा सा खरगोश पेड़ के नीचे से निकला, अपनी छोटी सी नाक हवा में घुमाते हुए,  और कुछ ही पलों में  घने  पेड़ों में  गायब हो गया।'''

for i in range(5):
    start = time.time()
    async_generator.speak(text)
    print(f"\033[92m\nAsync Hearling Audio Generator response time: {time.time() - start:.2f} seconds\033[0m")

    start = time.time()
    partial_async_generator.speak(text)
    print(f"\033[94mPartial Async Bearling Audio Generator response time: {time.time() - start:.2f} seconds\033[0m")

    start = time.time()
    generator.speak(text)
    print(f"\033[93mHearling Audio Generator response time: {time.time() - start:.2f} seconds\033[0m")
