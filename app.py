import streamlit as st
import json
import re

st.set_page_config(page_title="Insta Takip Kontrol", page_icon="📸")

st.title("📸 Kim Beni Takip Etmiyor?")
st.write("Instagram JSON dosyalarını yükle, kimlerin seni geri takip etmediğini bul.")

col1, col2 = st.columns(2)
with col1:
    followers_file = st.file_uploader("followers_1.json yükle", type=['json'])
with col2:
    following_file = st.file_uploader("following.json yükle", type=['json'])

def smart_extract(obj):
    """JSON içinde 'title', 'value' veya 'href' olan her şeyi toplar."""
    found = set()
    
    def walk(data):
        if isinstance(data, dict):
            for k, v in data.items():
                if k == 'title' and isinstance(v, str):
                    found.add(v)
                elif k == 'value' and isinstance(v, str):
                    found.add(v)
                elif k == 'href' and isinstance(v, str):
                    match = re.search(r'instagram\.com/(_u/)?([^/?]+)', v)
                    if match:
                        found.add(match.group(2))
                else:
                    walk(v)
        elif isinstance(data, list):
            for item in data:
                walk(item)
                
    walk(obj)
    return found

if followers_file and following_file:
    try:
        f_data = json.load(followers_file)
        fg_data = json.load(following_file)

        followers = smart_extract(f_data)
        following = smart_extract(fg_data)

      
        following = {u for u in following if u and not u.startswith('http')}
        followers = {u for u in followers if u and not u.startswith('http')}

        not_following_back = sorted(list(following - followers))

        st.divider()
        st.write(f"📊 **Sistem Analizi:** {len(followers)} Takipçi | {len(following)} Takip Edilen")

        if not_following_back:
            st.error(f"Seni geri takip etmeyen {len(not_following_back)} kişi bulundu:")
            for user in not_following_back:
                st.markdown(f"- [@{user}](https://instagram.com/{user})")
        else:
            st.success("Tebrikler! Herkes seni geri takip ediyor.")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")