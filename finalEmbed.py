from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_ollama import ChatOllama


def collected_data(data,userQuery):
    print(f'collected data: {data}')
    print(f'userQuery: {userQuery}')


def embed_response(data,userQuery):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=300)
    docs = text_splitter.split_text(data)
    embeddings_llama = OllamaEmbeddings(model="llama3.2") 
    library = FAISS.from_texts(docs, embedding=embeddings_llama)
    retriever = library.as_retriever()
    llm = ChatOllama(model="llama3.2")
    query = userQuery
    system_prompt = (
    "You are a helpful AI assistant called samy."
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "You were developed by Tenzin, Tatwansh and Praveen who are students at NSUT(Netaji Subhas University of Technology ), which is a college"
    "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    result = chain.invoke({"input": query})
    print(result['answer'])
    return result['answer']




