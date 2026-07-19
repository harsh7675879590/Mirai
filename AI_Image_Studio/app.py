import streamlit as st
import random
import requests
import urllib.parse

st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="wide")

st.markdown("""
<style>
.main { background: #0E1117; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 AI Image Studio")
st.write("Turn your imagination into stunning artwork in seconds!")

# Sidebar Settings
st.sidebar.title("⚙️ Studio Settings")
art_style = st.sidebar.selectbox(
    "Choose Art Style", 
    ["Realistic", "Anime", "Cyberpunk", "Watercolor", "Oil Painting", "3D Render", "Pixel Art"]
)

# Sliders for Image Dimensions
width = st.sidebar.slider("Image Width", min_value=256, max_value=1920, value=1080, step=64)
height = st.sidebar.slider("Image Height", min_value=256, max_value=1920, value=1080, step=64)

# TASK 3: The "Magic Enhance" Toggle
magic_enhance = st.sidebar.checkbox(" ✨ Enable Magic Enhance")

st.sidebar.divider()
st.sidebar.markdown("🚀 Built with Streamlit & Pollinations.ai")

# Main Interface
prompt_input = st.text_input("💬 Enter your prompt:", "A futuristic city skyline with flying cars")

col1, col2 = st.columns(2)
with col1:
    generate_btn = st.button("🖼️ Generate Image", use_container_width=True, type="primary")

with col2:
    # TASK 4: The "Surprise Me!" Feature
    surprise_btn = st.button(" 🎲 Surprise Me!", use_container_width=True)

# List of 5 crazy, creative prompts
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A giant panda playing a grand piano in a lush forest",
    "A steampunk airship flying through a storm of glowing clouds",
    "A medieval knight fighting a robot dragon"
]

prompt_to_generate = prompt_input
if surprise_btn:
    prompt_to_generate = random.choice(surprise_prompts)
    # Update the UI state with the new prompt so the user can see it
    st.info(f"🎲 Surprise Prompt Selected: **{prompt_to_generate}**")

if generate_btn or surprise_btn:
    if not prompt_to_generate.strip():
        st.warning("⚠ Please enter a prompt first!")
    else:
        # Base full prompt construction
        full_prompt = f"{prompt_to_generate} in {art_style} style"

        # Apply Magic Enhance
        if magic_enhance:
            full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

        # URL encode the prompt to ensure it's a valid URL
        encoded_prompt = urllib.parse.quote(full_prompt)

        with st.spinner("✨ AI is working its magic..."):
            try:
                # TASK 1: The Broken Sliders (URL Parameters)
                # Appending width and height parameters correctly
                url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"
                
                # Fetching the image using requests
                response = requests.get(url)
                
                if response.status_code == 200:
                    image_bytes = response.content
                    
                    st.success("🎉 Image generated successfully!")
                    
                    # Display the generated image
                    st.image(image_bytes, caption=f"{full_prompt} ({width}x{height})", use_container_width=True)
                    
                    # TASK 2: The File Extension Fix
                    # Make the file name dynamic based on the chosen art style
                    formatted_style = art_style.lower().replace(" ", "_")
                    file_name = f"{formatted_style}_image.png"
                    
                    st.download_button(
                        label="📥 Download Image",
                        data=image_bytes,
                        file_name=file_name,
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.error(f"Failed to generate image. Server responded with status code: {response.status_code}")
            
            except Exception as e:
                st.error(f"An error occurred while generating the image: {e}")
