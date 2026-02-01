import streamlit as st
import json

st.set_page_config(page_title="Insta Takip Kontrol", page_icon="📸")

st.title("📸 Kim Beni Takip Etmiyor?")
st.write("Instagram'dan indirdiğin JSON dosyalarını yükle, seni geri takip etmeyenleri anında gör.")

# Dosya yükleme alanları
col1, col2 = st.columns(2)
with col1:
    followers_file = st.file_uploader("followers_1.json yükle", type=['json'])
with col2:
    following_file = st.file_uploader("following.json yükle", type=['json'])

if followers_file and following_file:
    try:
        # JSON verilerini yükle
        followers_data = json.load(followers_file)
        following_data = json.load(following_file)

        # Takipçileri ayıkla (Instagram yapısına göre)
        # Not: JSON yapısı bazen liste bazen dict içinde geliyor, kontrol ekliyoruz.
        followers = set()
        for item in followers_data:
            followers.add(item['string_list_data'][0]['value'])

        # Takip edilenleri ayıkla
        following = set()
        for item in following_data['relationships_following']:
            following.add(item['string_list_data'][0]['value'])

        # Analiz
        not_following_back = list(following - followers)
        not_following_back.sort()

        st.divider()
        
        if not_following_back:
            st.error(f"Seni takip etmeyen {len(not_following_back)} kişi bulundu!")
            
            # Arama kutusu (Arkadaşların listede birini aratabilsin diye)
            search = st.text_input("Listede ara:", placeholder="Kullanıcı adı yazın...")
            
            filtered_list = [user for user in not_following_back if search.lower() in user.lower()]
            
            for user in filtered_list:
                st.markdown(f"- [{user}](https://instagram.com/{user})")
        else:
            st.success("Harika! Herkes seni geri takip ediyor.")

    except Exception as e:
        st.error(f"Dosya işlenirken bir hata oluştu. Lütfen doğru JSON dosyalarını yüklediğinden emin ol. Hata: {e}")

else:
    st.info("Lütfen her iki dosyayı da yukarıya yükle.")