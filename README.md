# 🎵 TikTok Profile Data Scraper

A Streamlit web application for extracting follower, following, and likes data from TikTok profiles.

## ✨ Features

- **Multiple Input Methods**: Use default links, upload custom files, or enter links manually
- **Real-time Progress**: Live updates and progress tracking during scraping
- **Data Export**: Download results in Excel or CSV format
- **Data Visualization**: Interactive charts showing top accounts
- **User-friendly Interface**: Clean, responsive design with Arabic support

## 🚀 Quick Start

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tiktok-profile-scraper.git
cd tiktok-profile-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Chrome/Chromium browser (required for web scraping)

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser and go to `http://localhost:8501`

### 🌐 Online Deployment

#### Deploy on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Select this repository
5. Deploy!

#### Deploy on Heroku

1. Create a new Heroku app
2. Add the following buildpacks:
   - `heroku/python`
   - `https://github.com/heroku/heroku-buildpack-google-chrome`
   - `https://github.com/heroku/heroku-buildpack-chromedriver`

3. Deploy from GitHub or using Heroku CLI

## 📋 How to Use

1. **Choose Input Method**:
   - Use default TikTok profile links
   - Upload a text file with custom links
   - Enter links manually in the text area

2. **Start Scraping**:
   - Click the "Start Scraping" button
   - Monitor real-time progress
   - View partial results as they're processed

3. **Download Results**:
   - Download data in Excel or CSV format
   - View interactive charts and statistics

## 📊 Data Extracted

For each TikTok profile, the app extracts:
- **Username**: TikTok handle
- **Followers**: Number of followers
- **Following**: Number of accounts following
- **Likes**: Total likes received
- **Status**: Success/Error status

## ⚙️ Configuration

### Browser Options
The app uses headless Chrome with optimized settings for cloud deployment:
- No sandbox mode
- Disabled GPU acceleration
- Custom user agent
- Optimal window size

### Rate Limiting
- Built-in delays between requests
- Error handling for blocked requests
- Retry mechanisms for failed extractions

## 🔧 Technical Details

- **Frontend**: Streamlit
- **Web Scraping**: Selenium WebDriver
- **Data Processing**: Pandas
- **Export Formats**: Excel (XLSX), CSV
- **Browser**: Chrome/Chromium (headless mode)

## 📝 File Structure

```
tiktok-profile-scraper/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Git ignore rules
└── Procfile          # Heroku deployment config
```

## 🚨 Important Notes

### Legal Considerations
- This tool is for educational and research purposes only
- Respect TikTok's Terms of Service and robots.txt
- Implement appropriate delays between requests
- Do not use for commercial purposes without proper authorization

### Rate Limiting
- TikTok may block excessive requests
- Use reasonable delays between scraping sessions
- Consider using proxy servers for large-scale scraping

### Browser Requirements
- Requires Chrome or Chromium browser
- WebDriver automatically managed
- Optimized for cloud deployment environments

## 🐛 Troubleshooting

### Common Issues

1. **Chrome not found**:
   - Install Chrome/Chromium browser
   - Update WebDriver version

2. **Scraping fails**:
   - Check internet connection
   - Verify TikTok profile URLs are valid
   - Try reducing the number of profiles

3. **Deployment issues**:
   - Check buildpack configuration
   - Verify all dependencies are listed
   - Review cloud service logs

### Error Messages
- `WebDriverException`: Browser or driver issues
- `TimeoutException`: Page loading timeout
- `NoSuchElementException`: Page structure changed

## 📈 Future Enhancements

- [ ] Add support for batch processing
- [ ] Implement proxy rotation
- [ ] Add more social media platforms
- [ ] Enhanced data visualization
- [ ] API integration options
- [ ] Scheduled scraping capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for complying with all applicable laws and terms of service. The authors are not responsible for any misuse of this software.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Review TikTok's current page structure

---

Made with ❤️ using Streamlit and Python
