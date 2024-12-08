from flask import Flask, render_template, jsonify,  request
from store_index import store_data
from finalEmbed import embed_response, collected_data

# import torch
# from transformers import AutoModelForQuestionAnswering, AutoTokenizer
# from langchain_ollama import OllamaLLM

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.vectorstores import VectorStoreRetriever
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import RetrievalQA
# from langchain_ollama import ChatOllama


# model = OllamaLLM(model="llama3.2")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatpage", methods=["GET", "POST"])
def chat_page():
    return render_template("chat.html")

    

@app.route("/get", methods=["GET", "POST"])
def chat():
    userQuery = request.form["msg"]  # User's question
    print(f'User query: {userQuery}')

    userUrl = request.form["url"]
    print(userUrl)

    data = store_data(userUrl)
    print(data)

    result = embed_response(data,userQuery)

    # result = model.invoke(input=f'{userQuery}')

    return result



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)



