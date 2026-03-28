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
- Enabled required APIs:

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
    
- `mkdir med_agent` & `cd med_agent`
- Create `requiremets.txt` in the `med_agent` folder
    ```
    google-adk==1.14.0
    langchain-community==0.3.27
    lxmltodict
    ```
- Create python virtual environment: `uv venv --python 3.12`
- Activate virtual environment: `source .venv/bin/activate`
- Install dependencies: `uv pip install -r requirements.txt`
- Set up environment variables:
    - `PROJECT_ID=$(gcloud config get-value project)`
    - `PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")`
    - `SA_NAME=project1-cloudrun-service`
- Create .env file in /home/bshouvik/google-genai-project1/med_agent directory: `more .env` (_Hardcoded the values_)
    ```
    PROJECT_ID=cohort1-project-31032026
    PROJECT_NUMBER=612889370094
    SA_NAME=project1-cloudrun-service
    SERVICE_ACCOUNT=project1-cloudrun-service@cohort1-project-31032026.iam.gserviceaccount.com
    MODEL="gemini-2.5-flash"
    ```
- Create an agent: `adk create med_assistant`. 
    - model: gemini-2.5-flash for root agent
    - Vertex AI
    - Google Cloud project ID [cohort1-project-31032026]
    - Google Cloud region [us-central1]
- Folder structure:
    - Root of the project is `google-genai-project1` which is the git repo
    - Folder `med_agent` is created which holds all installations and python venv
    - Inside `med_agent` an agent is created within directory `med_assistant` within which all agent specific files are created
        - .env
        - __initi.py__
        - agent.py
        - _to be added_
- **Update agent.py** - _Refer to the agent.py file for the updates_
    This is used as a reference to build [agent.py](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/5-deploying-agents/deploy-an-adk-agent-to-cloud-run?utm_source=newsletter&utm_medium=sendy#7)

- **Setup IAM permissions**
- Load the variables into your shell session: `source .env`
- Create a dedicated service account for your Cloud Run service so that it has its own specific permission
    `gcloud iam service-accounts create ${SA_NAME} --display-name="Service Account for project1"`
- Grant the "Vertex AI User" role to the service account
    ```
    gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
    ```
- Test the basic agent: `adk run med_assistant` WORKS!!
- Test the agent on Development Web UI: `adk web --allow_origins="*"` WORKS!!

### Configure Cloud Run for Application Deployment
Use the `adk deploy cloud_run` command, a convenient tool that automates the entire deployment workflow. This single command packages the code, builds a container image, pushes it to Artifact Registry, and launches the service on Cloud Run, making it accessible on the web.

The `uvx` command allows to run command line tools published as Python packages without requiring a global installation of those tools.
 
- **Depoloy the Agent with Cloud Run**

    ```
    uvx --from google-adk==1.14.0 \
    adk deploy cloud_run \
    --project=$PROJECT_ID \
    --region=us-central1 \
    --service_name=med-app-on-cloud \
    --with_ui \
    . \
    -- \
    --labels=project=genai-project1 \
    --service-account=$SERVICE_ACCOUNT
    ```
A repository named [cloud-run-source-deploy] in region [us-central1] will be created

Output excerpt:
```
Service [med-app-on-cloud] revision [med-app-on-cloud-00002-gj9] has been deployed and is serving 100 percent of traffic.
Service URL: https://med-app-on-cloud-612889370094.us-central1.run.app
```



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
    
## Notes

**Reference:** https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-empowering-with-tools#0

A basic agent built with the ADK has a powerful LLM brain, but it also has limitations: it can't access information created after its training date, and it can't interact with external services. It's like a brilliant, book-smart assistant locked in a library with no phone or internet. To make an agent truly useful, we need to give it tools.

Think of tools as giving that AI assistant access to the outside world: a calculator, a web browser, or access to a specific company database. In ADK, a tool is a modular piece of code that allows the agent to perform specific actions like looking up real-time data or calling an external API. Using tools extends its capabilities far beyond simple conversation.

ADK offers three categories of tools:

- **Function Tools:** Custom tools you develop to meet your application's unique requirements, such as predefined functions and agents.
- **Built-in Tools:** Ready-to-use tools provided by the framework for common operations, like Google Search and Code Execution.
- **Third-party Tools:** Popular external libraries such as Serper and tools from LangChain and CrewAI.
To learn more about using Tools with ADK Agents, have a look at the official documentation. In this codelab, we will add tools to transform our simple agent into a capable personal travel assistant. Let's begin!


Let's break down the powerful new pattern in the code:

A New Specialist Agent: We've defined a completely new agent, google_search_agent. Note its specific description and that its only tool is google_search. It's a search specialist.
agent_tool.AgentTool: This is a special wrapper from the ADK. It takes an entire agent (our google_search_agent) and packages it to look and act like a standard tool.
A Smarter ﻿**root_agent**: Our root_agent now has a new tool: AgentTool(agent=google_search_agent). It doesn't know how to search the web, but it knows it has a tool it can delegate search tasks to.
Notice the instruction field is gone from root_agent. Its instructions are now implicitly defined by the tools it has available.

The root_agent has become an orchestrator or a router, whose main job is to understand a user's request and pass it to the correct tool, either the get_fx_rate function or the google_search_agent. This decentralized design is key to building complex, maintainable agent systems.


## PubmedQueryRun Tool

`uv pip install langchain-community xmltodict`

