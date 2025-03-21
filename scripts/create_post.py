#!/usr/bin/env python3
import sys
import os
from datetime import datetime
import re

def slugify(title):
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower().strip()
    # Remove special characters
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def create_post(title):
    if not title:
        print("Error: Please provide a title for the blog post")
        sys.exit(1)

    # Get current date
    date = datetime.now().strftime('%Y-%m-%d')
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    
    # Create filename
    slug = slugify(title)
    filename = f"{date}-{slug}.md"
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_posts', filename)
    
    # Create post content
    content = f"""---
title: '{title}'
date: {date}
permalink: /posts/{year}/{month}/{slug}/
tags:
  - 
---

[Your content here]
"""
    
    # Create the file
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Created new post: {filepath}")
    except Exception as e:
        print(f"Error creating post: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_post.py \"Your Blog Post Title\"")
        sys.exit(1)
    
    title = " ".join(sys.argv[1:])
    create_post(title)
