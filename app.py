import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import io

# إعدادات الصفحة
st.set_page_config(
    page_title="TikTok Profile Scraper",
    page_icon="🎵",
    layout="wide"
)

def get_chrome_options():
    """إعداد خيارات Chrome للعمل في بيئة السحابة"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return chrome_options

@st.cache_data
def convert_number(number_str):
    """تحويل النص الرقمي إلى عدد صحيح مع مراعاة K و M"""
    if number_str in [None, '', 'Suspended']:
        return 0
    try:
        if "M" in number_str:
            return int(float(number_str.replace(",", "").replace("M", "")) * 1_000_000)
        if "K" in number_str:
            return int(float(number_str.replace(",", "").replace("K", "")) * 1_000)
        return int(number_str.replace(",", ""))
    except:
        return 0

def extract_data(url, driver):
    """استخراج البيانات من صفحة TikTok"""
    try:
        driver.get(url)
        time.sleep(3)
        
        following = driver.find_element(By.XPATH, "//strong[@data-e2e='following-count']").text
        followers = driver.find_element(By.XPATH, "//strong[@data-e2e='followers-count']").text
        likes = driver.find_element(By.XPATH, "//strong[@data-e2e='likes-count']").text

        return {
            "URL": url,
            "Username": url.split('@')[-1].split('?')[0] if '@' in url else url,
            "Followers": convert_number(followers),
            "Following": convert_number(following),
            "Likes": convert_number(likes),
            "Status": "Success"
        }
    except Exception as e:
        return {
            "URL": url,
            "Username": url.split('@')[-1].split('?')[0] if '@' in url else url,
            "Followers": 0,
            "Following": 0,
            "Likes": 0,
            "Status": f"Error: {str(e)[:50]}"
        }

def main():
    st.title("🎵 TikTok Profile Data Scraper")
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
    if st.button("🚀 Start Scraping", disabled=not links):
        if not links:
            st.error("Please provide TikTok profile links first!")
            return
            
        st.info("Starting the scraping process... This may take a few minutes.")
        
        # شريط التقدم
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.empty()
        
        # تهيئة المتصفح
        try:
            chrome_options = get_chrome_options()
            driver = webdriver.Chrome(options=chrome_options)
            
            data_list = []
            
            for i, link in enumerate(links):
                status_text.text(f"Processing {i+1}/{len(links)}: {link}")
                
                # استخراج البيانات
                result = extract_data(link, driver)
                data_list.append(result)
                
                # تحديث شريط التقدم
                progress_bar.progress((i + 1) / len(links))
                
                # عرض النتائج الجزئية
                if data_list:
                    df = pd.DataFrame(data_list)
                    with results_container.container():
                        st.subheader("📊 Results So Far:")
                        st.dataframe(df, use_container_width=True)
            
            # إغلاق المتصفح
            driver.quit()
            
            # النتائج النهائية
            if data_list:
                df_final = pd.DataFrame(data_list)
                
                st.success("✅ Scraping completed successfully!")
                
                # عرض الإحصائيات
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Profiles", len(df_final))
                with col2:
                    successful = len(df_final[df_final['Status'] == 'Success'])
                    st.metric("Successful", successful)
                with col3:
                    total_followers = df_final['Followers'].sum()
                    st.metric("Total Followers", f"{total_followers:,}")
                with col4:
                    avg_followers = df_final['Followers'].mean()
                    st.metric("Avg Followers", f"{avg_followers:,.0f}")
                
                # عرض البيانات
                st.subheader("📋 Final Results:")
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
                        file_name="tiktok_profiles_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col2:
                    # تحميل CSV
                    csv = df_final.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV File",
                        data=csv,
                        file_name="tiktok_profiles_data.csv",
                        mime="text/csv"
                    )
                
                # رسوم بيانية
                st.subheader("📈 Data Visualization:")
                
                # أعلى 10 حسابات من ناحية المتابعين
                top_accounts = df_final.nlargest(10, 'Followers')[['Username', 'Followers']]
                if not top_accounts.empty:
                    st.bar_chart(top_accounts.set_index('Username'))
                
            else:
                st.error("No data was extracted. Please check your links and try again.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Make sure Chrome/Chromium is installed and accessible.")

if __name__ == "__main__":
    main()
