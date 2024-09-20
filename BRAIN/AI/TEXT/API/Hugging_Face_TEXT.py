import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate(
    prompt: str, 
    model: str = "microsoft/Phi-3-mini-4k-instruct", 
    system_prompt: str = "Keep your response short and concise.", 
    temperature: float = 0.9, 
    max_new_tokens: int = 512, 
    top_p: float = 0.95, 
    repetition_penalty: float = 1.0, 
    verbose: bool = False, 
    chat_template: str = "mistral"
) -> str:
    """
    Generate text based on the provided prompt using a specified model.

    Parameters:
        - prompt (str): The input text prompt to generate text from.
        - model (str): The name or path of the pre-trained language model to use for text generation available on Hugging Face.
                       Some Available Models:
                           - microsoft/Phi-3-mini-4k-instruct
                           - mistralai/Mistral-7B-Instruct-v0.2
                           - mistralai/Mixtral-8x7B-Instruct-v0.1
                           - meta-llama/Meta-Llama-3-8B
        - system_prompt (str): The system prompt to guide the generation process, encouraging short and concise responses.
        - temperature (float): Controls the randomness of the generated text. Higher values lead to more random output.
        - max_new_tokens (int): The maximum number of tokens to generate in the output text.
        - top_p (float): A nucleus sampling parameter. It controls the probability mass to sample from. 
                         Smaller values lead to more conservative sampling.
        - repetition_penalty (float): Penalty applied to the likelihood of tokens that are already present in the generated text.
        - verbose (bool): If True, the generated text will be printed; if False, it will only be returned.
                          stream (bool, optional): By default, text_generation returns the full generated text. 
                          Pass stream=True if you want a stream of tokens to be returned. 
                          Only available for models running with the text-generation-inference backend.

    Returns:
        str: The generated text based on the provided prompt and model.
    """

    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {os.environ.get('HUGGING_FACE_READ')}"}
    client = InferenceClient(api_url, headers=headers)

    if chat_template == "mistral":
        formatted_prompt = f"[INST] {system_prompt} [/INST][INST] {prompt} [/INST]"
    elif chat_template == "gemma":
        formatted_prompt = f"<bos><start_of_turn>system{system_prompt}<end_of_turn><start_of_turn>user{prompt}<end_of_turn><start_of_turn>model"
    elif chat_template == "helping ai":
        formatted_prompt = f"<|im_start|>system: {system_prompt}\n<|im_end|>\n<|im_start|>user: {prompt}\n<|im_end|>\n<|im_start|>assistant:"
    else:
        formatted_prompt = f"**Instructions**\n{system_prompt}\n\n **User**\n{prompt}\n\n**Assistant: **"

    try:
        response = ""
        for response_chunk in client.text_generation(
            formatted_prompt, 
            temperature=temperature, 
            max_new_tokens=max_new_tokens, 
            top_p=top_p, 
            repetition_penalty=repetition_penalty, 
            do_sample=True, 
            stream=True
        ):
            response += response_chunk
            if verbose:
                print(response_chunk, end="", flush=True)
    except:
        response = client.text_generation(
            formatted_prompt, 
            temperature=temperature, 
            max_new_tokens=max_new_tokens, 
            top_p=top_p, 
            repetition_penalty=repetition_penalty, 
            do_sample=True
        )

    # Clean the response from potential end-of-text tokens
    response = response.replace("<|end|>", "")
    response = response.replace("<|endoftext|>", "")
    response = response.replace("[END]", "")
    response = response.replace("<|eot_id|>", "")
    response = response.replace("</s>", "").strip()

    return response

# Example usage
if __name__ == "__main__":
    import time
    
    prompt = "Write 10 Lines on China"
    start = time.time()

    # response = generate(prompt, system_prompt="Be Helpful and Friendly", model="google/gemma-1.1-7b-it", temperature=0.7, chat_template="gemma", verbose=True)
    # response = generate(prompt, system_prompt="Be Helpful and Friendly", model="mistralai/Mistral-7B-Instruct-v0.2", temperature=0.7, chat_template="mistral", verbose=True)
    # response = generate(prompt, system_prompt="Be Helpful and Friendly", model="mistralai/Mistral-7B-Instruct-v0.3", temperature=0.7, chat_template="mistral", verbose=True)
    # response = generate(prompt, system_prompt="Be Helpful and Friendly", model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.7, chat_template="mistral", verbose=True)
    # response = generate(prompt, model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.7, chat_template="other", verbose=True)
    response = generate("I'm excited because I just got accepted into my dream school! I wanted to share the good news with someone.", model="OEvortex/HelpingAI-2B", temperature=0.7, chat_template="helping ai",  system_prompt="Your are Helping AI, an Emotional AI. You will always answer my questions in English and in Helping AI style.", verbose=True)
    
    print(f"\n\n\033[92m{time.time() - start:.2f} seconds\n\n\033[0m")
    # print(response)