import streamlit as st
import pandas as pd
import requests
import time
import io
from urllib.parse import urlparse
import re

# إعدادات الصفحة
st.set_page_config(
    page_title="TikTok Profile Scraper (Simple)",
    page_icon="🎵",
    layout="wide"
)

def extract_username_from_url(url):
    """استخراج اسم المستخدم من رابط TikTok"""
    try:
        if '@' in url:
            username = url.split('@')[-1].split('?')[0].split('/')[0]
            return username.strip()
        return url
    except:
        return url

def create_sample_data(links):
    """إنشاء بيانات نموذجية للعرض التوضيحي"""
    import random
    
    data_list = []
    for link in links:
        username = extract_username_from_url(link)
        
        # إنشاء بيانات عشوائية للعرض التوضيحي
        followers = random.randint(1000, 500000)
        following = random.randint(100, 2000)
        likes = random.randint(followers * 10, followers * 50)
        
        data_list.append({
            "URL": link,
            "Username": username,
            "Followers": followers,
            "Following": following,
            "Likes": likes,
            "Status": "Demo Data"
        })
    
    return data_list

def main():
    st.title("🎵 TikTok Profile Data Scraper")
    st.markdown("### 📝 Simple Version (Demo Mode)")
    
    st.warning("""
    ⚠️ **Demo Mode Active**
    
    This is a simplified version that generates sample data for demonstration.
    For real data extraction, you need the full version with Selenium support.
    """)
    
    st.markdown("---")
    
    # الشريط الجانبي
    st.sidebar.header("⚙️ Settings")
    
    # خيارات الإدخال
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Use default links", "Upload custom links", "Enter links manually"]
    )
    
    # الروابط الافتراضية
    default_links = [
        "https://www.tiktok.com/@sudanurgentnews2",
        "https://www.tiktok.com/@heartsudan",
        "https://www.tiktok.com/@sawret_desamber",
        "https://www.tiktok.com/@sandymohamed345",
        "https://www.tiktok.com/@jurialhabslab",
        "https://www.tiktok.com/@qatarelmotaheda",
        "https://www.tiktok.com/@qatar_lahza_b_lahza",
        "https://www.tiktok.com/@nohagamal520",
        "https://www.tiktok.com/@amal.badr442",
        "https://www.tiktok.com/@masrelyoum"
    ]
    
    links = []
    
    if input_method == "Use default links":
        links = default_links
        st.info(f"Using {len(links)} default TikTok profile links")
        
    elif input_method == "Upload custom links":
        uploaded_file = st.file_uploader("Upload a text file with links (one per line)", type=['txt'])
        if uploaded_file is not None:
            content = str(uploaded_file.read(), "utf-8")
            links = [line.strip() for line in content.split('\n') if line.strip()]
            st.success(f"Loaded {len(links)} links from file")
            
    elif input_method == "Enter links manually":
        manual_links = st.text_area(
            "Enter TikTok profile links (one per line):",
            height=200,
            placeholder="https://www.tiktok.com/@username1\nhttps://www.tiktok.com/@username2"
        )
        if manual_links:
            links = [line.strip() for line in manual_links.split('\n') if line.strip()]
            st.info(f"Entered {len(links)} links")
    
    # عرض الروابط المحددة
    if links:
        with st.expander("View selected links"):
            for i, link in enumerate(links[:10], 1):
                st.write(f"{i}. {link}")
            if len(links) > 10:
                st.write(f"... and {len(links) - 10} more links")
    
    # زر بدء العملية
    if st.button("🚀 Generate Demo Data", disabled=not links):
        if not links:
            st.error("Please provide TikTok profile links first!")
            return
            
        st.info("Generating demo data... (This is not real scraping)")
        
        # شريط التقدم
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # إنشاء بيانات نموذجية
        data_list = []
        
        for i, link in enumerate(links):
            status_text.text(f"Processing {i+1}/{len(links)}: {link}")
            time.sleep(0.5)  # محاكاة وقت المعالجة
            
            username = extract_username_from_url(link)
            
            # إنشاء بيانات عشوائية
            import random
            followers = random.randint(1000, 500000)
            following = random.randint(100, 2000)
            likes = random.randint(followers * 10, followers * 50)
            
            result = {
                "URL": link,
                "Username": username,
                "Followers": followers,
                "Following": following,
                "Likes": likes,
                "Status": "Demo Data"
            }
            
            data_list.append(result)
            progress_bar.progress((i + 1) / len(links))
        
        # النتائج النهائية
        if data_list:
            df_final = pd.DataFrame(data_list)
            
            st.success("✅ Demo data generated successfully!")
            
            # عرض الإحصائيات
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Profiles", len(df_final))
            with col2:
                st.metric("Demo Data", len(df_final))
            with col3:
                total_followers = df_final['Followers'].sum()
                st.metric("Total Followers", f"{total_followers:,}")
            with col4:
                avg_followers = df_final['Followers'].mean()
                st.metric("Avg Followers", f"{avg_followers:,.0f}")
            
            # عرض البيانات
            st.subheader("📋 Demo Results:")
            st.dataframe(df_final, use_container_width=True)
            
            # تحميل النتائج
            col1, col2 = st.columns(2)
            
            with col1:
                # تحميل Excel
                excel_buffer = io.BytesIO()
                df_final.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Excel File",
                    data=excel_buffer,
                    file_name="tiktok_demo_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                # تحميل CSV
                csv = df_final.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV File",
                    data=csv,
                    file_name="tiktok_demo_data.csv",
                    mime="text/csv"
                )
            
            # رسوم بيانية
            st.subheader("📈 Data Visualization:")
            
            # أعلى 10 حسابات من ناحية المتابعين
            top_accounts = df_final.nlargest(10, 'Followers')[['Username', 'Followers']]
            if not top_accounts.empty:
                st.bar_chart(top_accounts.set_index('Username'))
    
    # معلومات إضافية
    st.markdown("---")
    st.subheader("ℹ️ About This Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **This demo version:**
        - Generates random sample data
        - Shows the interface and functionality
        - Allows testing of download features
        - Demonstrates data visualization
        """)
    
    with col2:
        st.markdown("""
        **For real data extraction:**
        - Deploy the full version with Selenium
        - Use proper Chrome browser setup
        - Handle rate limiting and errors
        - Respect TikTok's terms of service
        """)

    st.info("""
    **💡 Tip**: This demo shows how the interface works. 
    For actual TikTok data scraping, you'll need the full version with proper browser automation setup.
    """)

if __name__ == "__main__":
    main()
