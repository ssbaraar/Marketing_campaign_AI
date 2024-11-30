# 📧 AI Email Marketing Team

<div align="center">
  
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red.svg)
![MongoDB](https://img.shields.io/badge/mongodb-6.0%2B-green.svg)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-blue)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Made with Love](https://img.shields.io/badge/Made%20with-❤-red.svg)

</div>

<div align="center">
  <img src="preview_imgs/Email_Marketing_Campign_Planner.png" alt="AI Email Marketing Team Logo" width="800"/>
  
  <h1>AI-Powered Email Marketing Campaign Generator</h1>
  
  <p align="center">
    <strong>Create professional email marketing campaigns in minutes with the power of AI 🚀</strong>
  </p>
  
  <p align="center">
    <a href="#demo">View Demo</a> •
    <a href="#key-features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#documentation">Docs</a>
  </p>

  <br/>
  
  <img src="preview_imgs/Screenshot 2024-11-30 at 20.23.10.png" alt="AI Email Marketing Team Preview 1" width="100%" />
  <img src="preview_imgs/Screenshot 2024-11-30 at 20.23.32.png" alt="AI Email Marketing Team Preview 2" width="100%" />
</div>

<br/>

<details>
<summary>📋 Table of Contents</summary>

- [✨ Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [💻 Tech Stack](#-tech-stack)
- [🏗️ Architecture](#️-architecture) 
- [📖 Documentation](#-documentation)
- [🔧 Configuration](#-configuration)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
</details>

## ✨ Key Features

- 🤖 **AI-Powered Email Generation**: Leverages Google's Gemini AI to create compelling email campaigns
- 📊 **Smart Campaign Management**: Track, manage, and optimize your email campaigns
- 🎯 **Targeted Audience Segmentation**: Create personalized campaigns for different audience segments
- 📈 **Performance Analytics**: Track open rates, click-through rates, and campaign success
- 🔒 **Secure Authentication**: Enterprise-grade security with JWT and bcrypt encryption
- 💫 **Interactive UI**: Modern, responsive interface with real-time updates and animations
- 🔄 **Workflow Automation**: Streamlined campaign creation and approval process

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/Email_marketing.git
   cd Email_marketing
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials:
   # - MONGODB_URI: Your MongoDB connection string
   # - GOOGLE_API_KEY: Your Google Gemini API key
   # - JWT_SECRET_KEY: Your JWT secret key
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 💻 Tech Stack

- **Frontend**: Streamlit with custom CSS animations and responsive design
- **Backend**: Python 3.8+
- **Database**: MongoDB 6.0+
- **AI Engine**: Google Gemini
- **Authentication**: JWT + bcrypt
- **Deployment**: Docker-ready

## 🔄 Workflow

1. **Authentication**
   - Secure login/signup system
   - JWT-based session management
   - Role-based access control

2. **Campaign Creation**
   - Name your campaign
   - Define target audience
   - Set campaign goals
   - Specify timeline and requirements

3. **AI-Powered Content Generation**
   - Strategy generation
   - Email content creation
   - A/B testing suggestions
   - Tone and style customization

4. **Review & Approval Process**
   - Multi-step approval workflow
   - Collaborative feedback system
   - Version control for email drafts
   - Final campaign validation

5. **Campaign Management**
   - Real-time campaign status
   - Performance metrics
   - Audience engagement tracking
   - Campaign optimization suggestions

## 🎨 UI Features

- **Modern Design**
  - Clean, minimalist interface
  - Responsive layout
  - Dark/Light mode support
  - Custom animations and transitions

- **Interactive Elements**
  - Progress indicators
  - Real-time updates
  - Toast notifications
  - Loading animations

- **Dashboard**
  - Campaign overview cards
  - Performance metrics
  - Activity timeline
  - Status indicators

## 🔧 Configuration

### Environment Variables

```env
MONGODB_URI=your_mongodb_connection_string
GOOGLE_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
```

### MongoDB Setup

1. Create a MongoDB Atlas account
2. Set up a new cluster
3. Configure network access
4. Create database user
5. Copy connection string to .env

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Streamlit for the amazing web framework
- MongoDB for reliable data storage
- All contributors and users of this project
