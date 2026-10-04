def build_comic_layout(images: list, full_story: str, outline: list) -> list:
    story_parts = full_story.split('|||')
    
    layout = []
    for i, panel in enumerate(outline):
        story_text = story_parts[i].strip() if i < len(story_parts) else "Text generation missed this panel."
        title = panel.get("title", f"Panel {i+1}")
        scene_desc = panel.get("scene_description", "")
        img_prompt = panel.get("image_prompt", "")
        
        layout.append({
            "panel": i + 1,
            "panel_number": i + 1,
            "number": i + 1,
            "title": title,
            "image": images[i],
            "image_path": images[i],
            "scene_description": scene_desc,
            "description": scene_desc,
            "image_prompt": img_prompt,
            "text": story_text,
            "story_text": story_text
        })
    return layout