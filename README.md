# CardWise - AI-Powered Credit Card Recommendation System

## 🎯 Overview

CardWise is a professional Streamlit web application that provides personalized credit card recommendations using real-time AI analysis. The app analyzes your financial profile, searches for current credit card offers, and uses the advanced OpenRouter AI model `openai/gpt-oss-20b:free` to generate step-by-step recommendations tailored to your specific needs.

## ✨ Features

- **Real-time AI Analysis**: Advanced AI model analyzes your spending patterns with current market data
- **Live Market Data**: Searches current credit card offers using Google search in real-time
- **Professional UI**: Clean, responsive design with sidebar inputs and main results panel
- **Comprehensive Recommendations**: Step-by-step action plans and optimization tips based on current offers
- **PDF Reports**: Downloadable PDF reports of your personalized recommendations
- **No Fallback Data**: 100% real-time recommendations using current market conditions

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Open in Browser

The app will automatically open in your default browser at `http://localhost:8501`

## 🔧 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Internet connection for real-time credit card data search
- **REQUIRED**: OpenRouter API key for AI recommendations (free tier available)

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd CardWise
   ```

2. **Install Required Packages**
   ```bash
   pip install streamlit requests googlesearch-python reportlab typing-extensions
   ```

3. **Configure API Key (REQUIRED)**
   - Get a free API key from [OpenRouter](https://openrouter.ai/)
   - Copy `secrets_template.toml` to `.streamlit/secrets.toml`
   - Add your API key: `OPENROUTER_API_KEY = "your_key_here"`
   - **Note**: App requires API key to function - no fallback options

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 📖 How to Use

### Step 1: Fill Your Essential Profile

In the sidebar, provide only these 4 essential inputs for maximum accuracy:

- **Monthly Spending**: Your total monthly credit card spending ($500-$20,000)
- **Credit Score Range**: Select your current credit score range (determines eligibility)
- **Primary Goals**: Choose what you want to maximize (cashback, travel, etc.)
- **Top Spending Categories**: Allocate percentages between Dining & Travel, Groceries & Gas, and Other

### Step 2: Generate Recommendations

Click the "🔍 Get AI Recommendations" button to:
- Search for current credit card offers
- Analyze your profile with AI
- Generate personalized recommendations

### Step 3: Review Results

The app will display:
- **Primary Recommendation**: Best credit card for your profile
- **Key Benefits**: Why this card suits you
- **Action Plan**: Step-by-step instructions
- **Optimization Tips**: How to maximize rewards
- **Estimated Value**: Expected annual reward value

### Step 4: Download Report

Generate and download a PDF report of your recommendations for future reference.

## 🛠️ Technical Architecture

### Core Components

1. **UserProfile Class**: Data structure for user financial information
2. **CardWiseApp Class**: Main application logic and UI management
3. **Search Module**: Google search integration for market data
4. **AI Integration**: OpenRouter API for intelligent recommendations
5. **PDF Generation**: ReportLab for downloadable reports

### API Integration

- **Google Search**: Fetches current credit card offers and real-time market data
- **OpenRouter AI**: Uses `openai/gpt-oss-20b:free` model for intelligent, personalized recommendations
- **Real-time Only**: No fallback data - all recommendations based on current market conditions

### Security Features

- API keys stored in Streamlit secrets
- No sensitive data logged or stored
- Graceful error handling for API failures

## 🎨 UI Features

### Professional Design

- **Responsive Layout**: Works on desktop and mobile devices
- **Custom CSS**: Professional gradient backgrounds and styling
- **Interactive Elements**: Sliders, dropdowns, and multi-select inputs
- **Visual Feedback**: Loading spinners and success/error messages

### User Experience

- **Sidebar Navigation**: All inputs organized in collapsible sidebar
- **Main Panel**: Clean display of results and recommendations
- **Download Integration**: One-click PDF generation and download
- **Error Handling**: Graceful fallbacks and user-friendly error messages

## 🔧 Configuration Options

### API Configuration

Edit `.streamlit/secrets.toml`:
```toml
OPENROUTER_API_KEY = "your_api_key_here"
```

### Customization

The app can be customized by modifying:

- **CSS Styles**: Update `apply_custom_css()` method
- **Search Parameters**: Modify search terms in `search_credit_cards()`
- **AI Prompts**: Customize prompts in `_create_recommendation_prompt()`
- **AI Model**: Currently uses `openai/gpt-oss-120b:free` - can be changed in the code

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade streamlit requests googlesearch-python reportlab
   ```

2. **Google Search Rate Limiting**
   - The app includes automatic rate limiting and respectful delays
   - App will stop if real-time data cannot be fetched

3. **API Key Issues**
   - API key is REQUIRED for app functionality
   - Ensure API key is correctly added to `.streamlit/secrets.toml`
   - Get free API key from [OpenRouter](https://openrouter.ai/)

4. **PDF Generation Issues**
   - Ensure ReportLab is properly installed
   - Check file permissions for PDF creation

### Error Messages

- **"Real-time search failed"**: Google search unavailable - app requires current data
- **"API request failed"**: OpenRouter API issue - check API key and connection
- **"API key not found"**: Missing required API key in secrets configuration
- **"PDF generation failed"**: ReportLab issue - check dependencies

## 📋 Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP requests for API calls
- **googlesearch-python**: Google search integration
- **reportlab**: PDF generation
- **typing-extensions**: Type hints support

## 🚀 Deployment

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud

1. Push code to GitHub repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in Streamlit Cloud dashboard
4. Deploy with one click

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🔒 Privacy & Security

- No user data is stored permanently
- API keys are securely managed through Streamlit secrets
- All processing happens locally or through secure API calls
- PDF reports are generated client-side

## 🆘 Support

For issues, questions, or feature requests:

1. Check the troubleshooting section above
2. Review the error messages for specific guidance
3. Ensure all dependencies are properly installed
4. Verify API key configuration if using AI features

## 📝 License

This project is provided as-is for educational and personal use. Please review the terms of service for any APIs used (OpenRouter, Google Search).

---

**CardWise** - Making credit card decisions simple and intelligent. 💳✨