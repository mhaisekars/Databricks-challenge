import streamlit as st
from langchain_utils import get_response

# Page configuration
st.set_page_config(page_title="SaiL - AI Travel Blog Creator", page_icon="✈️")

# Title
st.title("SaiL - AI Travel Blog Creator ! 🚀")

# Personal details section
st.header("Tell us a bit about yourself...")
name = st.text_input("What's your full name?")
email = st.text_input("Your email address?")
trip_title = st.text_input("What's the title of your trip?")
intro = st.text_area("Give a brief intro to your adventure or specify certain tone for the blog.", "Write a few lines about your trip...")

# Number of days in the trip
st.header("How long was your trip?")
num_days = st.number_input("Number of days you were traveling", min_value=1, step=1)

# Instructions for image URLs
st.markdown("""
**Quick Tip:**
- Upload your trip photos to [ImgBB](https://imgbb.com/).
- After uploading, grab the URL for each image and paste it in the fields below. Super easy!
""")

# Day-wise prompts and image URL input
st.subheader("Let's dive into the daily details! 🌅")
daywise_details = []
for i in range(1, num_days + 1):
    st.subheader(f"Day {i} Highlights")
    prompt = st.text_area(f"What happened on Day {i}? Share the fun stuff!", f"Tell us what you did on Day {i}...")

    # Input for image URL
    image_url = st.text_input(f"Got a cool photo for Day {i}? Paste the ImgBB link here!", key=f"image_day_{i}_url")

    # Save day details
    day_details = {
        "day": i,
        "prompt": prompt,
        "image_url": image_url
    }
    daywise_details.append(day_details)

# Submit button
if st.button("Create My Blog"):
    # Process the input data here
    st.success("Your blog is being crafted! ✨ Hang tight...")

    # Display personal details
    #st.write(f"**Author**: {name}")
    #st.write(f"**Email**: {email}")
    #st.write(f"**Trip Title**: {trip_title}")
    #st.write(f"**Introduction**: {intro}")
    
    itinerary = ""
    # Display day-wise blog content
    for day_detail in daywise_details:
        #st.write(f"### Day {day_detail['day']}:")
        #st.write(day_detail["prompt"])
        itinerary =  f"""\n{itinerary}
                        Day {day_detail['day']}:
                            {day_detail["prompt"]}
                    """
        if day_detail["image_url"]:
            #st.image(day_detail["image_url"], caption=f"Day {day_detail['day']} Photo")
            itinerary = itinerary+f""" \n image url to include for the day: {day_detail["image_url"]}"""

    prompt = f"""   Author: {name} 
                    Email: {email}
                    Intro or tone: {intro}
                    Trip Title: {trip_title}
                    Itinerary: {itinerary}
                """
    response = get_response(prompt)
    #st.write(prompt)
    st.html(response)

    # Generate AI-powered content based on the prompt for each day (Placeholder)
    st.info("AI-powered content is on its way... Stay tuned! 🚀")
