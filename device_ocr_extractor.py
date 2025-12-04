"""
Technohull Marine Device Serial Number Extractor - OCR Version
Extract serial numbers from screenshots of device lists

This program uses EasyOCR to read device information from images
and extract product names and serial numbers.
NO TESSERACT REQUIRED!
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import easyocr
import re
from pathlib import Path
from datetime import datetime
import json
import threading


class DeviceExtractorGUI:
    """GUI application for extracting device serials from images"""

    def _on_mousewheel(self, event):
        # Windows uses event.delta, positive/negative for up/down
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.main_canvas = None  # Placeholder for main_canvas
        self.root.title("Technohull Marine Device Serial Number Extractor")
        # Start maximized
        self.root.state('zoomed')  # Windows maximized window
        self.image_path = None
        self.image_paths = []
        self.extracted_devices = []
        self.reader = None
        self.is_loading = False
        self.setup_ui()
        
    def add_manual_engine(self):
        """Add engine manually from dropdown"""
        engine_type = self.engine_dropdown_add.get()
        model_number = self.engine_model_entry.get().strip()
        serial_number = self.engine_serial_entry.get().strip()
        if not engine_type:
            messagebox.showwarning("Warning", "Please select an engine type from dropdown")
            return
        if not model_number:
            messagebox.showwarning("Warning", "Please enter a model number")
            return
        if not serial_number:
            messagebox.showwarning("Warning", "Please enter a serial number")
            return
        # Add to tree
        item_id = self.tree.insert("", tk.END, values=("☑", engine_type, model_number, serial_number))
        self.device_selected[item_id] = True
        self.device_types[item_id] = engine_type
        # Clear inputs
        self.engine_dropdown_add.set("")
        self.engine_model_entry.delete(0, tk.END)
        self.engine_serial_entry.delete(0, tk.END)
        self.export_btn.config(state=tk.NORMAL)
        self.status_label.config(text=f"✓ Added {engine_type}")

    def setup_ui(self):
        """Setup the user interface"""
        
        # Dark mode colors
        # Black-friendly theme
        self.bg_dark = "#111111"  # true black
        self.bg_medium = "#181818"  # near black
        self.bg_light = "#222222"  # dark gray
        self.fg_primary = "#f8f8f8"  # off-white
        self.fg_secondary = "#888888"  # muted gray
        self.accent_blue = "#1a8cff"  # vivid blue
        self.accent_green = "#14cc60"
        self.accent_red = "#e74c3c"
        self.accent_orange = "#ff8c42"
        self.border_radius = 18  # px for more rounded corners
        
        # Set dark background for root
        self.root.configure(bg=self.bg_dark)
        
        # Set window icon if available
        try:
            icon_path = Path(__file__).parent / "assets" / "app_icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_medium, height=80, highlightbackground=self.bg_light, highlightthickness=1)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        title_frame.configure(borderwidth=0)
        
        # Try to load logo
        try:
            logo_path = Path(__file__).parent / "assets" / "app_logo.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
                
                logo_label = tk.Label(title_frame, image=logo_photo, bg=self.bg_medium)
                logo_label.image = logo_photo  # Keep reference
                logo_label.pack(side=tk.LEFT, padx=15)
        except:
            pass
        
        title_label = tk.Label(
            title_frame,
            text="Technohull Marine Device Serial Number Extractor",
            font=("Arial", 16, "bold"),
            bg=self.bg_medium,
            fg=self.fg_primary,
            borderwidth=0,
            highlightthickness=0
        )
        title_label.pack(side=tk.LEFT, pady=20)
        
        # Main container with vertical scrollbar
        # Layout fix: use a container frame for canvas and scrollbar
        container = tk.Frame(self.root, bg=self.bg_dark)
        container.pack(fill=tk.BOTH, expand=True)
        main_canvas = tk.Canvas(container, bg=self.bg_dark, highlightbackground=self.bg_light, highlightthickness=1, borderwidth=0)
        main_scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=main_canvas.yview)
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_frame = tk.Frame(main_canvas, padx=20, pady=20, bg=self.bg_dark)
        main_window = main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        def _on_frame_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            main_canvas.itemconfig(main_window, width=main_canvas.winfo_width())
        main_frame.bind("<Configure>", _on_frame_configure)
        def _on_canvas_configure(event):
            main_canvas.itemconfig(main_window, width=event.width)
        main_canvas.bind("<Configure>", _on_canvas_configure)
        
        
        # Vessel information inputs
        vessel_info_frame = tk.LabelFrame(
            main_frame,
            text="Vessel Information",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bg=self.bg_medium,
            fg=self.fg_primary,
            borderwidth=0,
            highlightthickness=0
        )
        vessel_info_frame.pack(pady=10, fill=tk.X)
        
        # Vessel Model
        model_frame = tk.Frame(vessel_info_frame, bg=self.bg_medium, borderwidth=0, highlightthickness=0)
        model_frame.pack(fill=tk.X, pady=5)
        
        model_label = tk.Label(
            model_frame,
            text="Model:",
            font=("Arial", 10),
            width=15,
            anchor=tk.W,
            bg=self.bg_medium,
            fg=self.fg_primary
        )
        model_label.pack(side=tk.LEFT, padx=5)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TCombobox",
                        fieldbackground="#181818",
                        background="#181818",
                        foreground=self.fg_primary,
                        font=("Arial", 12, "bold"))
        self.vessel_model_entry = ttk.Combobox(
            model_frame,
            font=("Arial", 12, "bold"),
            values=[
                "GT9",
                "GTX",
                "ALPHA 40",
                "ALPHA 45",
                "ALPHA 50",
                "OMEGA 47",
                "XPD",
                "GT7",
                "GS38"
            ],
            width=38,
            style="Dark.TCombobox"
        )
        self.vessel_model_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.vessel_model_entry.set("Select model...")
        self.vessel_model_entry.config(foreground=self.fg_primary)
        
        # Vessel Name
        name_frame = tk.Frame(vessel_info_frame, bg=self.bg_medium, borderwidth=0, highlightthickness=0)
        name_frame.pack(fill=tk.X, pady=5)
        
        name_label = tk.Label(
            name_frame,
            text="Name:",
            font=("Arial", 10),
            width=15,
            anchor=tk.W,
            bg=self.bg_medium,
            fg=self.fg_primary
        )
        name_label.pack(side=tk.LEFT, padx=5)
        
        self.vessel_name_entry = tk.Entry(
            name_frame,
            font=("Arial", 12, "bold"),
            width=40,
            bg="#222222",
            fg=self.fg_primary,
            insertbackground=self.fg_primary,
            relief=tk.FLAT
        )
        self.vessel_name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.vessel_name_entry.insert(0, "e.g., Sea Explorer")
        self.vessel_name_entry.config(fg=self.fg_secondary)
        
        # SAP Number
        sap_frame = tk.Frame(vessel_info_frame, bg=self.bg_medium, borderwidth=0, highlightthickness=0)
        sap_frame.pack(fill=tk.X, pady=5)
        
        sap_label = tk.Label(
            sap_frame,
            text="SAP:",
            font=("Arial", 10),
            width=15,
            anchor=tk.W,
            bg=self.bg_medium,
            fg=self.fg_primary
        )
        sap_label.pack(side=tk.LEFT, padx=5)
        
        self.sap_entry = tk.Entry(
            sap_frame,
            font=("Arial", 12, "bold"),
            width=40,
            bg="#222222",
            fg=self.fg_primary,
            insertbackground=self.fg_primary,
            relief=tk.FLAT
        )
        self.sap_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.sap_entry.insert(0, "e.g., 9100967")
        self.sap_entry.config(fg=self.fg_secondary)
        
        # Bind events to clear placeholders
        self.vessel_model_entry.bind("<FocusIn>", lambda e: self._clear_combobox_placeholder(self.vessel_model_entry, "Select model..."))
        self.vessel_model_entry.bind("<<ComboboxSelected>>", lambda e: self._on_combobox_selected(self.vessel_model_entry))
        
        self.vessel_name_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(self.vessel_name_entry, "e.g., Sea Explorer"))
        self.vessel_name_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(self.vessel_name_entry, "e.g., Sea Explorer"))
        
        self.sap_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(self.sap_entry, "e.g., 9100967"))
        self.sap_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(self.sap_entry, "e.g., 9100967"))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.bg_dark, borderwidth=0, highlightthickness=0)
        button_frame.pack(pady=10)
        
        self.upload_btn = tk.Button(
            button_frame,
            text="📁 Upload Images",
            command=self.upload_image,
            font=("Arial", 11, "bold"),
            bg=self.accent_blue,
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
            activebackground="#0a5a5d",
            borderwidth=0
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.extract_btn = tk.Button(
            button_frame,
            text="🔍 Extract Devices & Engines",
            command=self.extract_devices,
            font=("Arial", 11, "bold"),
            bg=self.accent_blue,
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
            state=tk.DISABLED,
            activebackground="#0a5a5d",
            borderwidth=0,
            disabledforeground="#7f8c8d"
        )
        self.extract_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = tk.Button(
            button_frame,
            text="💾 Export to TXT",
            command=self.export_results,
            font=("Arial", 11, "bold"),
            bg=self.accent_blue,
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
            state=tk.DISABLED,
            activebackground="#0a5a5d",
            borderwidth=0,
            disabledforeground="#7f8c8d"
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Image preview frame
        preview_frame = tk.LabelFrame(
            main_frame,
            text="Image Preview",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bg=self.bg_medium,
            fg=self.fg_primary,
            borderwidth=0,
            highlightthickness=0
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)


        # Main image preview
        self.image_label = tk.Label(
            preview_frame,
            text="No image loaded",
            font=("Arial", 10),
            fg=self.fg_secondary,
            bg=self.bg_medium,
            borderwidth=0,
            highlightthickness=0
        )
        self.image_label.pack(pady=(0, 5))

        # Always visible enlarge button (below preview frame)
        self.enlarge_btn = tk.Button(
            main_frame,
            text="🔍 Enlarge Image",
            command=self.enlarge_image,
            font=("Arial", 10, "bold"),
            bg=self.accent_blue,
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=0,
            activebackground="#0a5a5d",
            highlightthickness=0
        )
        self.enlarge_btn.pack(pady=(0, 10))

        # Thumbnails frame
        self.thumbnails_frame = tk.Frame(preview_frame, bg=self.bg_medium, borderwidth=0, highlightthickness=0)
        self.thumbnails_frame.pack(fill=tk.X, pady=5)
        self.thumbnail_images = []  # Store references
        self.thumbnail_buttons = []
        self.current_image_index = 0
        
        # Results frame
        results_frame = tk.LabelFrame(
            main_frame,
            text="Extracted Items (Devices & Engines) - Select items to export",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bg=self.bg_medium,
            fg=self.fg_primary,
            borderwidth=0,
            highlightthickness=0
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add device dropdown and button - for manual additions
        add_device_frame = tk.Frame(results_frame, bg=self.bg_medium, borderwidth=0, highlightthickness=0)
        add_device_frame.pack(fill=tk.X, pady=5)
        tk.Label(add_device_frame, text="Add Device Manually:", font=("Arial", 9, "bold"), bg=self.bg_medium, fg=self.fg_primary).pack(side=tk.LEFT, padx=5)
        self.device_dropdown_add = ttk.Combobox(
            add_device_frame,
            values=[
                "AXIOM 2 PRO 9",
                "AXIOM 2 PRO 12",
                "AXIOM 2 PRO 16",
                "GMDSS",
                "RAYMARINE AIS 700",
                "RADAR QUANTUM 2",
                "THERMAL CAMERA",
                "RAYMARINE RAY53 VHF",
                "RAYMARINE RS 150"
            ],
            state="readonly",
            width=25,
            font=("Arial", 9)
        )
        self.device_dropdown_add.pack(side=tk.LEFT, padx=5)
        # Product code entry
        tk.Label(add_device_frame, text="Code:", font=("Arial", 9), bg=self.bg_medium, fg=self.fg_primary).pack(side=tk.LEFT, padx=5)
        self.product_code_entry = tk.Entry(add_device_frame, width=10, font=("Arial", 9), bg=self.bg_light, fg=self.fg_primary, insertbackground=self.fg_primary)
        self.product_code_entry.pack(side=tk.LEFT, padx=5)
        # Serial number entry
        tk.Label(add_device_frame, text="Serial:", font=("Arial", 9), bg=self.bg_medium, fg=self.fg_primary).pack(side=tk.LEFT, padx=5)
        self.serial_entry = tk.Entry(add_device_frame, width=15, font=("Arial", 9), bg=self.bg_light, fg=self.fg_primary, insertbackground=self.fg_primary)
        self.serial_entry.pack(side=tk.LEFT, padx=5)
        # Add button
        add_btn = tk.Button(
            add_device_frame,
            text="➕ Add",
            command=self.add_manual_device,
            font=("Arial", 9),
            bg=self.accent_blue,
            fg="white",
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=0,
            activebackground="#0a5a5d"
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        # Edit button
        edit_btn = tk.Button(
            add_device_frame,
            text="✏️ Edit Selected",
            command=self.edit_selected_device,
            font=("Arial", 9),
            bg=self.accent_blue,
            fg="white",
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=0,
            activebackground="#0a5a5d"
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        # Remove button
        remove_btn = tk.Button(
            add_device_frame,
            text="➖ Remove Selected",
            command=self.remove_selected_device,
            font=("Arial", 9),
            bg=self.accent_blue,
            fg="white",
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=0,
            activebackground="#0a5a5d"
        )
        remove_btn.pack(side=tk.LEFT, padx=5)

        # Engine section for manual addition
        engine_frame = tk.Frame(results_frame, bg=self.bg_medium, borderwidth=0, highlightthickness=0)
        engine_frame.pack(fill=tk.X, pady=5)
        tk.Label(engine_frame, text="Add Engine Manually:", font=("Arial", 9, "bold"), bg=self.bg_medium, fg=self.fg_primary).pack(side=tk.LEFT, padx=5)
        self.engine_dropdown_add = ttk.Combobox(
            engine_frame,
            values=[
                "300 MERCURY NO ELECTRIC STEERING",
                "350 V10 MERCURY",
                "400 V10 MERCURY",
                "400R V10 MERCURY",
                "600 MERCURY",
                "300 YAMAHA",
                "350 YAMAHA",
                "370 YANMAR"
            ],
            state="readonly",
            width=30,
            font=("Arial", 9)
        )
        self.engine_dropdown_add.pack(side=tk.LEFT, padx=5)
        tk.Label(engine_frame, text="Model Number:", font=("Arial", 9), bg=self.bg_medium, fg=self.fg_primary).pack(side=tk.LEFT, padx=5)
        self.engine_model_entry = tk.Entry(engine_frame, width=12, font=("Arial", 9), bg=self.bg_light, fg=self.fg_primary, insertbackground=self.fg_primary)
        self.engine_model_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(engine_frame, text="Serial Number:", font=("Arial", 9), bg=self.bg_medium, fg=self.fg_primary).pack(side=tk.LEFT, padx=5)
        self.engine_serial_entry = tk.Entry(engine_frame, width=15, font=("Arial", 9), bg=self.bg_light, fg=self.fg_primary, insertbackground=self.fg_primary)
        self.engine_serial_entry.pack(side=tk.LEFT, padx=5)
        engine_add_btn = tk.Button(
            engine_frame,
            text="➕ Add Engine",
            command=self.add_manual_engine,
            font=("Arial", 9),
            bg=self.accent_blue,
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            borderwidth=0,
            activebackground="#0a5a5d"
        )
        engine_add_btn.pack(side=tk.LEFT, padx=5)
        
        # Create treeview with device type dropdown in each row
        columns = ("Select", "DeviceType", "Code", "Serial")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=self.bg_light,
                        foreground=self.fg_primary,
                        fieldbackground=self.bg_light,
                        borderwidth=0,
                        rowheight=28,
                        font=("Arial", 10))
        style.map("Treeview",
                  background=[('selected', self.accent_blue)])
        style.configure("Treeview.Heading",
                        background=self.bg_medium,
                        foreground=self.fg_primary,
                        font=("Arial", 10, "bold"),
                        borderwidth=0)
        self.tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=10
        )
        
        self.tree.heading("Select", text="✓")
        self.tree.heading("DeviceType", text="Device Type (Double-click to change)")
        self.tree.heading("Code", text="Code")
        self.tree.heading("Serial", text="Serial Number")
        
        self.tree.column("Select", width=50, minwidth=50)
        self.tree.column("DeviceType", width=500, minwidth=200)
        self.tree.column("Code", width=150, minwidth=100)
        self.tree.column("Serial", width=200, minwidth=150)
        
        # Bind click event for checkboxes and device type selection
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", self.on_device_type_double_click)
        
        # Store checkbox states and device type dropdowns
        self.device_selected = {}
        self.device_types = {}  # Store device type for each item
        
        # Available device types
        self.available_device_types = [
            "AXIOM 2 PRO 9",
            "AXIOM 2 PRO 12",
            "AXIOM 2 PRO 16",
            "GMDSS",
            "RAYMARINE AIS 700",
            "RADAR QUANTUM 2",
            "THERMAL CAMERA",
            "RAYMARINE RAY53 VHF",
            "RAYMARINE RS 150",
            "ENGINE"
        ]
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9),
            bg=self.bg_light,
            fg=self.fg_primary,
            anchor=tk.W,
            padx=10,
            borderwidth=0,
            highlightthickness=0
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _clear_placeholder(self, entry_widget, placeholder_text):
        """Clear placeholder text when entry is focused"""
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, tk.END)
            entry_widget.config(fg=self.fg_primary)
    
    def _restore_placeholder(self, entry_widget, placeholder_text):
        """Restore placeholder if entry is empty"""
        if not entry_widget.get():
            entry_widget.insert(0, placeholder_text)
            entry_widget.config(fg=self.fg_secondary)
    
    def _clear_combobox_placeholder(self, combobox_widget, placeholder_text):
        """Clear placeholder text when combobox is focused"""
        if combobox_widget.get() == placeholder_text:
            combobox_widget.set("")
            combobox_widget.config(foreground=self.fg_primary)
    
    def _on_combobox_selected(self, combobox_widget):
        """Handle combobox selection"""
        combobox_widget.config(foreground=self.fg_primary)
        
    def upload_image(self):
        """Handle image upload (supports multiple files)"""
        file_paths = filedialog.askopenfilenames(
            title="Select One or More Screenshots",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )

        if file_paths:
            self.image_paths = list(file_paths)
            self.current_image_index = 0
            # Backward compatibility for single image usage
            self.image_path = self.image_paths[0]
            # Display the first image
            self.display_image(self.image_paths[0])
            self.extract_btn.config(state=tk.NORMAL)
            loaded_count = len(self.image_paths)
            if loaded_count == 1:
                self.status_label.config(text=f"Loaded 1 image: {Path(self.image_paths[0]).name}")
            else:
                self.status_label.config(text=f"Loaded {loaded_count} images (showing first)")
            self.show_thumbnails()
            
    def display_image(self, image_path):
        """Display the uploaded image"""
        try:
            # Load and resize image
            image = Image.open(image_path)
            # Calculate size to fit in preview (max 800x250)
            max_width = 800
            max_height = 250
            ratio = min(max_width/image.width, max_height/image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def show_thumbnails(self):
        """Show thumbnails for all selected images"""
        # Clear previous thumbnails
        for btn in self.thumbnail_buttons:
            btn.destroy()
        self.thumbnail_buttons.clear()
        self.thumbnail_images.clear()
        # Create thumbnails
        thumb_size = (60, 40)
        for idx, img_path in enumerate(self.image_paths):
            try:
                img = Image.open(img_path)
                img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
                thumb = ImageTk.PhotoImage(img)
                self.thumbnail_images.append(thumb)
                btn = tk.Label(
                    self.thumbnails_frame,
                    image=thumb,
                    bg=self.bg_medium,
                    cursor="hand2",
                    borderwidth=0,
                    highlightthickness=0,
                    relief=tk.FLAT
                )
                # Custom rounded border using a frame
                border_frame = tk.Frame(self.thumbnails_frame, bg=self.bg_medium, borderwidth=0, highlightthickness=0)
                btn.pack(in_=border_frame, padx=0, pady=0)
                border_frame.pack(side=tk.LEFT, padx=4, pady=2)
                # Draw highlight border for selected
                if idx == self.current_image_index:
                    border_frame.config(bg=self.accent_blue)
                else:
                    border_frame.config(bg=self.bg_medium)
                btn.bind("<Button-1>", lambda e, i=idx: self.on_thumbnail_click(i))
                self.thumbnail_buttons.append(border_frame)
            except Exception:
                continue

    def on_thumbnail_click(self, idx):
        """Change main preview to selected thumbnail and update highlight"""
        self.current_image_index = idx
        self.image_path = self.image_paths[idx]
        self.display_image(self.image_path)
        # Redraw thumbnails to update highlight
        self.show_thumbnails()

    def enlarge_image(self):
        """Open the current image in a maximized popup window"""
        if not self.image_paths:
            return
        img_path = self.image_paths[self.current_image_index]
        try:
            img = Image.open(img_path)
            popup = tk.Toplevel(self.root)
            popup.title(f"Enlarged View - {Path(img_path).name}")
            popup.configure(bg=self.bg_dark)
            # Maximize window
            popup.state('zoomed')
            # Resize image to fit screen
            screen_w = popup.winfo_screenwidth()
            screen_h = popup.winfo_screenheight()
            ratio = min(screen_w/img.width, screen_h/img.height, 1.0)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(popup, image=photo, bg=self.bg_dark)
            label.image = photo
            label.pack(expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enlarge image: {e}")
            
    def extract_devices(self):
        """Extract device and engine information from image(s) using OCR"""
        if not self.image_paths:
            messagebox.showwarning("Warning", "Please upload one or more images first")
            return
        
        if self.is_loading:
            messagebox.showinfo("Please Wait", "OCR engine is still loading...")
            return
        
        # Disable buttons during extraction
        self.extract_btn.config(state=tk.DISABLED)
        self.upload_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Extracting devices... This may take 10-30 seconds")
        self.root.update()
        
        # Run extraction in a separate thread to keep GUI responsive
        thread = threading.Thread(target=self._perform_extraction, daemon=True)
        thread.start()
    
    def _perform_extraction(self):
        """Perform the actual OCR extraction (runs in background thread)"""
        try:
            # Initialize reader if needed (first time only)
            if self.reader is None:
                self.root.after(0, lambda: self.status_label.config(
                    text="First time: Loading OCR engine... (10-30 seconds)"
                ))
                self.reader = easyocr.Reader(['en'], gpu=False)
            
            self.root.after(0, lambda: self.status_label.config(
                text="Reading image(s)... Please wait"
            ))

            aggregated_devices = []
            for idx, img_path in enumerate(self.image_paths):
                # Perform OCR per image
                results = self.reader.readtext(img_path)
                text_lines = [detection[1] for detection in results]
                text = '\n'.join(text_lines)
                # Parse the text to extract devices and engine serials
                parsed = self.parse_device_text(text)
                aggregated_devices.extend(parsed)

            self.extracted_devices = aggregated_devices
            
            # Update GUI in main thread
            self.root.after(0, self._update_results)
                
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="✗ Extraction failed"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to extract devices: {e}"))
            self.root.after(0, lambda: self.extract_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.upload_btn.config(state=tk.NORMAL))
    
    def _update_results(self):
        """Update the GUI with extraction results"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.device_selected.clear()
        self.device_types.clear()
        
        # Add extracted devices to treeview with checkboxes
        if self.extracted_devices:
            for idx, device in enumerate(self.extracted_devices):
                # Parse product to separate name and code
                product_full = device['product']
                # Try to extract product code
                code_match = re.search(r'\b([EV]\d{5}|MS-[A-Z0-9]+|\d{1,3}L\d{4})\b', product_full)
                
                if code_match:
                    code = code_match.group(1)
                    product_name = product_full.replace(code, '').strip()
                else:
                    product_name = product_full
                    code = ""
                
                # Try to auto-match device type from extracted name
                device_type = self.auto_match_device_type(product_name)
                if not device_type:
                    device_type = "[Click to select device type]"
                
                item_id = self.tree.insert("", tk.END, values=("☐", device_type, code, device['serial']))
                self.device_selected[item_id] = False
                self.device_types[item_id] = device_type
            
            self.export_btn.config(state=tk.NORMAL)
            self.status_label.config(
                text=f"✓ Extracted {len(self.extracted_devices)} items - Double-click device type to change"
            )
            messagebox.showinfo(
                "Success",
                f"Successfully extracted {len(self.extracted_devices)} items!\n\nDouble-click on 'Device Type' column to assign device types.\nCheck the boxes for items to export."
            )
        else:
            self.status_label.config(text="⚠ No devices or engines found in image(s)")
            messagebox.showwarning(
                "Warning",
                "Could not find any devices or engine serials in the image(s).\n\nTips:\n- Ensure image is clear and in focus\n- Try a higher resolution screenshot\n- Check that text is visible"
            )
        
        # Re-enable buttons
        self.extract_btn.config(state=tk.NORMAL)
        self.upload_btn.config(state=tk.NORMAL)
    
    def auto_match_device_type(self, product_name):
        """Try to automatically match extracted product name to device type"""
        product_upper = product_name.upper()
        
        # Match patterns
        if "AXIOM" in product_upper and "9" in product_upper:
            return "AXIOM 2 PRO 9"
        elif "AXIOM" in product_upper and "12" in product_upper:
            return "AXIOM 2 PRO 12"
        elif "AXIOM" in product_upper and "16" in product_upper:
            return "AXIOM 2 PRO 16"
        elif "GMDSS" in product_upper or "12L" in product_name:
            return "GMDSS"
        elif "AIS" in product_upper and "700" in product_upper:
            return "RAYMARINE AIS 700"
        elif "QUANTUM" in product_upper or ("RADAR" in product_upper and "2" in product_upper):
            return "RADAR QUANTUM 2"
        elif "THERMAL" in product_upper or "CAMERA" in product_upper:
            return "THERMAL CAMERA"
        elif "RAY53" in product_upper or ("VHF" in product_upper and "53" in product_upper):
            return "RAYMARINE RAY53 VHF"
        elif "RS" in product_upper and "150" in product_upper:
            return "RAYMARINE RS 150"
        elif "ENGINE" in product_upper:
            return "ENGINE"
        
        return None
    
    def on_tree_click(self, event):
        """Handle clicks on tree items to toggle checkboxes"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            # If clicked on checkbox column
            if item and column == "#1":  # Select column
                # Toggle selection
                current_state = self.device_selected.get(item, False)
                new_state = not current_state
                self.device_selected[item] = new_state
                
                # Update checkbox display
                values = list(self.tree.item(item, "values"))
                values[0] = "☑" if new_state else "☐"
                self.tree.item(item, values=values)
    
    def on_device_type_double_click(self, event):
        """Handle double-click on device type to show selection dialog"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            # If double-clicked on device type column
            if item and column == "#2":  # DeviceType column
                # Create popup window for device type selection
                self.show_device_type_selector(item)
    
    def show_device_type_selector(self, item):
        """Show popup window to select device type"""
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Select Device Type")
        popup.geometry("350x400")
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(bg=self.bg_dark)
        
        # Center the popup
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        tk.Label(
            popup,
            text="Select Device Type:",
            font=("Arial", 12, "bold"),
            pady=10,
            bg=self.bg_dark,
            fg=self.fg_primary
        ).pack()
        
        # Create listbox with device types
        listbox_frame = tk.Frame(popup, bg=self.bg_dark)
        listbox_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame, bg=self.bg_light)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 11),
            yscrollcommand=scrollbar.set,
            height=12,
            bg=self.bg_light,
            fg=self.fg_primary,
            selectbackground=self.accent_blue,
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Add device types to listbox
        for device_type in self.available_device_types:
            listbox.insert(tk.END, device_type)
        
        # Highlight current selection
        current_type = self.device_types.get(item, "")
        if current_type in self.available_device_types:
            idx = self.available_device_types.index(current_type)
            listbox.selection_set(idx)
            listbox.see(idx)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                selected_type = self.available_device_types[selection[0]]
                # Update the tree item
                values = list(self.tree.item(item, "values"))
                values[1] = selected_type
                self.tree.item(item, values=values)
                self.device_types[item] = selected_type
                popup.destroy()
        
        def on_double_click(event):
            on_select()
        
        listbox.bind("<Double-Button-1>", on_double_click)
        
        # Buttons
        button_frame = tk.Frame(popup, bg=self.bg_dark)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Select",
            command=on_select,
            font=("Arial", 10, "bold"),
            bg=self.accent_blue,
            fg="white",
            padx=20,
            pady=5,
            relief=tk.FLAT,
            borderwidth=0,
            activebackground="#0a5a5d"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy,
            font=("Arial", 10),
            bg=self.bg_light,
            fg=self.fg_primary,
            padx=20,
            pady=5,
            relief=tk.FLAT,
            borderwidth=0
        ).pack(side=tk.LEFT, padx=5)
    
    def add_manual_device(self):
        """Add device manually from dropdown"""
        device_name = self.device_dropdown_add.get()
        product_code = self.product_code_entry.get().strip()
        serial = self.serial_entry.get().strip()
        
        if not device_name:
            messagebox.showwarning("Warning", "Please select a device from dropdown")
            return
        
        if not serial:
            messagebox.showwarning("Warning", "Please enter a serial number")
            return
        
        # Add to tree
        item_id = self.tree.insert("", tk.END, values=("☑", device_name, product_code, serial))
        self.device_selected[item_id] = True
        self.device_types[item_id] = device_name
        
        # Clear inputs
        self.device_dropdown_add.set("")
        self.product_code_entry.delete(0, tk.END)
        self.serial_entry.delete(0, tk.END)
        
        # Enable export button
        self.export_btn.config(state=tk.NORMAL)
        
        self.status_label.config(text=f"✓ Added {device_name}")
    
    def edit_selected_device(self):
        """Edit selected device"""
        # Use tree selection, not just checked items
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a device row to edit (click to highlight)")
            return
        if len(selected) > 1:
            messagebox.showwarning("Warning", "Please select only one device to edit")
            return
        item = selected[0]
        values = self.tree.item(item, "values")
        current_device_type = values[1]
        current_code = values[2]
        current_serial = values[3]
        self.show_edit_dialog(item, current_device_type, current_code, current_serial)
    
    def show_edit_dialog(self, item, device_type, code, serial):
        """Show popup window to edit device"""
        popup = tk.Toplevel(self.root)
        popup.title("Edit Device")
        popup.geometry("400x300")
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(bg=self.bg_dark)
        # Center the popup
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        tk.Label(
            popup,
            text="Edit Device Information",
            font=("Arial", 12, "bold"),
            pady=15,
            bg=self.bg_dark,
            fg=self.fg_primary
        ).pack()
        # Device Type
        type_frame = tk.Frame(popup, pady=10, bg=self.bg_dark)
        type_frame.pack(fill=tk.X, padx=20)
        tk.Label(type_frame, text="Device Type:", font=("Arial", 10), width=12, anchor=tk.W, bg=self.bg_dark, fg=self.fg_primary).pack(side=tk.LEFT)
        type_combo = ttk.Combobox(
            type_frame,
            values=self.available_device_types,
            state="readonly",
            font=("Arial", 10),
            width=25
        )
        type_combo.set(device_type)
        type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Product Code
        code_frame = tk.Frame(popup, pady=10, bg=self.bg_dark)
        code_frame.pack(fill=tk.X, padx=20)
        tk.Label(code_frame, text="Code:", font=("Arial", 10), width=12, anchor=tk.W, bg=self.bg_dark, fg=self.fg_primary).pack(side=tk.LEFT)
        code_entry = tk.Entry(code_frame, font=("Arial", 10), bg=self.bg_light, fg=self.fg_primary, insertbackground=self.fg_primary)
        code_entry.insert(0, code)
        code_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Serial Number
        serial_frame = tk.Frame(popup, pady=10, bg=self.bg_dark)
        serial_frame.pack(fill=tk.X, padx=20)
        tk.Label(serial_frame, text="Serial:", font=("Arial", 10), width=12, anchor=tk.W, bg=self.bg_dark, fg=self.fg_primary).pack(side=tk.LEFT)
        serial_entry = tk.Entry(serial_frame, font=("Arial", 10), bg=self.bg_light, fg=self.fg_primary, insertbackground=self.fg_primary)
        serial_entry.insert(0, serial)
        serial_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        def on_save():
            new_device_type = type_combo.get()
            new_code = code_entry.get().strip()
            new_serial = serial_entry.get().strip()
            if not new_device_type or new_device_type == "[Click to select device type]":
                messagebox.showwarning("Warning", "Please select a device type")
                return
            if not new_serial:
                messagebox.showwarning("Warning", "Serial number cannot be empty")
                return
            # Update the tree item
            values = list(self.tree.item(item, "values"))
            values[1] = new_device_type
            values[2] = new_code
            values[3] = new_serial
            self.tree.item(item, values=values)
            self.device_types[item] = new_device_type
            self.status_label.config(text=f"✓ Updated {new_device_type}")
            popup.destroy()
        # Buttons
        button_frame = tk.Frame(popup, pady=20, bg=self.bg_dark)
        button_frame.pack()
        tk.Button(
            button_frame,
            text="Save",
            command=on_save,
            font=("Arial", 10, "bold"),
            bg=self.accent_blue,
            fg="white",
            padx=30,
            pady=8,
            relief=tk.FLAT,
            borderwidth=0,
            activebackground="#0a5a5d"
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy,
            font=("Arial", 10),
            bg=self.bg_light,
            fg=self.fg_primary,
            padx=30,
            pady=8,
            relief=tk.FLAT,
            borderwidth=0
        ).pack(side=tk.LEFT, padx=5)
    
    def remove_selected_device(self):
        """Remove selected device from list"""
        selected_items = [item for item, selected in self.device_selected.items() if selected]
        
        if not selected_items:
            messagebox.showinfo("Info", "Please check the devices you want to remove")
            return
        
        for item in selected_items:
            self.tree.delete(item)
            del self.device_selected[item]
            if item in self.device_types:
                del self.device_types[item]
        
        self.status_label.config(text=f"✓ Removed {len(selected_items)} device(s)")
            
    def parse_device_text(self, text):
        """Parse OCR text to extract device and engine serial information"""
        devices = []
        lines = text.split('\n')
        
        # Process each line - looking for product name + code + serial
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Split line into parts (space-separated)
            parts = line.split()
            if len(parts) < 2:
                continue
            
            # Look for product code patterns (E##### or V##### etc.)
            product_code_pattern = r'^(E\d{5}|V\d{5}|MS-[A-Z0-9]+|\d{1,3}L\d{4})$'
            
            # Look for serial number patterns
            # Further expanded serial patterns based on new examples
            serial_patterns = [
                r'^[A-Z]{3}\d[A-Z0-9]{3}$',  # TAZ2ZKB, TAR3WR7, TADG0G9
                r'^\d{7,12}$',  # 1240430, 0330729, 10962030599, 3490083196
                r'^[JC]\d{6}-\d{4}$',  # J497793-0051
                r'^E\d{10,}$',  # E704760350080
                r'^[A-Z]{1,2}\d{7,10}$',  # Yamaha: 6MLN1000296, Mercury: 1E100979
                r'^[A-Z0-9]{8,12}$',  # General engine/device serials: 3B417994, 3B424456, 3B331193
                r'^[A-Z]{1,2}\d{6,8}$',  # Volvo: A1230833
                r'^\d{8,10}$',  # Numeric serials: 0233669, 0326146
                r'^[A-Z]{1,2}\d{6,12}$',  # e.g. 6MLLN1005392, 6KNN1005289
                r'^[A-Z0-9]{6,14}$',  # e.g. 3B553644, 3B557006, 3B563885, 3B563883
                r'^[A-Z]{1,2}\d{6,12}$',  # e.g. 6MLN1005390, 6MLLN1005392
                r'^[A-Z]{1,2}\d{6,12}$',  # e.g. 6KNN1005289, 6KNN1005075
                r'^[A-Z0-9]{8,15}$',  # e.g. 1E103027, 1E103214, 1E102818, 1E102771
                r'^[A-Z0-9]{8,15}$',  # e.g. 1E102775, 1E102817, 1E102460
                r'^[A-Z0-9\u0391-\u03A9]{8,15}$',  # Greek/Unicode letters (e.g. 13500033Α, 3Β535504)
                r'^[A-Z0-9\-]{6,16}$',  # D6-440A-G, 8LV370Z, XF450NSA
                r'^[A-Z0-9]{4,8}$',  # Short Yanmar: 6467, 6465, 6725, 6724
            ]
            
            # Try to find product code and serial in the line
            product_code_idx = None
            serial_idx = None
            
            for idx, part in enumerate(parts):
                # Check if this part is a product code
                if re.match(product_code_pattern, part):
                    product_code_idx = idx
                
                # Check if this part is a serial number
                for pattern in serial_patterns:
                    if re.match(pattern, part):
                        serial_idx = idx
                        break
            
            # If we found both a product code and serial number
            if product_code_idx is not None and serial_idx is not None and serial_idx > product_code_idx:
                # Product name is everything before the serial number
                product_parts = parts[:serial_idx]
                product_name = ' '.join(product_parts)
                
                # Serial is the last part
                serial_number = parts[serial_idx]
                
                devices.append({
                    'product': product_name,
                    'serial': serial_number
                })
            
            # If we only found product code but no serial on same line, check next line
            elif product_code_idx is not None and serial_idx is None and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                next_parts = next_line.split()
                
                for part in next_parts:
                    for pattern in serial_patterns:
                        if re.match(pattern, part):
                            product_name = ' '.join(parts[:product_code_idx+1])
                            devices.append({
                                'product': product_name,
                                'serial': part
                            })
                            break
        
        # Engine serial detection: look for lines indicating engine serial markers
        for i, line in enumerate(lines):
            l = line.strip()
            if not l:
                continue
            # Look for engine serial blocks (Yamaha, Mercury, Volvo, etc.)
            if re.search(r'engine', l, flags=re.IGNORECASE) or re.search(r'engines', l, flags=re.IGNORECASE):
                # Scan next few lines for model/serial pairs
                for j in range(i+1, min(i+6, len(lines))):
                    model_line = lines[j].strip()
                    if re.search(r'model', model_line, flags=re.IGNORECASE):
                        # Try to get serial from next line
                        if j+1 < len(lines):
                            serial_line = lines[j+1].strip()
                            serial_match = None
                            for pattern in serial_patterns:
                                m = re.match(pattern, serial_line)
                                if m:
                                    serial_match = serial_line
                                    break
                            if serial_match:
                                devices.append({'product': 'ENGINE', 'serial': serial_match})
                    # Also catch lines like 'SERIAL NUMBER:'
                    if re.search(r'serial', model_line, flags=re.IGNORECASE):
                        serial_match = None
                        for pattern in serial_patterns:
                            m = re.match(pattern, model_line)
                            if m:
                                serial_match = model_line
                                break
                        if serial_match:
                            devices.append({'product': 'ENGINE', 'serial': serial_match})

        # Remove duplicates
        seen = set()
        unique_devices = []
        for device in devices:
            key = (device['product'], device['serial'])
            if key not in seen:
                seen.add(key)
                unique_devices.append(device)
        
        return unique_devices
    
    def export_results(self):
        """Export results to text file"""
        # Get selected devices from tree
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "No devices to export")
            return
        
        # Check if any devices are selected
        selected_count = sum(1 for selected in self.device_selected.values() if selected)
        if selected_count == 0:
            messagebox.showwarning("Warning", "Please select at least one device to export")
            return
        
        # Get SAP for filename
        sap_number = self.sap_entry.get()
        if sap_number == "e.g., 9100967" or not sap_number.strip():
            default_name = f"SN_NoSAP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        else:
            default_name = f"SN_{sap_number}.txt"
        
        file_path = filedialog.asksaveasfilename(
            title="Save Device Serial Numbers",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Get vessel information
                vessel_model = self.vessel_model_entry.get()
                if vessel_model == "Select model..." or not vessel_model.strip():
                    vessel_model = "N/A"
                
                vessel_name = self.vessel_name_entry.get()
                if vessel_name == "e.g., Sea Explorer" or not vessel_name.strip():
                    vessel_name = "N/A"
                
                sap_number = self.sap_entry.get()
                if sap_number == "e.g., 9100967" or not sap_number.strip():
                    sap_number = "N/A"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Header with vessel info - format: (MODEL) - (NAME)
                    f.write(f"{vessel_model} - {vessel_name}\n")
                    # SAP line
                    f.write(f"{sap_number}\n")
                    # Divider line
                    f.write("___________________________________\n\n")
                    
                    # Collect devices grouped by type
                    devices_by_type = {}
                    for item in self.tree.get_children():
                        if self.device_selected.get(item, False):
                            values = self.tree.item(item, "values")
                            # values: (checkbox, device_type, code, serial)
                            device_type = values[1]
                            code = values[2]
                            serial = values[3]
                            
                            # Skip if device type not selected
                            if device_type == "[Click to select device type]":
                                continue
                            
                            # Group by device type
                            if device_type not in devices_by_type:
                                devices_by_type[device_type] = []
                            
                            devices_by_type[device_type].append({
                                'code': code,
                                'serial': serial
                            })
                    
                    # Export grouped by device type
                    exported_count = 0
                    for device_type, devices in devices_by_type.items():
                        # Append 'GPS' to AXIOM screens
                        display_type = device_type
                        if device_type.upper().startswith("AXIOM"):
                            display_type = f"{device_type} GPS"
                        # For engines, show count and type
                        if device_type.upper() == "ENGINE" or device_type.upper().startswith("ENGINE"):
                            count = len(devices)
                            if count > 1:
                                display_type = f"{device_type} (x{count})"
                        else:
                            count = len(devices)
                            if count > 1:
                                display_type = f"{display_type} (x{count})"
                        f.write(f"{display_type}:\n")
                        # Write all serial numbers for this device type
                        for device in devices:
                            if device['code']:
                                f.write(f"{device['code']}\t{device['serial']}\n")
                            else:
                                f.write(f"{device['serial']}\n")
                            exported_count += 1
                        # Add blank line between device types
                        f.write("\n")
                
                self.status_label.config(text=f"✓ Exported {exported_count} devices to {Path(file_path).name}")
                messagebox.showinfo(
                    "Success",
                    f"Successfully exported {exported_count} selected devices to:\n{file_path}"
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")


def main():
    """Main entry point"""
    print("Starting Technohull Marine Device Serial Number Extractor...")
    print("Note: First run will download OCR model (~100MB). Please be patient.")
    
    root = tk.Tk()
    app = DeviceExtractorGUI(root)
    
    # Show initial loading message
    messagebox.showinfo(
        "Welcome!",
        "Technohull Marine Device Serial Number Extractor\n\n"
        "No installation required!\n\n"
        "Note: First time use will download OCR model (~100MB)\n"
        "This only happens once.\n\n"
        "Click OK to start"
    )
    
    root.mainloop()


if __name__ == '__main__':
    main()
