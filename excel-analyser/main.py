from langchain_experimental.agents import create_csv_agent # type: ignore
from langchain.llms import OpenAI # type: ignore
import streamlit as st # type: ignore
import pandas as pd # type: ignore
from dotenv import load_dotenv # type: ignore
import os
import altair as alt # type: ignore
import matplotlib # type: ignore
from IPython.display import display # type 
def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="Ask your CSV", page_icon="📊")
    st.title("Ask your CSV 📈")

    csv_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

    if csv_file != None and csv_file:
        agent = create_csv_agent(
            OpenAI(temperature=0.4), csv_file, verbose=True)
        user_question = st.text_input("Ask a question about your CSV: ")

        if user_question is not None and user_question != "":
            result_placeholder = st.empty()
            with st.spinner(text="In progress..."):
                result = agent.run(user_question)
                result_placeholder.write(result)
                display(result)
                if isinstance(result, pd.DataFrame):
                    st.write("### Chart")
                    chart = alt.Chart(result).mark_bar().encode(
                        x='x:Q',
                        y='y:Q'
                    ).interactive()
                    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()
