import json
import os

class DocumentLoader:

    def load_from_text(self, text: str) -> dict:
        return{
            "content": self._clean_text(text),
            "source": "paste",
            "metadata": {}
        }
    
    def load_from_file(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")

        ext = file_path.split(".")[-1].lower()

        if ext == "txt":
            content = self._load_txt(file_path)

        elif ext == "json":
            content = self._load_json(file_path)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return {
            "content": self._clean_text(content),
            "source": "file",
            "metadata": {
                "file_name": os.path.basename(file_path),
                "file_type": ext,
                "size": os.path.getsize(file_path)
            }
        }
    
    def _load_txt(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_json(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)

    def _clean_text(self, text: str) -> str:
        return text.strip()