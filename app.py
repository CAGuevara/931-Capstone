import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

#Testing Streamlit
#st.title("Sales Agent")

#lets declare the model and agent to be used
llm = ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"))
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()

#Page Header
st.title("Assistant Agent")
st.markdown("Assistant Agent Power by the Neat Company!")
# Data collection/inputs
with st.form("company_info", clear_on_submit=True):
    vendor_name = st.text_input("**Sales Representative** (What is your name?):")
    product_name = st.text_input("**Product Name** (What product are you selling?):")
    company_url = st.text_input("**Company URL** (The URL of the company you are targeting):")
    product_category = st.text_input("**Product Category** (e.g., 'Data Warehousing' or 'Cloud Data Platform')")
    competitors_url = st.text_input("**Competitors URL** (ex. www.apple.com):")
    value_proposition = st.text_input("**Value Proposition** (A sentence summarizing the product’s value):")
    target_customer = st.text_input("**Target Customer** (Name of the person you are trying to sell to.) :")

    # For the llm insights result
    company_insights = ""
    # Data process
    if st.form_submit_button("Generate Insights"):
        if product_name and company_url:
            st.spinner("Processing...")

            # Use search tool to get Company Information
            company_information = search.invoke(company_url)
            print(company_information)
            #Create prompt <=================
            prompt = """
            act as a succesful vendor to Create a compelling sales pitch designed to engage a target company based on publicly available web data. The pitch should be concise, persuasive, and tailored to highlight how our product or service aligns with the company’s strategy, leadership priorities, and market positioning. Structure the output as follows:
            1. Opening Statement:
            Craft a personalized introduction that grabs the attention of key decision-makers.
            Mention relevant leadership figures or recent public statements to establish credibility and show understanding of the company.
            2. Value Proposition:
            Align our product/service benefits with the company’s current strategy or priorities, referencing insights from job postings, public reports, or press releases.
            Highlight how our solution addresses specific pain points or opportunities.
            3. Competitor Positioning:
            Provide context on competitors mentioned in public data and how our offering differentiates from or outperforms them.
            4. Tailored Solution:
            Propose a specific use case or application of our product/service that resonates with the company’s needs (e.g., based on their technology stack, market goals, or strategic initiatives).
            5. Call to Action:
            Conclude with a clear next step (e.g., scheduling a meeting, providing a demo, or exploring a pilot program).
            Reinforce urgency or exclusivity to encourage immediate engagement.
            Optional Enhancements:
            Incorporate industry trends or benchmarks to further validate our offering.
            Suggest collateral materials (e.g., custom decks, case studies, or white papers) to support the pitch.
            If applicable, outline how alerts or future updates can provide additional value to the prospect.
            Instructions for the LLM:
            Use a professional yet conversational tone that emphasizes collaboration and shared goals.
            Prioritize actionable insights and specificity.
            Link each argument to publicly available sources for credibility.

            Input data:
            Company info: {company_information}
            Product name: {product_name}
            competitors_url: {competitors_url}
            product_category: {product_category}
            value_proposition: {value_proposition}
            target_customer: {target_customer}
            vendor_name: {vendor_name}
           
            
            Output: A polished and impactful sales pitch, ready for use in a client-facing scenario.
            """
            # Lets setup the Prompt Template
            prompt_template = ChatPromptTemplate([("system", prompt)])
            # Chain
            chain = prompt_template | llm | parser
            # Lets see the Insights
            company_insights = chain.invoke(
                {
                    "company_information": company_information,
                    "product_name": product_name,
                    "competitors_url": competitors_url,
                    "product_category": product_category,
                    "value_proposition": value_proposition,
                    "target_customer": target_customer,
                    "vendor_name": vendor_name
                }
            )

st.markdown(company_insights)





