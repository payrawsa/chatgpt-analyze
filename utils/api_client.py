import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, **kwargs):
        """Perform a GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Ensure no double slashes
        return requests.get(url, **kwargs)

    def post(self, endpoint, **kwargs):
        """Perform a POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Ensure no double slashes
        return requests.post(url, **kwargs)

    def ask_chatgpt(self, system_prompt, user_content):
        """
        Send a request to the 'ask_chatgpt' endpoint.
        """
        endpoint = "ask_chatgpt/"
        headers = {"Content-Type": "application/json"}
        payload = {
            "system": system_prompt,
            "user": user_content
        }
        
        try:
            response = self.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def transcribe_audio(self, audio_file_path):
        """
        Send a request to the 'transcribe_audio' endpoint.
        """
        endpoint = "transcribe_audio/"
        files = {
            "audio_file": open(audio_file_path, "rb")
        }
        data = {
            "system": "answer the question as best as you can."
        }
        
        try:
            response = self.post(endpoint, data=data, files=files)
            response.raise_for_status()
            data = response.json()
            return data.get("steps")
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        finally:
            files["audio_file"].close()