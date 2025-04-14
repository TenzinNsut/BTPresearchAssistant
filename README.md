# Research Assistant

An AI-powered tool designed to help researchers extract insights from academic papers. This application allows users to upload PDFs or provide URLs to research papers, then ask specific questions about the content.

![Research Assistant Interface](https://kstatic.googleusercontent.com/files/202018a3b69e60845af5a9903c7bf87010a2e2e8d987bd0fef5a598c0ee2b4345721a4c549a4a8039ff3a3dfd85239de3d6735b9956ff60f525b72e36c377164)

## Features

- **PDF Upload**: Upload research papers in PDF format
- **URL Support**: Extract content from research paper URLs (ArXiv, IEEE, Science Direct)
- **AI-Powered Q&A**: Ask specific questions about the paper and get accurate, context-aware responses
- **Session Management**: Manage multiple research sessions with automatic cleanup
- **Mobile-Friendly UI**: Responsive design that works across devices

## Technology Stack

- **Backend**: Python with Flask
- **AI Processing**: LangChain, HuggingFace Transformers, PyTorch
- **Vector Database**: Pinecone for efficient semantic search and retrieval
- **Web Scraping**: Beautiful Soup, Selenium for dynamic content extraction
- **PDF Processing**: PyPDF for extracting text from PDFs

## Deployment

This application is configured for deployment on [Render](https://render.com/):

1. Connect your GitHub repository to Render
2. Create a new Web Service pointing to this repository
3. The deployment will automatically use the `render.yaml` configuration

## Environment Variables

Set the following environment variables in your Render dashboard:

- `HUGGINGFACE_API_KEY`: Your Hugging Face API key for embedding generation
- `PINECONE_API_KEY`: Your Pinecone API key for vector storage
- `PINECONE_ENVIRONMENT`: Your Pinecone environment (e.g., "us-west1-gcp")

## Local Development

To run the app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the build script
./build.sh  # On Linux/Mac
# or 
python -c "exec(open('build.sh').read())"  # On Windows

# Start the server
python main.py
```

The app will be available at http://localhost:8080

## Usage

1. **Upload a PDF**: Click the "Upload" button in the sidebar and select a research paper PDF
2. **Or Enter a URL**: Paste a URL from ArXiv, IEEE, or Science Direct in the URL field
3. **Ask Questions**: Type your question about the paper in the chat box
4. **Review Responses**: The AI will provide specific answers based on the paper's content

## Project Structure

```
research-assistant/
├── main.py                    # Main Flask application
├── finalEmbed.py              # Embedding and vector search logic
├── requirements.txt           # Project dependencies
├── scrapers/                  # Web scrapers for different sites
│   ├── ArxivScraper.py
│   ├── IeeeScraper.py
│   ├── ScienceDirectScraper.py
│   └── UniversalScraper.py
├── static/                    # Static assets
│   ├── styles.css
│   └── homeStyle.css
├── templates/                 # HTML templates
│   ├── index.html
│   └── chat.html
└── uploads/                   # Directory for uploaded PDFs
```

## Limitations

- Currently supports PDFs and specific research paper sites (ArXiv, IEEE, Science Direct)
- Session data is stored in memory and will be lost on server restart
- Maximum PDF size is limited to 10MB

## Future Improvements

- Support for more research paper sources
- Persistent storage for user sessions
- Integration with reference management tools
- Enhanced visualization of paper structure and key findings
- Multi-document comparison capabilities

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project uses various open-source libraries and AI models
- Research paper crawler and scraping techniques adapted from academic literature
- User interface design inspired by modern AI assistants
