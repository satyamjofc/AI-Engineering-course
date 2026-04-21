import json

# converting text into dict
# text = "id=1, name= Satyam"
# data = dict(item.split("=") for item in text.split(","))
# print(data)

# reading a file
with open("example.json", "r") as file:
    example = json.load(file)
# value = example["user"]
# print(value["name"])


# converting Dict to JSON
# result = json.dumps(example, indent=4)
# print(result[a])


# writing a text file into prompt_template
with open("example.json", "r") as file:
    example2 = file.read()
with open("prompt_template.txt", "w") as prompt:
    prompt.write(example2)