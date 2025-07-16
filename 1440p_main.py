import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import cv2
import numpy as np
import win32gui
import win32ui
import win32con
from PIL import Image
import keyboard
import json
import os

class ShopAutomationUI:
    def __init__(self):
        self.automation = ShopAutomation()
        
        if not self.automation.find_and_select_window():
            messagebox.showerror("Error", "No Epic Seven window found!\nPlease start the game first.")
            return

        self.root = tk.Tk()
        self.root.title("Epic Seven Shop Automation")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="Epic Seven Shop Automation", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready to start")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.purchases_label = ttk.Label(status_frame, text="Purchases: 0")
        self.purchases_label.grid(row=1, column=0, sticky=tk.W)
        
        self.cov_label = ttk.Label(status_frame, text="Covenant: 0")
        self.cov_label.grid(row=2, column=0, sticky=tk.W)
        
        self.myst_label = ttk.Label(status_frame, text="Mystic: 0")
        self.myst_label.grid(row=3, column=0, sticky=tk.W)
        
        self.refreshes_label = ttk.Label(status_frame, text="Refreshes: 0")
        self.refreshes_label.grid(row=4, column=0, sticky=tk.W)
        
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.run_once_btn = ttk.Button(controls_frame, text="Run Once", 
                                      command=self.run_once, width=15)
        self.run_once_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.loop_btn = ttk.Button(controls_frame, text="Start Loop", 
                                  command=self.toggle_loop, width=15)
        self.loop_btn.grid(row=0, column=1)
        
        loop_settings_frame = ttk.LabelFrame(main_frame, text="Loop Settings", padding="10")
        loop_settings_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(loop_settings_frame, text="Sky Stones:").grid(row=0, column=0, sticky=tk.W)
        self.sky_stones_var = tk.StringVar(value="300")
        self.sky_stones_entry = ttk.Entry(loop_settings_frame, textvariable=self.sky_stones_var, width=10)
        self.sky_stones_entry.grid(row=0, column=1, padx=(10, 0))
        
        self.max_refreshes_label = ttk.Label(loop_settings_frame, text="Max Refreshes: 100")
        self.max_refreshes_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        self.sky_stones_var.trace('w', self.update_max_refreshes)
        
        info_frame = ttk.LabelFrame(main_frame, text="Info", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        info_text = "• Run Once: Single refresh (3 sky stones)\n• Loop: Continuous until stopped or budget reached\n• Press 'q' during loop to stop early\n• Window is resizable if needed"
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.is_looping = False
        self.loop_thread = None
        
    def update_max_refreshes(self, *args):
        try:
            sky_stones = int(self.sky_stones_var.get())
            max_refreshes = sky_stones // 3
            self.max_refreshes_label.config(text=f"Max Refreshes: {max_refreshes}")
        except ValueError:
            self.max_refreshes_label.config(text="Max Refreshes: 0")
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def update_counters(self):
        self.purchases_label.config(text=f"Purchases: {self.automation.purchases_made}")
        self.cov_label.config(text=f"Covenant: {self.automation.cov_purchased}")
        self.myst_label.config(text=f"Mystic: {self.automation.myst_purchased}")
        self.refreshes_label.config(text=f"Refreshes: {self.automation.refreshes_done}")
        self.root.update_idletasks()
    
    def run_once(self):
        if not self.initialize_automation():
            return
        
        self.run_once_btn.config(state='disabled')
        self.loop_btn.config(state='disabled')
        
        def run_single():
            try:
                self.automation.sky_stone_budget = 3
                self.automation.max_refreshes = 1
                self.automation.running = True
                self.automation.refreshes_done = 0
                
                self.update_status("Running single cycle...")
                self.automation.run_automation_cycle()
                self.update_counters()
                self.update_status("Single run complete!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error during automation: {e}")
                self.update_status("Error occurred")
            finally:
                self.run_once_btn.config(state='normal')
                self.loop_btn.config(state='normal')
        
        threading.Thread(target=run_single, daemon=True).start()
    
    def toggle_loop(self):
        if not self.is_looping:
            self.start_loop()
        else:
            self.stop_loop()
    
    def start_loop(self):
        if not self.initialize_automation():
            return
        
        try:
            sky_stones = int(self.sky_stones_var.get())
            if sky_stones <= 0:
                messagebox.showerror("Error", "Sky stones must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for sky stones")
            return
        
        self.is_looping = True
        self.loop_btn.config(text="Stop Loop")
        self.run_once_btn.config(state='disabled')
        self.sky_stones_entry.config(state='disabled')
        
        self.automation.sky_stone_budget = sky_stones
        self.automation.max_refreshes = sky_stones // 3
        self.automation.running = True
        self.automation.refreshes_done = 0
        
        self.update_status(f"Looping... Budget: {sky_stones} sky stones")
        
        def run_loop():
            try:
                keyboard_thread = threading.Thread(target=self.keyboard_listener)
                keyboard_thread.daemon = True
                keyboard_thread.start()
                
                while self.automation.running and self.automation.refreshes_done < self.automation.max_refreshes:
                    self.automation.run_automation_cycle()
                    self.update_counters()
                    
                    if self.automation.refreshes_done < self.automation.max_refreshes:
                        self.update_status(f"Waiting... Cycle {self.automation.refreshes_done + 1}/{self.automation.max_refreshes}")
                        time.sleep(.7)
                
                if self.automation.refreshes_done >= self.automation.max_refreshes:
                    self.update_status("Budget reached!")
                else:
                    self.update_status("Loop stopped early")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error during loop: {e}")
                self.update_status("Error occurred")
            finally:
                self.stop_loop()
        
        self.loop_thread = threading.Thread(target=run_loop, daemon=True)
        self.loop_thread.start()
    
    def stop_loop(self):
        self.automation.running = False
        self.is_looping = False
        self.loop_btn.config(text="Start Loop")
        self.run_once_btn.config(state='normal')
        self.sky_stones_entry.config(state='normal')
        if self.automation.running:
            self.update_status("Stopping...")
    
    def keyboard_listener(self):
        keyboard.wait('q')
        if self.is_looping:
            self.automation.running = False
            self.update_status("Stop key pressed - finishing current cycle...")
    
    def initialize_automation(self):
        if not self.automation.validate_window():
            if not self.automation.find_and_select_window():
                messagebox.showerror("Error", "Epic Seven window not found!\nMake sure the game is running.")
                return False
        
        if not self.automation.load_target_images():
            messagebox.showerror("Error", "Could not load target images!\nMake sure shop_cov.png and shop_myst.png are in the same folder.")
            return False
        
        return True
    
    def run(self):
        self.root.mainloop()

class ShopAutomation:
    def __init__(self):
        self.confidence_threshold = 0.89
        self.game_window = None
        self.game_window_title = None
        self.strip_width = 600
        
        self.cov_image = None
        self.myst_image = None
        
        self.running = False
        self.pause_between_actions = 0.1
        self.refresh_button_pos = None
        self.confirm_button_pos = None
        self.buy_button_offset = 900
        self.scroll_amount = -500
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
        self.purchases_made = 0
        self.cov_purchased = 0
        self.myst_purchased = 0
        
        self.sky_stone_budget = 0
        self.max_refreshes = 0
        self.refreshes_done = 0
        
        # Settings file for window preference
        self.settings_file = "epic_seven_automation_settings.json"
    
    def save_window_preference(self):
        """Save the selected window information"""
        if self.game_window and self.game_window_title:
            settings = {
                'window_title': self.game_window_title,
                'window_position': win32gui.GetWindowRect(self.game_window)
            }
            try:
                with open(self.settings_file, 'w') as f:
                    json.dump(settings, f)
                print(f"Saved window preference: {self.game_window_title}")
            except Exception as e:
                print(f"Could not save window preference: {e}")
    
    def load_window_preference(self):
        """Load saved window preference"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Could not load window preference: {e}")
        return None
    
    def find_and_select_window(self):
        def enum_windows_proc(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if "Epic Seven" in window_title:
                    windows.append((hwnd, window_title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_proc, windows)
        
        if not windows:
            return False
        
        saved_pref = self.load_window_preference()
        if saved_pref:
            for hwnd, title in windows:
                if title == saved_pref['window_title']:
                    try:
                        win32gui.GetWindowRect(hwnd)
                        self.game_window = hwnd
                        self.game_window_title = title
                        print(f"Using saved window preference: {title}")
                        self.setup_button_positions()
                        return True
                    except:
                        pass
        
        if len(windows) == 1:
            self.game_window = windows[0][0]
            self.game_window_title = windows[0][1]
            print(f"Found single window: {windows[0][1]}")
            self.setup_button_positions()
            self.save_window_preference()
            return True
        
        selection_root = tk.Tk()
        selection_root.withdraw()
        
        selection_window = tk.Toplevel(selection_root)
        selection_window.title("Select Epic Seven Window")
        selection_window.geometry("500x400")
        
        ttk.Label(selection_window, text="Multiple Epic Seven windows found.\nPlease select one:", 
                 font=("Arial", 12)).pack(pady=10)
        
        selected_hwnd = tk.IntVar()
        selected_title = tk.StringVar()
        
        radio_frame = ttk.Frame(selection_window)
        radio_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        for hwnd, title in windows:
            try:
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                window_info = f"{title}\nPosition: ({left}, {top}) | Size: {right-left}x{bottom-top}"
                
                rb = ttk.Radiobutton(radio_frame, text=window_info, 
                                   variable=selected_hwnd, value=hwnd)
                rb.pack(pady=5, anchor=tk.W)
                
                rb.configure(command=lambda t=title, h=hwnd: [selected_hwnd.set(h), selected_title.set(t)])
            except:
                continue

        if windows:
            selected_hwnd.set(windows[0][0])
            selected_title.set(windows[0][1])
        
        remember_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(selection_window, text="Remember this selection", 
                       variable=remember_var).pack(pady=10)
        
        selection_confirmed = False
        
        def confirm_selection():
            nonlocal selection_confirmed
            selection_confirmed = True
            selection_window.destroy()
        
        def cancel_selection():
            selection_window.destroy()
        
        # Buttons
        button_frame = ttk.Frame(selection_window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Confirm", 
                  command=confirm_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=cancel_selection).pack(side=tk.LEFT, padx=5)
        
        selection_window.update_idletasks()
        x = (selection_window.winfo_screenwidth() // 2) - (selection_window.winfo_width() // 2)
        y = (selection_window.winfo_screenheight() // 2) - (selection_window.winfo_height() // 2)
        selection_window.geometry(f"+{x}+{y}")
        
        selection_window.lift()
        selection_window.attributes('-topmost', True)
        
        selection_root.wait_window(selection_window)
        selection_root.destroy()
        
        if not selection_confirmed:
            return False
        
        self.game_window = selected_hwnd.get()
        self.game_window_title = selected_title.get()
        
        if self.game_window and self.game_window_title:
            print(f"Selected window: {self.game_window_title}")
            self.setup_button_positions()
            
            if remember_var.get():
                self.save_window_preference()
            
            return True
        
        return False
    
    def validate_window(self):
        if self.game_window:
            try:
                win32gui.GetWindowRect(self.game_window)
                return True
            except:
                print("Selected window no longer exists")
                self.game_window = None
                self.game_window_title = None
        return False
    
    def setup_button_positions(self):
        if not self.game_window:
            return
        
        left, top, right, bottom = win32gui.GetWindowRect(self.game_window)
        window_width = right - left
        window_height = bottom - top
        
        print(f"Setting up positions for window at: left={left}, top={top}, width={window_width}, height={window_height}")
        
        confirm_x = left + window_width // 2 + 100
        confirm_y = top + int(window_height * 0.70) - 70
        self.confirm_button_pos = (confirm_x, confirm_y)
        
        refresh_x = left + window_width // 2 - 700  # Changed from -200 to -400 (200 pixels more left)
        refresh_y = top + window_height - 100
        self.refresh_button_pos = (refresh_x, refresh_y)
        
        print(f"Confirm button position: {self.confirm_button_pos}")
        print(f"Refresh button position: {self.refresh_button_pos}")
    
    def focus_game_window(self):
        if self.game_window:
            try:
                if win32gui.IsIconic(self.game_window):
                    win32gui.ShowWindow(self.game_window, win32con.SW_RESTORE)
                
                win32gui.SetForegroundWindow(self.game_window)
                time.sleep(0.2)
                print("Epic Seven window focused")
            except Exception as e:
                print(f"Warning: Could not focus window: {e}")
    
    def find_game_window(self):
        return self.validate_window()
    
    def load_target_images(self):
        try:
            self.cov_image = cv2.imread('shop_cov.png', cv2.IMREAD_COLOR)
            if self.cov_image is None:
                print("Could not load shop_cov.png")
                return False
            
            self.myst_image = cv2.imread('shop_myst.png', cv2.IMREAD_COLOR)
            if self.myst_image is None:
                print("Could not load shop_myst.png")
                return False
            
            print("Target images loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading images: {e}")
            return False
    
    def capture_game_window(self):
        if not self.game_window:
            return None
        
        try:
            left, top, right, bottom = win32gui.GetWindowRect(self.game_window)
            full_width = right - left
            full_height = bottom - top
            
            strip_x = (full_width - self.strip_width) // 2
            
            hwndDC = win32gui.GetWindowDC(self.game_window)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, self.strip_width, full_height)
            saveDC.SelectObject(saveBitMap)
            
            saveDC.BitBlt((0, 0), (self.strip_width, full_height), mfcDC, (strip_x, 0), win32con.SRCCOPY)
            
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            
            img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
            
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.game_window, hwndDC)
            
            return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            print(f"Error capturing window: {e}")
            return None
    
    def find_item_on_screen(self, screen_image, target_image, item_name="item"):
        if target_image is None or screen_image is None:
            return False, 0, (0, 0)
        
        methods = [
            ('TM_CCOEFF_NORMED', cv2.TM_CCOEFF_NORMED),
            ('TM_CCORR_NORMED', cv2.TM_CCORR_NORMED),
            ('TM_SQDIFF_NORMED', cv2.TM_SQDIFF_NORMED)
        ]
        
        best_confidence = 0
        best_location = (0, 0)
        
        for method_name, method in methods:
            result = cv2.matchTemplate(screen_image, target_image, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if method == cv2.TM_SQDIFF_NORMED:
                confidence = 1 - min_val
                location = min_loc
            else:
                confidence = max_val
                location = max_loc
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_location = location
        
        found = best_confidence >= self.confidence_threshold
        
        if found:
            print(f"{item_name} found with confidence: {best_confidence:.3f}")
        
        return found, best_confidence, best_location
    
    def check_and_buy_items(self):
        self.focus_game_window()
        
        screen = self.capture_game_window()
        if screen is None:
            print("Failed to capture screen")
            return False
        
        purchased_something = False
        
        left, top, _, _ = win32gui.GetWindowRect(self.game_window)
        strip_x_offset = (win32gui.GetWindowRect(self.game_window)[2] - left - self.strip_width) // 2
        
        found_cov, conf_cov, loc_cov = self.find_item_on_screen(screen, self.cov_image, "Covenant Bookmarks")
        if found_cov:
            h, w = self.cov_image.shape[:2]
            click_x = left + strip_x_offset + loc_cov[0] + w + self.buy_button_offset
            click_y = top + loc_cov[1] + h // 2
            
            print(f"Buying Covenant at position: ({click_x}, {click_y})")
            self.click_and_confirm(click_x, click_y, "Covenant Bookmarks")
            self.cov_purchased += 1
            purchased_something = True
            time.sleep(0.5)
        
        found_myst, conf_myst, loc_myst = self.find_item_on_screen(screen, self.myst_image, "Mystic Bookmarks")
        if found_myst:
            h, w = self.myst_image.shape[:2]
            click_x = left + strip_x_offset + loc_myst[0] + w + self.buy_button_offset
            click_y = top + loc_myst[1] + h // 2
            
            print(f"Buying Mystic at position: ({click_x}, {click_y})")
            self.click_and_confirm(click_x, click_y, "Mystic Bookmarks")
            self.myst_purchased += 1
            purchased_something = True
        
        return purchased_something
    
    def click_and_confirm(self, x, y, item_name):
        self.focus_game_window()
        
        print(f"Moving to buy button: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=0)
        
        time.sleep(self.pause_between_actions)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.5)
        
        confirm_x = self.confirm_button_pos[0]
        confirm_y = self.confirm_button_pos[1] + 100
        print(f"Moving to confirm button: ({confirm_x}, {confirm_y})")
        pyautogui.moveTo(confirm_x, confirm_y, duration=0)
        
        time.sleep(self.pause_between_actions)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.click()
        
        self.purchases_made += 1
        print(f"Purchased {item_name}! Total purchases: {self.purchases_made}")
        time.sleep(1.0)
    
    def refresh_shop(self):
        self.focus_game_window()
        
        print(f"Refreshing shop at position: {self.refresh_button_pos}")
        pyautogui.moveTo(self.refresh_button_pos[0], self.refresh_button_pos[1], duration=0)
        time.sleep(self.pause_between_actions)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.5)
        
        # Now click the confirm button to actually refresh
        print(f"Confirming refresh at position: {self.confirm_button_pos}")
        pyautogui.moveTo(self.confirm_button_pos[0], self.confirm_button_pos[1], duration=0)
        time.sleep(self.pause_between_actions)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(1.0)
        
        self.refreshes_done += 1
    
    def scroll_shop(self):
        self.focus_game_window()
        
        if self.confirm_button_pos:
            print(f"Scrolling at position: {self.confirm_button_pos}")
            pyautogui.moveTo(self.confirm_button_pos[0], self.confirm_button_pos[1], duration=0)
            time.sleep(0.1)
        pyautogui.scroll(self.scroll_amount)
        time.sleep(0.8)
    
    def run_automation_cycle(self):
        print(f"\n=== Starting cycle {self.refreshes_done + 1} ===")
        self.focus_game_window()
        
        self.refresh_shop()
        self.check_and_buy_items()
        self.scroll_shop()
        self.check_and_buy_items()
        print(f"=== Cycle {self.refreshes_done} complete ===")

def main():
    app = ShopAutomationUI()
    if hasattr(app, 'root'):
        app.run()

if __name__ == "__main__":
    main()