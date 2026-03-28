import requests

# define a function to get exchange rate
def get_fx_rate(base: str, target: str):
        """
        Fetches the current exchange rate between two currencies.

        Args:
                base: The base currency (e.g., "SGD").
                target: The target currency (e.g., "JPY").

        Returns:
                The exchange rate information as a json response,
                or None if the rate could not be fetched.
        """
        base_url = "https://hexarate.paikama.co/api/rates/latest"
        api_url = f"{base_url}/{base}?target={target}"

        response = requests.get(api_url)
        if response.status_code == 200:
                return response.json()

# Note: Pay close attention to the descriptive text within the triple quotes ("""..."""). This is called a docstring. While it's good practice for human developers, for an AI Agent it is essential. The agent's underlying LLM reads the function name and this docstring to understand what the tool does, what its arguments (base and target in this case) mean, and when it should be used. A clear, descriptive docstring is the single most important factor for the agent to use your tool correctly.