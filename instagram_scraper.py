
import instaloader
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Initialize Instaloader
L = instaloader.Instaloader()

# List of drug-related keywords (expanded)
# List of drug-related keywords (expanded)
drug_keywords = [
    "A2", "Piperazines", "acetylfentanyl", "Acid", "Aerosols", "Agaric", "Alcohol", 
    "Alpha-Methyltryptamine", "Alprazolam", "Amphetamine", "Cannabis", "Cocaine", 
    "Heroin", "LSD", "MDMA", "Meth", "Weed", "Xanax", "Ecstasy", "ESRB", ""  # Add ESRB here
    # Add more keywords as needed
]


def contains_drug_keywords(text):
    """Check if the text contains any drug-related keywords."""
    text = text.lower() if text else ""
    for keyword in drug_keywords:
        if re.search(rf'\b{re.escape(keyword.lower())}\b', text):
            return True
    return False


def fetch_instagram_data(profile_name):
    """Fetch Instagram profile data and check posts for drug-related keywords."""
    output = []
    post_data = []
    try:
        output.append(f"Loading profile: {profile_name}")
        profile = instaloader.Profile.from_username(L.context, profile_name)

        output.append(f"Profile: {profile.username}")
        output.append(f"Bio: {profile.biography}")
        output.append(f"Followers: {profile.followers}")
        output.append(f"Following: {profile.followees}")

        # Check for drug-related keywords in the bio
        if contains_drug_keywords(profile.biography):
            output.append("⚠ Drug-related keywords found in bio.")
        else:
            output.append("No drug-related keywords found in bio.")

        # Fetch the user's posts and check for drug-related keywords
        found_any = False

        # Fetching all posts including images, not just reels
        for post in profile.get_posts():
            post_info = {
                'url': post.url,
                'caption': post.caption,
                'likes': post.likes,
                'comments': post.comments,
                'thumbnail_url': post.url + "media/?size=t",  # Thumbnail image URL (Instagram format)
                'media_url': post.url  # Regular post image URL (Instagram format)
            }

            # Check for drug-related keywords in the post caption
            if contains_drug_keywords(post.caption):
                post_info['contains_drug_keywords'] = True
                found_any = True
            else:
                post_info['contains_drug_keywords'] = False

            post_data.append(post_info)
            
            if len(post_data) == 10:  # Limit to showing the last 10 posts (adjustable)
                break

        if not found_any:
            output.append("No drug-related keywords found in recent posts.")
        
    except instaloader.exceptions.ProfileNotExistsException:
        output.append(f"Profile {profile_name} does not exist.")
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        output.append(f"Cannot access private profile: {profile_name}.")
    except Exception as e:
        output.append(f"An error occurred: {e}")
    
    return output, post_data

def display_data():
    """Display the Instagram profile data and posts in a Tkinter window."""
    profile_name = entry.get().strip()
    
    if not profile_name:
        messagebox.showerror("Error", "Please enter a valid Instagram profile name.")
        return
    
    data, posts = fetch_instagram_data(profile_name)

    # Create result window
    result_window = tk.Toplevel(root)
    result_window.title(f"Instagram Profile: {profile_name}")
    
    # Display general profile information
    text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=80, height=10)
    text_area.pack(padx=10, pady=10)
    text_area.insert(tk.END, "\n".join(data))
    
    # Display posts
    for post_info in posts:
        frame = tk.Frame(result_window, borderwidth=2, relief="groove")
        frame.pack(padx=10, pady=5, fill="x")
        
        # Load the full image for the post, not just thumbnails
        try:
            response = requests.get(post_info['media_url'])
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((200, 200))  # Adjust image size here if needed
            img_tk = ImageTk.PhotoImage(img)
            media_label = tk.Label(frame, image=img_tk)
            media_label.image = img_tk  # Keep reference to avoid garbage collection
            media_label.pack(side="left", padx=10)
        except Exception as e:
            tk.Label(frame, text="Image not available").pack(side="left", padx=10)
        
        # Post info text
        post_text = f"Post URL: {post_info['url']}\nLikes: {post_info['likes']}\nComments: {post_info['comments']}"
        post_caption = f"Caption: {post_info['caption'][:100]}..." if post_info['caption'] else "No caption"
        
        if post_info['contains_drug_keywords']:
            post_text += "\n⚠ Drug-related keywords found!"
        
        tk.Label(frame, text=post_text).pack(anchor="w")
        tk.Label(frame, text=post_caption, wraplength=400).pack(anchor="w")

# Tkinter GUI setup
root = tk.Tk()
root.title("Instagram Profile Drug Checker")

# Input field for Instagram profile name
tk.Label(root, text="Enter Instagram profile name:").pack(padx=10, pady=5)
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=5)

# Button to check the profile and display data
tk.Button(root, text="Check Profile", command=display_data).pack(padx=10, pady=10)

root.mainloop()