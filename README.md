# Security Policy Generator

A comprehensive Flask-based web application for generating professional security policies, controls, and implementation guides using AI-powered assistance.

## 🚀 Features

### Core Features
- **Multi-Industry Support**: Tailored policies for Technology, Healthcare, Financial Services, Manufacturing, and more
- **Compliance Framework Integration**: ISO 27001, ISO 42001, NIST AI RMF, PCI DSS, SOC 2, GDPR, and others
- **Multiple Selection**: Choose multiple industries and frameworks for comprehensive coverage
- **Professional Output**: Download policies in Markdown or PDF format
- **Organization Size Adaptation**: Policies tailored for small, medium, large, and enterprise organizations

### AI-Powered Features (Claude Integration)
- **Enhanced Policy Generation**: Sophisticated, contextual policies using Claude AI
- **Security Controls Generation**: Detailed technical controls with implementation guidance
- **Implementation Guide**: Step-by-step deployment roadmaps and resource planning
- **Complete Security Package**: All three components (policy, controls, implementation) in one generation

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI Integration**: Anthropic Claude API
- **PDF Generation**: ReportLab
- **Database**: SQLite (for policy tracking)
- **Security**: CSRF protection, input validation

## 📋 Prerequisites

- Python 3.7 or higher
- Anthropic Claude API key (optional, for AI features)
- Modern web browser

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd security-policy-generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Claude API (Optional)
To enable AI-powered features, set your Claude API key:

```bash
export CLAUDE_API_KEY="sk-ant-your-api-key-here"
```

Or add it to your shell profile:
```bash
echo "export CLAUDE_API_KEY='sk-ant-your-api-key-here'" >> ~/.zshrc
source ~/.zshrc
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your browser and navigate to: `http://localhost:5013`

## 📖 Usage Guide

### Basic Policy Generation
1. Fill in your organization details
2. Select relevant industries and compliance frameworks
3. Add any additional requirements
4. Click "Generate Professional Policy"
5. Download in Markdown or PDF format

### AI-Powered Features
1. **Generate Controls**: Creates detailed security controls based on your policy
2. **Generate Implementation Guide**: Provides deployment roadmap and resource planning
3. **Generate Complete Package**: Creates all three components together

## 🏗️ Project Structure

```
security-policy-generator/
├── app.py                          # Main Flask application
├── policy_generator.py             # Standard policy generator
├── claude_policy_generator.py      # AI-powered policy generator
├── requirements.txt                # Python dependencies
├── setup_claude.py                 # Claude API setup script
├── templates/                      # HTML templates
│   ├── base.html
│   └── index.html
├── static/                         # Static assets
│   ├── css/
│   └── js/
├── temp/                          # Temporary files
├── uploads/                       # Generated files
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables
- `CLAUDE_API_KEY`: Your Anthropic Claude API key
- `SECRET_KEY`: Flask secret key (auto-generated if not set)

### API Endpoints
- `GET /`: Main application page
- `POST /generate_policy`: Generate security policy
- `POST /generate_controls`: Generate security controls (AI)
- `POST /generate_implementation_guide`: Generate implementation guide (AI)
- `POST /generate_complete_package`: Generate complete security package (AI)
- `POST /download_policy`: Download policy as Markdown
- `POST /download_pdf`: Download policy as PDF

## 🔒 Security Features

- CSRF protection on all forms
- Input validation and sanitization
- Secure file handling
- Environment variable protection for API keys
- Comprehensive error handling

## 📊 Supported Industries

- Technology/Software
- Healthcare
- Financial Services
- Manufacturing
- Retail/E-commerce
- Education
- Government
- Non-profit
- Consulting
- Real Estate
- Transportation
- Energy
- Media/Entertainment
- Legal Services

## 🎯 Supported Compliance Frameworks

- **ISO 27001**: Information Security Management System
- **ISO 42001**: AI Management System
- **NIST AI RMF**: AI Risk Management Framework
- **NIST SP 800-53**: Security and Privacy Controls
- **FedRAMP**: Federal Risk and Authorization Management Program
- **CIS Controls**: Critical Security Controls
- **PCI DSS**: Payment Card Industry Data Security Standard
- **SOC 2**: Service Organization Control 2
- **GDPR**: General Data Protection Regulation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section in `CLAUDE_SETUP.md`
2. Review the console output for error messages
3. Ensure all dependencies are installed correctly
4. Verify your Claude API key is set correctly (if using AI features)

## 🔄 Updates and Maintenance

- Regular updates to compliance frameworks
- New industry templates added periodically
- AI model improvements and prompt optimization
- Security patches and bug fixes

## 📈 Roadmap

- [ ] Multi-language support
- [ ] Advanced policy customization
- [ ] Integration with GRC platforms
- [ ] Real-time collaboration features
- [ ] Policy version control
- [ ] Automated compliance checking
- [ ] Mobile application
- [ ] API for third-party integrations

---

**Note**: This application is designed for educational and professional use. Always review generated policies with qualified security professionals before implementation. 