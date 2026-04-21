import jsonschema
import json
from jsonschema import validate


# converting text into JSON
text = """Satyam 23 Python ADIT
Mukesh 25 MERN GCET
Anish 21 UIUX BVM"""

data = []
fields = ["name", "age", "tech", "college"]

for line in text.splitlines():
    desc = list(line.strip().split(None, 3))
    record = dict(zip(fields, desc))
    record["age"] = int(record["age"])

    data.append(record)

with open("test.json", "w") as out_file:
    json.dump(data, out_file, indent=4)


# validating a json with jsonschema validator
schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "tech": {"type": "string"},
            "college": {"type": "string"},
        },
        "required": ["name", "age", "tech", "college"]
    }
}

with open("test.json", "r") as in_file:
    data1 = json.load(in_file)
try:
    validate(instance=data1, schema=schema)
    print("Valid JSON")
except jsonschema.exceptions.ValidationError as e:
    print(f"Invalid Json: {e}")