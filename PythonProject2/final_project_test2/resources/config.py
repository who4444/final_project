from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = BASE_DIR / "resources"

# Resource directories
BOOKS_DIR = RESOURCES_DIR / "books"
COVERS_DIR = RESOURCES_DIR / "covers"
IMAGES_DIR = RESOURCES_DIR / "images"
CONFIG_DIR = RESOURCES_DIR / "config"
ICONS_DIR = RESOURCES_DIR / "icons"

# Icon paths organized in dictionary
ICONS = {
    'notification': {
        'alert': ICONS_DIR / "alert_icon.png",
        'bell': ICONS_DIR / "bell_icon.png"
    },
    'menu': {
        'home': ICONS_DIR / "home_icon.png",
        'settings': ICONS_DIR / "settings_icon.png"
    },
    'status': {
        'success': ICONS_DIR / "success_icon.png",
        'error': ICONS_DIR / "error_icon.png"
    }
}

# Database paths
DATABASE_DIR = BASE_DIR / "database"

# UI paths
UI_DIR = BASE_DIR / "ui"
DIALOGS_DIR = UI_DIR / "dialogs"
READERS_DIR = UI_DIR / "readers"

# Create required directories
DIRECTORIES = [
    BOOKS_DIR,
    COVERS_DIR,
    IMAGES_DIR,
    CONFIG_DIR,
    ICONS_DIR
]

def ensure_directories():
    """Create directories if they don't exist."""
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)

# Helper function to verify icon existence
def verify_icon(icon_path: Path) -> bool:
    """Check if icon file exists."""
    return icon_path.exists()

if __name__ == "__main__":
    print(verify_icon(ICONS['notification']['bell']))
    img_path = ICONS['notification']['bell']
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    img = mpimg.imread(img_path)
    plt.imshow(img)
    plt.axis('off')  # Turn off axis labels and ticks
    plt.show()
