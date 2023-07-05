import json
import sys
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.llms import OpenAIChat
from langchain import PromptTemplate
from langchain.llms import PromptLayerOpenAIChat
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic

sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

print("Executing promptTemplate.py")

llm = OpenAIChat(model_name="gpt-4") # type: ignore

template = """
You are a powerful AI Assistant which is well trained on many videos.

The input may contain one of the following: 
a) video_input: JSON which contains the current JSON configuration.
b) user_query: Question by the user using which a new JSON configuration has to be generated.

The template for the new JSON to be created is as follows:

{{
    "videoInput": {{
      "backgroundColor": "#000000", // Any color that suits the project
      "durationInFrames": 300,  // Got from the user_query input. This is project duration
      "fps": 30, // Got from the user_query input
      "width": 1920, // Got from the user_query input
      "height": 1080, // Got from the user_query input
      "sequences": [ // A sequence is a kind of slide in a video. Multiple sequences can be generated.
        {{
          "sequenceNo": 1, // Sequential number
          "from": 0, // Based on the previous sequence
          "durationInFrames": 300, // Split the project duration among the sequences
          "transition": {{
            "type": "in" // Can be 'in' or 'out'
          }},
          "structure": {{
            "backgroundColor": "#000000", // Any color that suits the project
            "useTemplate": false,
            "template": null,
            "generatedText": "", // The text that will be generated for this sequence
            "components": []
          }}
        }}
      ]
    }}
  }}

Steps:
1. Generate the text for each sequence based on the user_input query.
2. Form JSON based on the above template substituting the generated text for each sequence in the formed JSON.

durationInFrames, fps, width and height are got from the user_query input.
The durationInFrames of each sequence can be different from the other.

video_input:
{video_input}

user_query:
{user_query}


Result:

Example Input:
user_query: Generate a video of duration 900 frames in 30 fps with width: 1080 and height: 1920. The video is about five facts about cats.
Example output:
{{
    "videoInput": {{
      "backgroundColor": "#000000",
      "durationInFrames": 900,
      "fps": 30,
      "width": 1080,
      "height": 1920,
      "sequences": [
        {{
          "sequenceNo": 1,
          "from": 0,
          "durationInFrames": 300,
          "transition": {{
            "type": "in"
          }},
          "structure": {{
            "backgroundColor": "#000000",
            "useTemplate": false,
            "template": null,
            "generatedText": "Cat is a friendly animal",
            "components": []
          }}
        }},
        {{
          "sequenceNo": 2,
          "from": 300,
          "durationInFrames": 300,
          "transition": {{
            "type": "in"
          }},
          "structure": {{
            "backgroundColor": "#000000",
            "useTemplate": false,
            "template": null,
            "generatedText": "Cat can be a pet animal",
            "components": []
          }}
        }},
        {{
          "sequenceNo": 3,
          "from": 600,
          "durationInFrames": 300,
          "transition": {{
            "type": "in"
          }},
          "structure": {{
            "backgroundColor": "#000000",
            "useTemplate": false,
            "template": null,
            "generatedText": "Cat has a soft body",
            "components": []
          }}
        }}
      ]
    }}
  }}
""" # type: ignore

prompt_template = PromptTemplate(input_variables=["user_query", "video_input"], template=template)

# formatted_prompt = prompt_template.format(user_input="Generate a video of duration 900 frames in 30 fps with width: 1080 and height: 1920. The video is about five facts about cats.", video_input="")

llm_chain = LLMChain(prompt=prompt_template, llm=llm)
output = llm_chain.run(video_input='', user_query="Generate a video of duration 900 frames in 30 fps with width: 1080 and height: 1920. The video is about five facts about cats.")
print(f"output: {output}")
# Convert output string to JSON
output_json = json.loads(output)
print(f"output_json: {output_json['videoInput']}")

# Convert JSON to dict
output_dict = dict(output_json)
print(f"output_dict: {output_dict}")
print(f"output_dict: {output_dict['videoInput']}")



