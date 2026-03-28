from google.adk.agents import Agent
from google.adk.tools.langchain_tool import LangchainTool

from .third_party_tools import langchain_pubmed_tool

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="""
                You are a medical research assistant.
                When answering questions that require scientific or clinical evidence,
                you MUST use the PubMed research tool to retrieve peer-reviewed sources
                and cite findings in your reasoning.
                """,
    instruction="""
                You are a medical research assistant.
                When answering questions that require scientific or clinical evidence,
                you MUST use the PubMed research tool.
                When querying PubMed, prioritize:
                    - systematic reviews
                    - meta-analyses
                    - randomized controlled trials
                    - recent publications (last 5 years) when available
                Synthesize findings clearly and base conclusions strictly on evidence.
                """,
    tools=[
        LangchainTool(langchain_pubmed_tool),  
    ]
)