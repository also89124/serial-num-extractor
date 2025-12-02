"""
Create app icon and logo from barcode image
"""

from PIL import Image
import os

def create_logo():
    """Create app logo from existing barcode image"""
    
    # Load the barcode image
    barcode_path = "barcode-illustration-isolated_23-2150584090.avif"
    
    if not os.path.exists(barcode_path):
        print(f"Error: {barcode_path} not found!")
        print("Creating fallback barcode icon...")
        # Create a simple fallback if image not found
        from PIL import ImageDraw
        logo = Image.new('RGB', (256, 256), 'white')
        draw = ImageDraw.Draw(logo)
        
        # Draw simple barcode pattern
        bar_width = 6
        x = 30
        for i in range(30):
            if i % 2 == 0:
                draw.rectangle([x, 50, x + bar_width, 206], fill='black')
            x += bar_width + 2
        return logo
    
    try:
        # Load and process the barcode image
        logo = Image.open(barcode_path)
        
        # Convert to RGB if needed
        if logo.mode != 'RGB':
            logo = logo.convert('RGB')
        
        # Resize to 256x256 maintaining aspect ratio
        logo.thumbnail((256, 256), Image.Resampling.LANCZOS)
        
        # Create a white background
        final_logo = Image.new('RGB', (256, 256), 'white')
        
        # Center the barcode image
        x_offset = (256 - logo.width) // 2
        y_offset = (256 - logo.height) // 2
        final_logo.paste(logo, (x_offset, y_offset))
        
        return final_logo
        
    except Exception as e:
        print(f"Error loading barcode image: {e}")
        print("Creating fallback barcode icon...")
        from PIL import ImageDraw
        logo = Image.new('RGB', (256, 256), 'white')
        draw = ImageDraw.Draw(logo)
        
        # Draw simple barcode pattern
        bar_width = 6
        x = 30
        for i in range(30):
            if i % 2 == 0:
                draw.rectangle([x, 50, x + bar_width, 206], fill='black')
            x += bar_width + 2
        return logo

def create_icon():
    """Create Windows .ico file"""
    logo = create_logo()
    
    # Create multiple sizes for .ico
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    icons = []
    
    for size in sizes:
        resized = logo.resize(size, Image.Resampling.LANCZOS)
        icons.append(resized)
    
    return icons

if __name__ == '__main__':
    # Create assets directory
    os.makedirs('assets', exist_ok=True)
    
    # Create and save logo
    logo = create_logo()
    logo.save('assets/app_logo.png', 'PNG')
    print("✓ Created app_logo.png")
    
    # Create and save icon
    icons = create_icon()
    icons[0].save(
        'assets/app_icon.ico',
        format='ICO',
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    )
    print("✓ Created app_icon.ico")
    
    # Also save smaller logo for title bar
    small_logo = logo.resize((50, 50), Image.Resampling.LANCZOS)
    small_logo.save('assets/app_logo_small.png', 'PNG')
    print("✓ Created app_logo_small.png")
    
    print("\n✓ All icons created successfully!")
    print("Icons saved to: assets/")
