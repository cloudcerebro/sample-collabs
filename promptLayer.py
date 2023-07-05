import json
import sys
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain import LLMChain
import promptlayer
from langchain.llms import PromptLayerOpenAIChat

sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

print("Executing promptLayer.py")

promptlayer.api_key = os.environ.get("PROMPTLAYER_API_KEY")
llm = PromptLayerOpenAIChat(pl_tags=["video-platform", "v2"], model_name="gpt-4") # type: ignore


prompt_template_obj = None

prompt = None
try:
    prompt = promptlayer.prompts.get("Generate_JSON", langchain=True)
except Exception as error:
    print("Prompt template not found.")
    print(f"Error: ", error)
    exit(1)

if prompt is None:
    print("Prompt template not found.")
    exit(1)

llm_chain = LLMChain(prompt=prompt, llm=llm)
output = llm_chain.run(video_input='', user_query="Generate a video of duration 9000 frames in 30 fps with width: 1080 and height: 1920. The video is about 50 facts about cats.")
print(f"output: {output}")
# Convert output string to JSON
output_json = json.loads(output)
print(f"output_json: {output_json['videoInput']}")

# Convert JSON to dict
output_dict = dict(output_json)
print(f"output_dict: {output_dict}")
print(f"output_dict: {output_dict['videoInput']}")


