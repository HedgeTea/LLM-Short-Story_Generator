import streamlit as st
from streamlit_extras.let_it_rain import rain
from openai import OpenAI
import PIL.Image as pimg
import requests

def gen_prompt(prompt:str):
  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role": 'system',
          "content": "You are a bestselling story author. You will take the user's prompt and generate a short story of about 100 words for adults age 20-30."
      },{
          "role":"user",
          "content" : f'{prompt}'
      }],
      max_tokens = 400,
      temperature = 1
  )

  return response.choices[0].message.content

def gen_image(prompt: str,refine_amount: int = 1):
  """
  prompt: the initial story
  refine_amount: amount of times to refine the story
  """
  img_prompt = gen_prompt(prompt)

  for _ in range(1,refine_amount):
    img_prompt = gen_prompt(img_prompt)


  img_response = client.images.generate(
      model="dall-e-2",
      prompt = f"{img_prompt}. Give it in an impressionism style",
      size = "256x256",
      quality = "standard",
      n=1
  )
  img = img_response.data[0].url
  return img
api_key = st.secrets["OPENAI_KEY"]
client = OpenAI(api_key= api_key)


with st.form("Nice Form"):
  st.markdown("**Promptly prompt me now.**")
  p1 = st.text_input("I will promptly give you a story and a picture.", placeholder="There was a cow on the mountain peak.")
  submitted =st.form_submit_button("Boom")
  if submitted:
    rain(emoji="ඞ",font_size = 20, animation_length=1)
    story = gen_prompt(p1)
    st.write(gen_prompt(p1))
    st.image(image = gen_image(story))

  