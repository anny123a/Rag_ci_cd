from dotenv import load_dotenv
import os
import sys

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from store import FAISS_INDEX_PATH, load_vector_store

load_dotenv()

_qa_chain = None


def get_llm():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing in your .env file.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=google_api_key,
    )


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_qa_chain(index_path=FAISS_INDEX_PATH):
    db = load_vector_store(index_path)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template(
        """
Answer the question based only on the following context:
{context}

Question: {question}
"""
    )

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | get_llm()
        | StrOutputParser()
    )


def get_qa_chain(index_path=FAISS_INDEX_PATH):
    global _qa_chain

    if _qa_chain is None:
        _qa_chain = build_qa_chain(index_path)

    return _qa_chain


def ask_question(query, index_path=FAISS_INDEX_PATH):
    return get_qa_chain(index_path).invoke(query)



# response=ask_question("can you answer this question?")
# print('response:-',response)
# def main():
#     command = sys.argv[1].lower() if len(sys.argv) > 1 else "help"

#     if command == "ask":
#         if len(sys.argv) < 3:
#             print('Usage: python rag.py ask "Your question here"')
#             return

#         query = " ".join(sys.argv[2:])
#         print(ask_question(query))
#         return

#     print("Usage:")
#     print('  python rag.py ask "Your question here"')
#     print("  python store.py")


# if __name__ == "__main__":
#     main()
