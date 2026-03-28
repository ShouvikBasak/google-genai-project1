# google-genai-project1
Google GenAI Academy APAC 2026 - Project 1 (Track 1)

## Problem Statement
Build and deploy a single AI agent using ADK and Gemini that is hosted on Cloud Run and performs one clearly defined task.
The agent must be callable via an HTTP endpoint and return a valid response for a given input.

This is a mini project focused on agent structure and deployment, not complex logic.

## What You Must Build
You must build one AI agent that:

- Is implemented using ADK
- Uses a Gemini model for inference
- Performs one simple capability, such as:
  - Text summarization
  - Question answering over a prompt
  - Classification of input text
  - Routing a request to a fixed response logic
- Accepts an input request and returns a response
- We will take the cloud run link as submission, along with the repository if applicable.

## Steps followed

- Created "Cohort1 Project" and linked to billing account
- Enabled required APIs: `gcloud services enable aiplatform.googleapis.com`
- `mkdir med_agent` & `cd med_agent`
- Create python virtual environment: `uv venv --python 3.12`
- Activate virtual environment: `source .venv/bin/activate`
- Install Google ADK: `uv pip install google-adk` (inside the virtual env)
- Create an agent: `adk create med_assistant`. 
    - model: gemini-2.5-flash for root agent
    - Vertex AI
    - Google Cloud project ID [cohort1-project-31032026]
    - Google Cloud region [us-central1]
- Folder structure:
    - Root of the project is `google-genai-project1` which is the git repo
    - Folder `med_agent` is created within that which holds all installations and python venv
    - Inside `med_agent` an agent is created within directory `med_assistant` within which all agent specific files are created
        - .env
        - __initi.py__
        - agent.py
        - _to be added_
- Test the basic agent: `adk run med_assistant` WORKS!!
- Test the agent on web: `adk web --allow_origins="*"` WORKS!!



## Errors & Resolutions
- `google.auth.exceptions.RefreshError: Unexpected response from metadata server: service account info is missing 'email' field.`.  
    To resolve this error the Cloud Shell need to be reauthorized with the google cloud login id. Close the Terminal and open Terminal again from the cloud console. 

- `adk web` opens terminal but agent does not respond. Error in console:
    ```
    INFO:     127.0.0.1:33088 - "POST /run_sse HTTP/1.1" 403 Forbidden
    INFO:     127.0.0.1:33088 - "GET /debug/trace/session/ HTTP/1.1" 307 Temporary Redirect
    INFO:     127.0.0.1:33088 - "GET /debug/trace/session HTTP/1.1" 404 Not Found
    ```
    To resolve, run with `adk web --allow_origins="*"`
    



