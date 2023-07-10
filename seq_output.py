import json
from promptTemplate import get_video_sequences

user_query = input("Enter the query: ")

output = get_video_sequences(video_input='', user_query=user_query)

print(f"output: {output}")

output_json = json.dumps(output)

print(f"output_json: {output_json}")

# Formatted json output
print(json.dumps(output, indent=4, sort_keys=True))