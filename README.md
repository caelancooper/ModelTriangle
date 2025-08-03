# Pyramid Model Conference ◭

## Executive AI Decision Support System

A sophisticated multi-agent AI interface designed for executives who require comprehensive insights from multiple state-of-the-art language models. The Pyramid Model Conference harmonizes responses from three carefully selected open-source models to provide well-rounded, enterprise-grade AI assistance.

## 🎯 Target Audience

This application is specifically designed for **C-suite executives and senior decision-makers** who need:
- Multi-perspective AI analysis for complex business decisions
- Access to the latest open-source AI capabilities without vendor lock-in
- Reliable, consistent AI assistance for strategic planning
- Data-driven insights from multiple AI reasoning approaches

## 🤖 Selected AI Models

The system leverages three complementary models, each chosen for specific strengths:

### 1. **DeepSeek-R1** (`deepseek-ai/DeepSeek-R1`)
- **Specialty**: Advanced reasoning and analytical thinking
- **Strength**: Complex problem-solving and logical analysis
- **Use Case**: Strategic decision support and detailed reasoning

### 2. **Llama 3.3 Maverick** (`meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8`)
- **Specialty**: Balanced general intelligence and instruction following
- **Strength**: Comprehensive responses and nuanced understanding
- **Use Case**: General business intelligence and communication

### 3. **Qwen 2.5 Coder** (`Qwen/Qwen2.5-Coder-32B-Instruct`)
- **Specialty**: Technical analysis and code-related tasks
- **Strength**: Data processing, automation, and technical solutions
- **Use Case**: Technical implementation and process optimization

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Together.ai API key ([Get one here](https://api.together.xyz/))

### Installation & Setup

#### Option 1: Direct Download & Run
```bash
# Download the application
curl -O https://raw.githubusercontent.com/[your-repo]/pyramid-conference/main/pyramid_chat.py

# Set your Together.ai API key
export API_KEY="your_together_ai_api_key_here"

# Install dependencies
pip install customtkinter pandas huggingface-hub

# Run the application
python pyramid_chat.py
```

#### Option 2: Clone Repository
```bash
# Clone the repository
git clone https://github.com/caelancooper/ModelTriangle.git

# Set environment variable
export API_KEY="your_together_ai_api_key_here"

# Install dependencies
pip install -r requirements.txt

# Run the application
python pyramid_chat.py
```

### Setting Up Your API Key

1. **Get Together.ai API Key**:
   - Visit [Together.ai](https://api.together.xyz/)
   - Sign up for an account
   - Generate your API key

2. **Set Environment Variable**:
   
   **Linux/macOS:**
   ```bash
   export API_KEY="your_api_key_here"
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   set API_KEY=your_api_key_here
   ```
   
   **Windows (PowerShell):**
   ```powershell
   $env:API_KEY="your_api_key_here"
   ```

3. **Persistent Setup** (Recommended):
   Add the export command to your shell profile (`.bashrc`, `.zshrc`, etc.):
   ```bash
   echo 'export API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

## 💼 Key Features

- **Multi-Agent Responses**: Get insights from three different AI models simultaneously
- **Conversation History**: Save and load conversation sessions
- **Streaming Responses**: Real-time response generation
- **Executive-Friendly Interface**: Clean, professional UI designed for business use
- **Session Management**: Save important conversations for future reference
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🔮 Future Development Roadmap

We invite contributions and feature additions in the following areas:

### 📋 Task Management Integration
- **Project Planning**: AI-assisted project breakdown and timeline generation
- **Decision Trees**: Interactive decision-making frameworks
- **Risk Assessment**: Automated risk analysis and mitigation suggestions
- **Resource Allocation**: Optimization recommendations for team and budget allocation

### 🌐 Web Intelligence Backend
- **Market Research**: Automated competitor analysis and market trend monitoring
- **News Aggregation**: Real-time industry news summarization and impact analysis
- **Social Sentiment**: Brand and market sentiment tracking
- **Regulatory Monitoring**: Compliance and regulatory change notifications

### 📊 Custom Data Processing
- **Document Analysis**: Upload and analyze contracts, reports, and presentations
- **Financial Modeling**: Excel/CSV integration for financial analysis
- **Survey Processing**: Customer feedback and employee survey analysis
- **Performance Metrics**: KPI tracking and trend analysis

### 🔧 Technical Integrations
- **CRM Integration**: Salesforce, HubSpot, and other business system connectivity
- **Calendar Integration**: Meeting summaries and action item extraction
- **Email Processing**: Important email summarization and response drafting
- **API Ecosystem**: Custom integrations with existing business tools

## 📁 Project Structure

```
pyramid-conference/
├── main.py          # Main application file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Dependencies

```txt
customtkinter>=5.2.0
pandas>=2.0.0
huggingface-hub>=0.19.0
```

## 🤝 Contributing

We welcome contributions from developers and business professionals alike. Areas of particular interest:

1. **Business Logic**: Industry-specific analysis modules
2. **Data Connectors**: Integration with business data sources
3. **UI/UX Improvements**: Enhanced executive dashboard features
4. **Security**: Enterprise-grade security implementations
5. **Performance**: Optimization for large-scale data processing

## 📄 License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## 🆘 Support

For technical support or business inquiries:
- 📧 Email: caelancooper100@gmail.com

## 🔒 Privacy & Security

- All conversations remain local to your machine
- API communications are encrypted via HTTPS
- No conversation data is stored on external servers
- Enterprise deployment options available for enhanced security

---

**Pyramid Model Conference ◭** - *Harmonizing AI Intelligence for Executive Decision Making*