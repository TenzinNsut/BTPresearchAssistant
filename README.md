# Research Paper Insights Generator

## Overview
This project provides a system to retrieve and analyze research papers effectively. By allowing users to input the URL of a research paper, the application scrapes its content, processes it into embeddings, and generates precise, context-aware responses to user queries using advanced natural language processing (NLP) techniques. The output is displayed in a chat interface for seamless user interaction.
![image](https://github.com/user-attachments/assets/e05a2207-e5f7-47d7-a83f-c1cbbcaea67b)

---

## Features
- **Web Scraping**: Extract textual content from research paper URLs using Beautiful Soup.
- **Vector Embedding Generation**: Represent research content in high-dimensional vectors.
- **FAISS for Similarity Search**: Perform efficient in-memory searches for relevant content.
- **Speculative RAG Model**: Utilize a dual-model architecture for response generation:
  - A specialized model drafts responses.
  - A generalized model refines and verifies them.
- **Flask Integration**: Provide an intuitive chat-based interface for query-response interaction.
- **Supported Websites**: Arxiv, ScienceDirect, Iee
---

## Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/your-repo-name/research-paper-insights-generator.git
   cd research-paper-insights-generator
   ```

2. **Set Up a Virtual Environment & Install the required dependencies**:
   ```
   create a virtual environment: python -m venv ayurbotEnv
   pip install -r requirements.txt
   ```
   
3. **Set up the necessary application**:
   - `ollama`: Install ollama on your device. (https://ollama.com/)
   - `llama3.2`: Install llama3.2, by running this command in cmd. "ollama pull llama3.2"


4. **Run the Application**:
   ```bash
   python main.py
   ```

5. **Access the chatbot through the provided URL or interface.**:


---

## Usage
1. Paste the URL of a research paper into the provided input field.
2. Submit a query related to the research content.
3. View the generated response in the chat interface, complete with references to relevant sections of the research paper.

---

## Technologies Used
- **Programming Language**: Python
- **Web Framework**: Flask
- **Web Scraping**: Beautiful Soup, Selenium
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Model Architecture**: Speculative Retrieval-Augmented Generation (RAG)

---


## Future Enhancements
- **User Authentication**: Add login and profile management features.
- **Cloud Deployment**: Host the application on AWS/GCP/Azure for broader accessibility.
- **Support for PDF Uploads**: Allow users to upload research papers directly.
- **Big Data Integration**: Use distributed processing tools like Apache Spark for handling large datasets.

---

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes and push to your fork.
4. Submit a pull request for review.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For any queries or suggestions:
- Email: [your-email@example.com](mailto:your-email@example.com)
- GitHub Issues: [Create an issue](https://github.com/your-repo-name/research-paper-insights-generator/issues)
