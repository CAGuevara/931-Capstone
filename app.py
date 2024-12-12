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
st.markdown("Assistant Agent Power by the Casi Nada Company!")
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
            Act as a successful vendor to create a compelling, one-page sales pitch designed to engage a target company based on publicly available web data. 
            The pitch should be concise, persuasive, and tailored to highlight how the product or service aligns with the company's strategy, leadership priorities, and market positioning. 
            Maintain a formal and professional tone with a sales-oriented approach. Strictly adhere to the following structure:

            1. Opening Statement (2-3 sentences):
            - Craft a personalized introduction that grabs the attention of key decision-makers.
            - Mention a specific leadership figure or recent public statement to establish credibility.

            2. Value Proposition (2-3 bullet points):
            - Align our {product_name} benefits with the {company_information}'s current strategy or priorities, referencing specific insights from job postings, public reports, or press releases.
            - Highlight how our solution addresses 1-2 specific pain points or opportunities relevant to the {target_customer}.

            3. Competitor Positioning (1-2 sentences):
            - Briefly differentiate our offering from competitors mentioned in {competitors_url}, focusing on unique strengths.

            4. Tailored Solution (2-3 bullet points):
            - Propose a specific use case of our {product_name} that resonates with the company's needs, based on their technology stack, market goals, or strategic initiatives.
            - Include one quantitative benefit or ROI estimate if available.

            5. Call to Action (1-2 sentences):
            - Conclude with a clear, specific next step (e.g., scheduling a demo, exploring a pilot program).
            - Create a sense of urgency or exclusivity to encourage immediate engagement.

            Additional Guidelines:
            - Ensure the entire pitch fits on one page when formatted as a standard business document.
            - Use bullet points and concise language to maximize impact and readability.
            - Incorporate at least one industry trend or benchmark to validate our offering.
            - Reference 2-3 publicly available sources throughout the pitch for credibility.
            - Maintain a balance between formal professionalism and persuasive sales language.

            Input data:
            Company info: {company_information}
            Product name: {product_name}
            Competitors URL: {competitors_url}
            Product category: {product_category}
            Value proposition: {value_proposition}
            Target customer: {target_customer}
            Vendor name: {vendor_name}

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





