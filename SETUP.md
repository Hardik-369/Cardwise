# CardWise Setup Instructions

## ✅ **API Key Setup (REQUIRED)**

1. **Get your FREE OpenRouter API key:**
   - Go to [https://openrouter.ai/](https://openrouter.ai/)
   - Sign up for a free account
   - Go to [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)
   - Create a new API key
   - Copy the key (starts with `sk-or-v1-...`)

2. **Configure the API key:**
   - Create a folder named `.streamlit` in your CardWise directory
   - Copy `secrets_template.toml` to `.streamlit/secrets.toml`
   - Open `.streamlit/secrets.toml` and replace `your_openrouter_api_key_here` with your actual API key

3. **File structure should look like:**
   ```
   CardWise/
   ├── .streamlit/
   │   └── secrets.toml (your API key here)
   ├── app.py
   ├── README.md
   ├── requirements.txt
   └── secrets_template.toml
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🔧 **Troubleshooting**

- **"API key not found"**: Make sure the `.streamlit/secrets.toml` file exists and contains your API key
- **"No endpoints found"**: The app now uses multiple free models with automatic fallbacks
- **"All AI models failed"**: Check your internet connection and verify your API key is valid

## 🎯 **Model Used**

The app uses the specific OpenRouter model:
- `openai/gpt-oss-20b:free`

This model provides excellent performance for financial recommendations and analysis.