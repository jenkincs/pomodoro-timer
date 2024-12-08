from PIL import Image, ImageDraw

def create_tomato_icon(size=(32, 32)):
    """
    Create a tomato-shaped icon
    Args:
        size: Icon size, default 32x32 pixels
    """
    # Create a transparent background image
    icon = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Define colors
    tomato_red = (255, 59, 48)    # Tomato red
    leaf_green = (76, 217, 100)   # Leaf green
    
    # Calculate center point and radius
    center_x = size[0] // 2
    center_y = size[1] // 2 + 2  # Slightly offset downward
    radius = min(size) // 2 - 2  # Leave margin
    
    # Draw tomato body (circle)
    draw.ellipse(
        [
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ],
        fill=tomato_red
    )
    
    # Draw leaves (two triangular leaves)
    leaf_points1 = [
        (center_x - 2, center_y - radius),      # Left leaf bottom
        (center_x - 6, center_y - radius - 4),  # Left leaf tip
        (center_x + 2, center_y - radius - 2)   # Left leaf right side
    ]
    
    leaf_points2 = [
        (center_x, center_y - radius - 1),      # Right leaf bottom
        (center_x + 4, center_y - radius - 6),  # Right leaf tip
        (center_x - 3, center_y - radius - 3)   # Right leaf left side
    ]
    
    # Draw leaves
    draw.polygon(leaf_points1, fill=leaf_green)
    draw.polygon(leaf_points2, fill=leaf_green)
    
    # Add highlight effect (small white dot)
    highlight_pos = (center_x - radius//2, center_y - radius//2)
    highlight_size = 3
    draw.ellipse(
        [
            highlight_pos[0],
            highlight_pos[1],
            highlight_pos[0] + highlight_size,
            highlight_pos[1] + highlight_size
        ],
        fill=(255, 255, 255, 180)  # Semi-transparent white
    )
    
    # Save as ICO file
    icon.save('tomato.ico', format='ICO', sizes=[(32, 32)])
    print("Icon created: tomato.ico")

if __name__ == '__main__':
    create_tomato_icon()