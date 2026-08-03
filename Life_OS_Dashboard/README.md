# 📱 Life-OS Dashboard

> "Your Digital Wellbeing Command Center"

## 🚀 Overview
Life-OS is a Streamlit dashboard that visualizes your daily screen time data and acts as a personalized, brutal-but-fair productivity and lifestyle coach. Using the Gemini API, it analyzes your digital habits and provides actionable, real-world suggestions to help you reclaim your time.

### 🌟 Features
- **Data Visualization**: Beautiful 14-day trend analysis of your screen time by category.
- **KPI Command Center**: Quick stats on your daily usage, most used apps, and goal tracking.
- **AI Life Coach**: Gemini analyzes your daily data and suggests physical, real-world replacements for digital addictions (e.g., swapping doomscrolling for meal prep).
- **The Guilt-Trip Avatar (Hidden Gem)**: Gemini generates a visual description of your current "digital soul" based on your performance, which is then rendered on the dashboard using AI image generation!

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **AI Integration**: Google Generative AI (Gemini)

## ⚙️ Installation & Setup

1. **Clone the repository** (if applicable) and navigate to the directory:
   ```bash
   cd Life_OS_Dashboard
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Dummy Data**:
   If you don't have a `screentime.csv` file, generate a realistic 14-day dataset by running:
   ```bash
   python generate_data.py
   ```

4. **Environment Variables**:
   You can either add your API key in the `.env` file:
   ```env
   GEMINI_API_KEY="your_actual_api_key"
   ```
   *OR* you can enter it directly in the Streamlit app sidebar when running.

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure
```text
Life_OS_Dashboard/
│
├── app.py                # Main Streamlit application
├── generate_data.py      # Script to generate dummy screentime.csv
├── screentime.csv        # Your screen time dataset
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (git ignored)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## ✅ Pre-Submission Checklist Complete
- [x] Includes `requirements.txt` and hides `.env`.
- [x] Custom, terminal-style `README.md`.
- [x] Streamlit dashboard uses `st.columns` for professional layout.
- [x] AI successfully reads CSV data and gives specific lifestyle advice.
- [x] Guilt-Trip Avatar hidden gem implemented.
- [ ] Ready to be deployed to Streamlit Community Cloud!
