# Epic Seven Shop Automation Bot

An automated bot for Epic Seven's Secret Shop that automatically refreshes and purchases Covenant and Mystic Bookmarks. This tool helps streamline the tedious process of manually refreshing the shop to find and purchase bookmarks.

## Quick Start

1) **You can get the newest version from this google drive link **Version 2.1**: [Download here](https://drive.google.com/file/d/1-_LzeNEE-GQSSlgIt_ALU5zX5jv-pF5p/view?usp=sharing)**
2) **Extract anywhere on your pc**
3) **Run bot/app as admin!!! Due to how smilegate handels their own games you need to allow the same permitions to the bot as well**
4) **Your screen will auto-boarderfullscreen, keep it like that and move to the secret shop**
5) **Enter the amount of skystones (and gold) you would like to spend and AFK**

## Features

- **Automatic Shop Refresh**: Continuously refreshes the secret shop using sky stones
- **Smart Item Detection**: Uses computer vision to identify Covenant and Mystic Bookmarks
- **Dual Resolution Support**: Separate versions optimized for 1080p and 1440p displays
- **Gold Management**: Optional gold threshold to prevent spending below a specified amount
- **Flexible Controls**: Run single cycles or continuous loops with customizable budgets
- **Safety Features**: Emergency stop with 'Q' key, window validation, and error handling
- **User-Friendly GUI**: Clean interface with real-time statistics and status updates

## Version Information

- **Current Version**: 2.0 Beta
- **Version 1**: [Download here](https://drive.google.com/file/d/1VnVWywmsZ36UmtVhqn1e2B_h7gO3cig3/view?usp=sharing)
- **Version 2.1**: [Download here](https://drive.google.com/file/d/1-_LzeNEE-GQSSlgIt_ALU5zX5jv-pF5p/view?usp=sharing)

## How It Works

The bot operates by:

1. **Window Detection**: Automatically finds and focuses the Epic Seven game window
2. **Image Recognition**: Captures screenshots and uses OpenCV template matching to identify bookmarks
3. **Automated Clicking**: Simulates mouse clicks to purchase items and refresh the shop
4. **Shop Cycling**: Refreshes the shop, checks for items, scrolls down, checks again, then repeats

### Technical Details

- Uses **PyAutoGUI** for mouse automation
- **OpenCV** for computer vision and template matching
- **Win32 API** for window management and screen capture
- **Tkinter** for the graphical user interface
- Confidence threshold of 89% for item detection accuracy

## Requirements

### Runtime Requirements
- Windows 10/11
- Epic Seven running in windowed or fullscreen mode
- Minimum 4GB RAM
- .NET Framework (usually pre-installed)

### Development Requirements
- Python 3.8+
- Required packages (see `requirements.txt`):
  - opencv-python==4.11.0.86
  - pyautogui==0.9.54
  - pillow==11.3.0
  - numpy==2.3.1
  - keyboard==0.13.5
  - pywin32==310
  - pyinstaller==6.14.2

## Installation & Building

### Option 1: Use Pre-built Executables
Download the appropriate version for your screen resolution:
- [Version 2 Beta (Latest)](https://drive.google.com/file/d/1-_LzeNEE-GQSSlgIt_ALU5zX5jv-pF5p/view?usp=sharing)
- [Version 1](https://drive.google.com/file/d/1VnVWywmsZ36UmtVhqn1e2B_h7gO3cig3/view?usp=sharing)

### Option 2: Build from Source

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/epic7-shop-automation.git
   cd epic7-shop-automation
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run from Source**
   ```bash
   # For 1080p displays
   python 1080_main.py
   
   # For 1440p displays
   python 1440p_main.py
   ```

4. **Build Executable (Optional)**
   ```bash
   # For 1080p version
   pyinstaller --onefile --windowed --add-data "1080shop_cov.png;." --add-data "1080shop_myst.png;." --add-data "icon.png;." --add-data "icon.ico;." --icon="icon.ico" --version-file version_info_1080p.txt --name "Secret Shop Bot 1080p" 1080_main.py
   
   # For 1440p version
   pyinstaller --onefile --windowed --add-data "shop_cov.png;." --add-data "shop_myst.png;." --add-data "icon.png;." --add-data "icon.ico;." --icon="icon.ico" --version-file version_info_1440p.txt --name "Secret Shop Bot 1440p" 1440p_main.py
   ```

## Usage Instructions

### Setup
1. Start Epic Seven and navigate to the Secret Shop
2. Ensure the game is in fullscreen or windowed mode (not minimized)
3. Launch the appropriate bot version for your screen resolution

### Basic Operation
1. **Single Run**: Click "Run Once" to refresh the shop one time (costs 3 sky stones)
2. **Loop Mode**: 
   - Set your sky stone budget
   - Click "Start Loop" to run continuously
   - Press 'Q' at any time to stop after the current cycle

### Gold Management
- Enable the gold threshold feature to automatically stop when gold drops below 300,000
- Enter your current gold amount for accurate tracking
- The bot deducts 184,000 gold for Covenant Bookmarks and 280,000 for Mystic Bookmarks

### Controls
- **Sky Stones Budget**: Set how many sky stones to spend (3 stones per refresh)
- **Emergency Stop**: Press 'Q' during operation to stop safely
- **Window Selection**: If multiple Epic Seven windows are detected, choose the correct one

## Important Notes

### Safety & Disclaimer
- **Use at your own risk**: This bot automates game interactions which may violate terms of service
- **No warranty**: The developers are not responsible for any account issues
- **Fair play**: Consider the impact on game balance and other players

### Limitations
- Requires Epic Seven to be visible and active
- Works best with stable internet connection
- May need adjustment if game UI changes
- Currently supports Windows only

### Troubleshooting
- **Bot doesn't find Epic Seven**: Ensure the game window title contains "Epic Seven"
- **Items not detected**: Check that template images are in the same folder as the executable
- **Clicks in wrong location**: Verify you're using the correct version for your screen resolution
- **Bot stops unexpectedly**: Check console output for error messages

## File Structure

```
epic7-shop-automation/
├── 1080_main.py              # Main script for 1080p
├── 1440p_main.py             # Main script for 1440p
├── requirements.txt          # Python dependencies
├── version_info_1080p.txt    # Version info for 1080p build
├── version_info_1440p.txt    # Version info for 1440p build
├── 1080shop_cov.png         # Covenant bookmark template (1080p)
├── 1080shop_myst.png        # Mystic bookmark template (1080p)
├── shop_cov.png             # Covenant bookmark template (1440p)
├── shop_myst.png            # Mystic bookmark template (1440p)
└── README.md                # This file
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational purposes. Users are responsible for compliance with Epic Seven's terms of service.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify you're using the correct version for your resolution
3. Ensure all dependencies are installed correctly
4. Check that Epic Seven is running and visible

---

**Developer**: t2ddy  
**Version**: 2.0 Beta  
**Last Updated**: September 2025
