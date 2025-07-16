# Epic-Seven-Auto-Shop-Refresher
A Python automation tool for Epic Seven's shop that automatically refreshes and purchases Covenant and Mystic Bookmarks. Features a user-friendly GUI with budget controls, real-time stats tracking, and multi-window support for efficient bookmark farming.

# Epic Seven Shop Automation

A Python automation tool for Epic Seven that automatically refreshes the shop and purchases Covenant and Mystic Bookmarks. Built with a user-friendly GUI interface for easy control and monitoring.

## Features

- **Automatic Shop Refresh**: Continuously refreshes the shop using sky stones
- **Smart Item Detection**: Uses computer vision to identify Covenant and Mystic Bookmarks
- **Budget Control**: Set sky stone limits to prevent overspending
- **Real-time Statistics**: Track purchases, refreshes, and bookmark counts
- **Multi-window Support**: Automatically detects and remembers Epic Seven windows
- **Flexible Operation**: Run single cycles or continuous loops
- **Safety Features**: Emergency stop with 'Q' key and window validation

## Requirements

- Python 3.7+
- Epic Seven (PC version)
- Windows OS
- 1440p display resolution (optimized for)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/epic-seven-shop-automation.git
cd epic-seven-shop-automation
```

2. Install required dependencies:
```bash
pip install tkinter pyautogui opencv-python numpy pywin32 pillow keyboard
```

3. Add the required image files to the project directory:
   - `shop_cov.png` - Screenshot of Covenant Bookmarks in shop
   - `shop_myst.png` - Screenshot of Mystic Bookmarks in shop

## Usage

1. Launch Epic Seven and navigate to the shop
2. Run the automation:
```bash
python 1440p_main.py
```

3. **First Time Setup**:
   - The app will detect Epic Seven windows automatically
   - If multiple windows are found, select your preferred one
   - Window preference will be saved for future use

4. **Configure Settings**:
   - Set your sky stone budget (default: 300)
   - Each refresh costs 3 sky stones
   - Max refreshes = Budget ÷ 3

5. **Run Automation**:
   - **Run Once**: Single refresh cycle (3 sky stones)
   - **Start Loop**: Continuous automation until budget is reached
   - Press 'Q' during loop to stop early

## How It Works

1. **Window Detection**: Automatically finds and focuses Epic Seven windows
2. **Screen Capture**: Takes screenshots of the shop area for analysis
3. **Image Recognition**: Uses OpenCV template matching to find bookmarks
4. **Purchase Flow**: Clicks buy button → confirms purchase → tracks statistics
5. **Shop Refresh**: Clicks refresh button → confirms → waits for reload
6. **Scroll Check**: Scrolls down to check for items in lower shop area

## Configuration

### Display Settings
- Optimized for 1440p resolution
- Captures 600px wide strip from center of game window
- Adjusts button positions based on window size

### Detection Settings
- Confidence threshold: 89% for item recognition
- Supports multiple template matching methods
- Automatic fallback if primary method fails

### Timing Settings
- 0.1s pause between actions
- 0.5s wait after purchases
- 1.0s wait after shop refresh
- 0.8s wait after scrolling

## Troubleshooting

### Common Issues

**"No Epic Seven window found"**
- Ensure Epic Seven is running and visible
- Try restarting the application
- Check if game window title contains "Epic Seven"

**"Could not load target images"**
- Verify `shop_cov.png` and `shop_myst.png` are in the same folder
- Ensure image files are valid PNG format
- Take new screenshots if items aren't being detected

**Items not being detected**
- Check confidence threshold (default 89%)
- Ensure shop is fully loaded before running
- Verify game is at correct resolution/scaling

**Clicks missing targets**
- Confirm window positions are correct
- Check if game window was moved after setup
- Restart application to recalibrate positions

### Performance Tips

- Close unnecessary applications for better performance
- Ensure stable internet connection for shop loading
- Use windowed mode for better window detection
- Keep game window visible during automation

## Safety Features

- **Failsafe Disabled**: PyAutoGUI failsafe is disabled for uninterrupted operation
- **Emergency Stop**: Press 'Q' during loop to stop safely
- **Window Validation**: Checks if game window still exists before actions
- **Budget Protection**: Automatically stops when sky stone limit is reached

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes only. Use at your own risk and ensure compliance with Epic Seven's terms of service.

## Disclaimer

This tool is not affiliated with Epic Seven or Smilegate. Users are responsible for ensuring their use complies with the game's terms of service. The authors are not responsible for any account actions that may result from using this tool.

## Support

If you encounter issues or have questions:
1. Check the troubleshooting section
2. Review existing issues on GitHub
3. Create a new issue with detailed information about your problem

---

**Note**: This automation tool requires the game to be running and visible. It does not modify game files or memory, only simulates mouse clicks and keyboard input.
