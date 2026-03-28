# Langchain RunPubmedQueryRun Tool integration (searches the PubMed API)
# https://reference.langchain.com/python/langchain-community/tools/pubmed/tool/PubmedQueryRun

from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities import PubMedAPIWrapper

# Configure the PubMed LangChain tool
langchain_pubmed_tool = PubmedQueryRun(
    api_wrapper=PubMedAPIWrapper(
        top_k_results=5,                # More articles = better coverage & triangulation
        doc_content_chars_max=4000,     # Prevents truncation of clinically important abstracts
        email="bshouvik@gmail.com"      # Required by NCBI best practices (avoids throttling)
    )
)

# Give the tool a more specific description for our agent
langchain_pubmed_tool.description = (
    "Searches PubMed for peer-reviewed biomedical and clinical research articles. "
    "Use this tool when evidence-based medical knowledge is required, including "
    "disease mechanisms, clinical outcomes, treatment efficacy, safety data, "
    "guidelines, biomarkers, and systematic reviews. "
    "Returns summarized abstracts with citations from authoritative medical journals. "
    "Prefer this tool over general knowledge when answering research, clinical, "
    "or literature-backed questions."
)