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
        
        
        initial_not_following = sorted(list(following - followers))

        
        if 'clean_list' not in st.session_state or st.session_state.get('last_files') != (followers_file.name + following_file.name):
            st.session_state.clean_list = initial_not_following.copy()
            st.session_state.last_files = followers_file.name + following_file.name

        st.divider()
        
        
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        col_stats1.metric("Takipçi", len(followers))
        col_stats2.metric("Takip Edilen", len(following))
        col_stats3.metric("Geri Takip Etmeyen", len(st.session_state.clean_list), delta_color="inverse")

        if st.session_state.clean_list:
            st.subheader("🕵️ Takip Etmeyenler Listesi")
            st.caption("Dondurulmuş hesapları listeden çıkarmak için ❌ butonuna basabilirsin.")
            
            
            for user in st.session_state.clean_list:
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1:
                    st.markdown(f"**@{user}**")
                with c2:
                    st.link_button("Profili Gör", f"https://instagram.com/{user}")
                with c3:
                    if st.button("❌", key=f"del_{user}"):
                        st.session_state.clean_list.remove(user)
                        st.rerun()
        else:
            st.success("Tebrikler! Herkes seni geri takip ediyor veya liste temizlendi.")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")