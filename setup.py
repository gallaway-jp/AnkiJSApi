"""
Setup script for AnkiDroid JS API Desktop add-on
"""

import os
import json
import zipfile
from pathlib import Path
from setuptools import setup, find_packages, Command


class BuildAddonCommand(Command):
    """Custom command to build .ankiaddon package"""
    
    description = "Build .ankiaddon package for Anki"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        """Build the .ankiaddon package"""
        # Create dist directory
        dist_dir = Path("dist")
        dist_dir.mkdir(exist_ok=True)
        
        # Read version from manifest
        manifest_path = Path("src/ankidroid_js_api/manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            version = manifest.get("human_version", "1.0.0")
        
        # Create .ankiaddon file (renamed .zip)
        addon_filename = f"ankidroid_js_api_desktop-{version}.ankiaddon"
        addon_path = dist_dir / addon_filename
        
        print(f"Building {addon_filename}...")
        
        with zipfile.ZipFile(addon_path, "w", zipfile.ZIP_DEFLATED) as zf:
            src_dir = Path("src/ankidroid_js_api")
            
            for file_path in src_dir.rglob("*"):
                if file_path.is_file():
                    # Skip __pycache__ and .pyc files
                    if "__pycache__" in str(file_path) or file_path.suffix == ".pyc":
                        continue
                    
                    # Add file to zip with relative path
                    arcname = file_path.relative_to(src_dir)
                    zf.write(file_path, arcname)
                    print(f"  Added: {arcname}")
        
        print(f"\nSuccessfully built: {addon_path}")
        print(f"\nTo install:")
        print(f"1. Open Anki Desktop")
        print(f"2. Go to Tools → Add-ons → Install from file")
        print(f"3. Select: {addon_path.absolute()}")


setup(
    name="ankidroid-js-api-desktop",
    version="1.0.0",
    description="Brings AnkiDroid's JavaScript API to Anki Desktop",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="AnkiDroid JS API Contributors",
    author_email="",
    url="https://github.com/yourusername/ankidroid-js-api-desktop",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "ankidroid_js_api": [
            "js/*.js",
            "test_templates/*.html",
            "manifest.json",
            "config.json",
        ],
    },
    python_requires=">=3.9",
    install_requires=[
        # Anki is not typically installed via pip for add-ons
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-anki>=1.0.0",
            "black>=22.0.0",
            "mypy>=0.990",
            "pylint>=2.15.0",
        ],
    },
    cmdclass={
        "build_addon": BuildAddonCommand,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="anki ankidroid addon flashcards spaced-repetition",
)
