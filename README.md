###  AWS Bedrock RAG API
A production-ready Retrieval-Augmented Generation (RAG) API built with FastAPI and AWS Bedrock, featuring intelligent document retrieval and response generation capabilities.
🌟 Key Features

Retrieval-Augmented Generation: Combines knowledge base retrieval with LLM generation for accurate, contextual responses
AWS Bedrock Integration: Leverages AWS's managed AI services for scalable inference
Production-Ready Architecture: Comprehensive error handling, logging, and configuration management
FastAPI Framework: High-performance async API with automatic OpenAPI documentation
Flexible Model Support: Compatible with multiple LLM models including Llama 3.3 70B

🏗️ Architecture Overview
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   AWS Bedrock   │    │  Knowledge Base │
│   Application   │───▶│   Runtime       │───▶│   (Vector DB)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
   REST Endpoints        Model Invocation        Document Retrieval
🚀 Quick Start
Prerequisites

Python 3.8+
AWS Account with Bedrock access
Configured AWS credentials
Knowledge Base set up in AWS Bedrock

Installation

Clone the repository
bash git clone https://github.com/KalenAsberry12/RAG-API
cd rag-api

Install dependencies
bash pip install -r requirements.txt

Environment Configuration
Create a .env file in the project root:
envAWS_REGION=us-east-2
KNOWLEDGE_BASE_ID=your_knowledge_base_id
MODEL_ARN=arn:aws:bedrock:us-east-2::foundation-model/meta.llama3-3-70b-instruct-v1:0

Run the application
bashpython main.py
Or with uvicorn directly:
bashuvicorn main:app --host 127.0.0.1 --port 8000 --reload


📚 API Documentation
Endpoints
GET /
Health check endpoint

Response: Welcome message and API status

GET /bedrock/query
Main RAG endpoint for querying the knowledge base

Parameters:

text (query string): Input text for the model


Response: JSON object with generated response
Example:
bashcurl "http://localhost:8000/bedrock/query?text=What%20is%20machine%20learning?"


Interactive API Documentation
Once running, visit:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

🔧 Technical Implementation
Code Quality Improvements
This implementation showcases several production-ready enhancements over basic implementations:
✅ Enhanced Error Handling

Comprehensive exception catching with specific AWS error types
Detailed logging for debugging and monitoring
User-friendly error messages with appropriate HTTP status codes

✅ Configuration Management

Environment variable validation
Secure credential handling via .env files
Flexible configuration for different deployment environments

✅ Performance Optimizations

Efficient client initialization
Async/await patterns for non-blocking operations
Optimized request/response handling

✅ Security Best Practices

No hardcoded credentials
Environment-based configuration
Secure AWS SDK integration

✅ Code Organization

Clean separation of concerns
Modular client initialization
Clear documentation and type hints

Architecture Decisions

FastAPI: Chosen for high performance, automatic API documentation, and excellent async support
AWS Bedrock: Provides managed AI infrastructure with enterprise-grade security and scalability
Environment Variables: Ensures secure and flexible configuration management
Boto3: Official AWS SDK providing robust AWS service integration

📋 Requirements
txtboto3==1.36.20
fastapi==0.115.8
python-dotenv==1.0.1
uvicorn==0.34.0
🛠️ Development
Local Development Setup

Virtual Environment (recommended)
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Development Dependencies
bashpip install -r requirements.txt

Run with Hot Reload
bashuvicorn main:app --reload


Testing
Test the API endpoints:
bash# Health check
curl http://localhost:8000/

# Query the RAG system
curl "http://localhost:8000/bedrock/query?text=Your%20question%20here"
🚀 Deployment
Docker Deployment
dockerfileFROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
AWS Lambda Deployment
This API can be deployed as a serverless function using AWS Lambda with the Mangum adapter:
pythonfrom mangum import Mangum
handler = Mangum(app)
🔐 Security Considerations

AWS IAM: Ensure proper IAM roles and policies for Bedrock access
Environment Variables: Never commit .env files to version control
API Keys: Use AWS credentials through IAM roles in production
CORS: Configure appropriate CORS policies for web applications

📈 Performance & Scaling

Async Operations: All endpoints use async/await for optimal performance
Connection Pooling: Boto3 handles connection pooling automatically
Caching: Consider implementing response caching for frequently asked questions
Load Balancing: Deploy behind a load balancer for high availability

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open a Pull Request
