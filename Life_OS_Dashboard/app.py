import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Life-OS Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern SaaS look
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #1e2129;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("📱 Life-OS: Your Digital Wellbeing Command Center")
st.markdown("Monitor your screen time, optimize your habits, and reclaim your real life.")

# Phase 1: Data Ingestion
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("screentime.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please run generate_data.py first.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Phase 2: Command Center UI
st.sidebar.header("Controls 🎛️")

# Filter by Day
unique_dates = df['Date'].dt.date.unique()
sorted_dates = sorted(unique_dates, reverse=True)
selected_date = st.sidebar.selectbox("Select Date to Analyze", sorted_dates)

# Daily Goal Slider (in minutes)
daily_goal = st.sidebar.slider(
    "Daily Screen Time Goal (Minutes)", 
    min_value=60, 
    max_value=600, 
    value=240, 
    step=30
)

# Set Gemini API Key
api_key = st.sidebar.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
if api_key:
    genai.configure(api_key=api_key)

st.sidebar.markdown("---")
st.sidebar.info("The Guilt-Trip Avatar is generated based on your daily screen time performance.")

# Filter Data for Selected Day
day_data = df[df['Date'].dt.date == selected_date]

# Calculate KPIs
total_minutes_today = day_data['Minutes_Used'].sum()
most_used_app = day_data.loc[day_data['Minutes_Used'].idxmax()]['App_Name'] if not day_data.empty else "None"
delta_vs_goal = int(total_minutes_today - daily_goal)

# The KPI Row
st.markdown("### 📊 Daily Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Screen Time",
        value=f"{total_minutes_today} min",
        delta=f"{delta_vs_goal} min over goal" if delta_vs_goal > 0 else f"{abs(delta_vs_goal)} min under goal",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="Most Used App",
        value=most_used_app
    )

with col3:
    st.metric(
        label="Daily Goal Status",
        value=f"{daily_goal} min",
        delta="Goal Missed ⚠️" if total_minutes_today > daily_goal else "Goal Met ✅",
        delta_color="inverse" if total_minutes_today > daily_goal else "normal"
    )

st.markdown("---")

# Visualizations: 14-Day Trends
st.markdown("### 📈 14-Day Screen Time Trend")
trend_data = df.groupby(['Date', 'Category'])['Minutes_Used'].sum().reset_index()
# Pivot the data for the stacked bar chart
pivot_trend = trend_data.pivot(index='Date', columns='Category', values='Minutes_Used').fillna(0)
st.bar_chart(pivot_trend, height=400)

st.markdown("---")

# Phase 3 & 4: AI Integration & The Guilt-Trip Avatar
st.markdown("### 🤖 Personalized AI Life Coach")

if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to unlock AI Coaching and the Guilt-Trip Avatar.")
else:
    with st.spinner("Analyzing your digital habits..."):
        try:
            # 8. The Data Bridge
            # Aggregate the day's usage by category
            category_summary = day_data.groupby('Category')['Minutes_Used'].sum()
            data_string = category_summary.to_json()
            
            # 9. The System Prompt
            prompt = f"""
            You are a brutal-but-fair, highly personalized productivity and lifestyle coach.
            Your goal is to help me reduce my screen time and live a better real-world life.
            
            Here is my screen time data for today by category (in minutes):
            {data_string}
            
            My daily total was {total_minutes_today} minutes. My goal was {daily_goal} minutes.
            
            Please provide a holistic coaching response:
            1. Briefly analyze my performance today.
            2. For any categories where I spent a lot of time (especially Social Media or Entertainment), suggest specific, physical, real-world replacements. DO NOT just tell me to "use my phone less". For example, if I doomscrolled, suggest a specific physical fitness routine, meal prep idea, or book genre.
            3. End with a 1-sentence visual description of what I look like right now based on this data. Format this description exactly like this: "AVATAR_PROMPT: [your description]". Make it dramatic! If I did bad, describe a lazy zombie or couch potato. If I did good, describe a focused warrior or zen master.
            """
            
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            ai_text = response.text
            
            # Extract AVATAR_PROMPT
            avatar_prompt_split = ai_text.split("AVATAR_PROMPT:")
            coaching_advice = avatar_prompt_split[0].strip()
            
            if len(avatar_prompt_split) > 1:
                avatar_prompt = avatar_prompt_split[1].strip().strip('"').strip("'")
            else:
                # Fallback if AI fails to follow exact format
                avatar_prompt = "A person looking at a screen in a dark room" if total_minutes_today > daily_goal else "A productive person smiling outdoors"
            
            # 10. The Output
            if total_minutes_today > daily_goal:
                st.warning("⚠️ High Screen Time Detected")
            else:
                st.success("🌟 Great Job Managing Your Screen Time!")
                
            st.markdown(coaching_advice)
            
            # Phase 4: The Guilt-Trip Avatar
            st.markdown("### 🖼️ Your Guilt-Trip Avatar For Today")
            st.markdown(f"**AI Vision:** *{avatar_prompt}*")
            
            # Use Pollinations AI for image generation (free, no key needed)
            encoded_prompt = urllib.parse.quote(avatar_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true"
            
            st.image(image_url, use_container_width=True, caption="Your Digital Soul Today")

        except Exception as e:
            st.error(f"Error communicating with AI: {str(e)}")
