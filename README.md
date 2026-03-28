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

### Create the scaffolding for the project
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
- Test the agent on Development Web UI: `adk web --allow_origins="*"` WORKS!!

### Configure Cloud Run for Application Deployment
Use the `adk deploy cloud_run` command, a convenient tool that automates the entire deployment workflow. This single command packages the code, builds a container image, pushes it to Artifact Registry, and launches the service on Cloud Run, making it accessible on the web.

The `uvx` command allows to run command line tools published as Python packages without requiring a global installation of those tools.

- **Enable APIS**
    ```
    gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    aiplatform.googleapis.com \
    compute.googleapis.com
    ```
    Output: `Operation "operations/acat.p2-[GUID]" finished successfully.`

**Introducing the APIs**
    - **Cloud Run Admin API** (run.googleapis.com) allows you to run frontend and backend services, batch jobs, or websites in a fully managed environment. It handles the infrastructure for deploying and scaling your containerized applications.  
    - **Artifact Registry API** (artifactregistry.googleapis.com) provides a secure, private repository to store your container images. It is the evolution of Container Registry and integrates seamlessly with Cloud Run and Cloud Build.  
    - **Cloud Build API** (cloudbuild.googleapis.com) is a serverless CI/CD platform that executes your builds on Google Cloud infrastructure. It is used to build your container image in the cloud from your Dockerfile.  
    - **Vertex AI API** (aiplatform.googleapis.com) enables your deployed application to communicate with Gemini models to perform core AI tasks. It provides the unified API for all of Google Cloud's AI services.  
    - **Compute Engine API** (compute.googleapis.com) provides secure and customizable virtual machines that run on Google's infrastructure. While Cloud Run is managed, the Compute Engine API is often required as a foundational dependency for various networking and compute resources.  

- **Set the variables** in the terminal:
    - `PROJECT_ID=$(gcloud config get-value project)`
    - `PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")`
    - `SA_NAME=project1-cloudrun-service`

- **Create .env file** in /home/bshouvik/google-genai-project1/med_agent directory: `more .env`
    ```
    PROJECT_ID=cohort1-project-31032026
    PROJECT_NUMBER=612889370094
    SA_NAME=project1-cloudrun-service
    SERVICE_ACCOUNT=project1-cloudrun-service@cohort1-project-31032026.iam.gserviceaccount.com
    MODEL="gemini-2.5-flash"
    ```

- **Update agent.py** - _Refer to the aget.py file for the updates_
    This is used as a reference to build [agent.py](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/5-deploying-agents/deploy-an-adk-agent-to-cloud-run?utm_source=newsletter&utm_medium=sendy#7)

- **Execute Cloud Run command**

    ```
    uvx --from google-adk==1.14.0 \
    adk deploy cloud_run \
    --project=$PROJECT_ID \
    --region=us-central1 \
    --service_name=my-app-on-cloud \
    --with_ui \
    . \
    -- \
    --labels=genai-project1=project1 \
    --service-account=$SERVICE_ACCOUNT
    ```

Output excerpt:
Service [my-app-on-cloud] revision [my-app-on-cloud-00001-k8k] has been deployed and is serving 100 percent of traffic.
Service URL: https://my-app-on-cloud-918201028398.europe-west1.run.app






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
    



