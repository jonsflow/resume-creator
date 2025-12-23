#!/usr/bin/env python3
"""
Resume Builder - Generate static HTML resume from YAML data
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

def load_yaml(filename: str) -> Dict[Any, Any]:
    """Load YAML file and return parsed data"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing {filename}: {e}")
        return {}

def generate_css(layout: Dict[Any, Any]) -> str:
    """Generate CSS from layout configuration"""
    colors = layout.get('colors', {{}})
    typography = layout.get('typography', {{}})
    spacing = layout.get('spacing', {{}})
    elements = layout.get('elements', {{}})
    
    return f"""
*
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: {typography.get('font_family', 'Arial, sans-serif')};
    line-height: {typography.get('spacing', {{}}).get('line_height', '1.4')};
    color: {colors.get('main', {{}}).get('text', '#333')};
    background: {colors.get('main', {{}}).get('background', 'white')};
}}

.resume-container {{
    max-width: {layout.get('layout', {{}}).get('page', {{}}).get('max_width', '8.5in')};
    min-height: {layout.get('layout', {{}}).get('page', {{}}).get('min_height', '11in')};
    margin: 0 auto;
    display: flex;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}}

.sidebar {{
    width: {layout.get('layout', {{}}).get('structure', {{}}).get('sidebar', {{}}).get('width', '35%')};
    background: {colors.get('sidebar', {{}}).get('background', '#3a4750')};
    color: {colors.get('sidebar', {{}}).get('text', 'white')};
    padding: {spacing.get('container_padding', '40px')} {spacing.get('sidebar_padding', '30px')};
}}

.main-content {{
    width: {layout.get('layout', {{}}).get('structure', {{}}).get('main', {{}}).get('width', '65%')};
    padding: {spacing.get('container_padding', '40px')};
    background: {colors.get('main', {{}}).get('background', 'white')};
}}

.profile-image {{
    width: {elements.get('profile_image', {{}}).get('width', '120px')};
    height: {elements.get('profile_image', {{}}).get('height', '120px')};
    border-radius: {elements.get('profile_image', {{}}).get('border_radius', '50%')};
    margin: 0 auto {elements.get('profile_image', {{}}).get('margin_bottom', '30px')};
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-color: #ddd;
}}

.sidebar h2 {{
    font-size: {typography.get('sizes', {{}}).get('sidebar_headings', '16px')};
    font-weight: {typography.get('weights', {{}}).get('headings', 'bold')};
    margin-bottom: {spacing.get('subsection_margin', '15px')};
    letter-spacing: 1px;
    border-bottom: {elements.get('borders', {{}}).get('sidebar_headings', {{}}).get('bottom', '2px solid #5a6a7a')};
    padding-bottom: {elements.get('borders', {{}}).get('sidebar_headings', {{}}).get('padding_bottom', '8px')};
}}

.sidebar h3 {{
    font-size: {typography.get('sizes', {{}}).get('sidebar_subheadings', '12px')};
    font-weight: {typography.get('weights', {{}}).get('headings', 'bold')};
    margin-top: {spacing.get('subsection_margin', '15px')};
    margin-bottom: 5px;
}}

.sidebar p, .sidebar li {{
    font-size: {typography.get('sizes', {{}}).get('sidebar_text', '10px')};
    margin-bottom: 5px;
    line-height: {typography.get('spacing', {{}}).get('sidebar_line_height', '1.3')};
}}

.sidebar ul {{
    list-style: none;
}}

.sidebar li {{
    margin-bottom: {spacing.get('item_margin', '8px')};
}}

.skills-category {{
    margin-bottom: {spacing.get('subsection_margin', '15px')};
}}

.skills-category strong {{
    display: block;
    font-size: {typography.get('sizes', {{}}).get('sidebar_text', '10px')};
    margin-bottom: 3px;
}}

.main-content h1 {{
    font-size: {typography.get('sizes', {{}}).get('name', '36px')};
    font-weight: {typography.get('weights', {{}}).get('headings', 'bold')};
    color: {colors.get('main', {{}}).get('headings', '#3a4750')};
    margin-bottom: 10px;
    letter-spacing: 2px;
}}

.main-content h2 {{
    font-size: {typography.get('sizes', {{}}).get('main_headings', '18px')};
    font-weight: {typography.get('weights', {{}}).get('headings', 'bold')};
    color: {colors.get('main', {{}}).get('headings', '#3a4750')};
    margin-top: {spacing.get('section_margin', '25px')};
    margin-bottom: {spacing.get('subsection_margin', '15px')};
    border-bottom: {elements.get('borders', {{}}).get('main_headings', {{}}).get('bottom', '2px solid #ddd')};
    padding-bottom: {elements.get('borders', {{}}).get('main_headings', {{}}).get('padding_bottom', '5px')};
}}

.job-header {{
    display: {elements.get('job_header', {{}}).get('display', 'flex')};
    justify-content: {elements.get('job_header', {{}}).get('justify_content', 'space-between')};
    align-items: {elements.get('job_header', {{}}).get('align_items', 'center')};
    margin-bottom: 5px;
}}

.job-title {{
    font-size: {typography.get('sizes', {{}}).get('job_titles', '12px')};
    font-weight: {typography.get('weights', {{}}).get('job_titles', 'bold')};
    color: {colors.get('main', {{}}).get('headings', '#3a4750')};
}}

.job-date {{
    font-size: {typography.get('sizes', {{}}).get('body_text', '10px')};
    color: {colors.get('main', {{}}).get('muted', '#666')};
    font-style: italic;
}}

.job-company {{
    font-size: {typography.get('sizes', {{}}).get('body_text', '10px')};
    color: {colors.get('main', {{}}).get('muted', '#666')};
    font-style: italic;
    margin-bottom: {spacing.get('item_margin', '8px')};
}}

.main-content ul {{
    margin-left: {spacing.get('list_indent', '15px')};
    margin-bottom: {spacing.get('subsection_margin', '15px')};
}}

.main-content li {{
    font-size: {typography.get('sizes', {{}}).get('body_text', '10px')};
    margin-bottom: 3px;
    color: {colors.get('main', {{}}).get('secondary', '#555')};
}}

.profile-text {{
    font-size: {typography.get('sizes', {{}}).get('profile_text', '11px')};
    color: {colors.get('main', {{}}).get('secondary', '#555')};
    line-height: {typography.get('spacing', {{}}).get('profile_line_height', '1.5')};
    margin-bottom: 20px;
}}

@media print {{
    .resume-container {{
        box-shadow: none;
        max-width: none;
        width: 100%;
    }}
}}
"""

def format_date(date_str: str) -> str:
    """Format date string for display"""
    return "Present" if date_str == "present" else date_str

def render_sidebar_section(section_name: str, data: Dict[Any, Any], sections: Dict[Any, Any]) -> str:
    """Render a sidebar section"""
    html = ""
    
    if section_name == "contact":
        personal = data.get('personal', {{}})
        contact = personal.get('contact', {{}})
        location = contact.get('location', {{}})
        links = contact.get('links', [])
        
        html += f"""
        <h2>CONTACT</h2>
        <p>{contact.get('email', '')}</p>
        <p>{location.get('city', '')}, {location.get('state', '')} {location.get('zip', '')}</p>
        <br>
        <p><strong>Website:</strong></p>
        """
        for link in links:
            html += f"<p>{link.get('display', '')}</p>"
            
    elif section_name in sections:
        section = sections[section_name]
        html += f"<h2>{section.get('title', '').upper()}</h2>"
        
        if section_name == "education":
            for degree in section.get('degrees', []):
                html += f"""
                <h3>{degree.get('degree', '')}</h3>
                <p>{degree.get('graduation_year', '')}</p>
                <p><em>{degree.get('institution', '')}</em></p>
                """
                
        elif section_name == "skills":
            for category in section.get('categories', []):
                items = ', '.join(category.get('items', []))
                html += f"""
                <div class="skills-category">
                    <strong>• {category.get('name', '')}:</strong>
                    <p>{items}</p>
                </div>
                """

        elif section_name == "favorite_dishes":
            html += "<ul>"
            for item in section.get('items', []):
                html += f"<li>• {item}</li>"
            html += "</ul>"

        elif section_name == "interests":
            items = ' • '.join(section.get('items', []))
            html += f"<p>{items}</p>"
    
    return html

def render_main_section(section_name: str, data: Dict[Any, Any], sections: Dict[Any, Any]) -> str:
    """Render a main content section"""
    html = ""
    
    if section_name == "header":
        personal = data.get('personal', {{}})
        html += f"<h1>{personal.get('full_name', '')}</h1>"
        
    elif section_name in sections:
        section = sections[section_name]
        html += f"<h2>{section.get('title', '').upper()}</h2>"
        
        if section_name == "profile":
            html += f'<p class="profile-text">{section.get("content", "")}</p>'
            
        elif section_name == "experience":
            for job in section.get('jobs', []):
                start_date = format_date(job.get('start_date', ''))
                end_date = format_date(job.get('end_date', ''))
                
                html += f"""
                <div class="job-header">
                    <span class="job-title">{job.get('position', '')}</span>
                    <span class="job-date">{start_date} – {end_date}</span>
                </div>
                <p class="job-company">{job.get('company', '')} – {job.get('location', '')}</p>
                <ul>
                """
                for achievement in job.get('achievements', []):
                    html += f"<li>{achievement}</li>"
                html += "</ul>"

    return html

def generate_html(data: Dict[Any, Any], layout: Dict[Any, Any]) -> str:
    """Generate complete HTML from data and layout"""
    personal = data.get('personal', {{}})
    sections = data.get('sections', {{}})
    
    # Generate CSS
    css = generate_css(layout)
    
    # Render sidebar
    sidebar_sections = layout.get('layout', {{}}).get('structure', {{}}).get('sidebar', {{}}).get('sections', [])
    sidebar_html = ""
    
    # Add profile image first
    profile_image = personal.get('profile_image', {{}})
    sidebar_html += f'<div class="profile-image" style="background-image: url(\'{profile_image.get("path", "")}\');"></div>'
    
    # Add sidebar sections
    for section_name in sidebar_sections:
        sidebar_html += render_sidebar_section(section_name, data, sections)
    
    # Render main content
    main_sections = layout.get('layout', {{}}).get('structure', {{}}).get('main', {{}}).get('sections', [])
    main_html = ""
    
    for section_name in main_sections:
        main_html += render_main_section(section_name, data, sections)
    
    # Generate complete HTML
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal.get('full_name', 'Resume')}</title>
    <style>
        {css}
    </style>
</head>
<body>
    <div class="resume-container">
        <div class="sidebar">
            {sidebar_html}
        </div>
        <div class="main-content">
            {main_html}
        </div>
    </div>
</body>
</html>"""

def main():
    """Main function to build resume"""
    resume_data_dir = 'resume-data'
    
    # Find available resume YAML files
    try:
        resume_files = [f for f in os.listdir(resume_data_dir) if f.endswith(('.yml', '.yaml'))]
    except FileNotFoundError:
        print(f"Error: Directory '{resume_data_dir}' not found.")
        return

    if not resume_files:
        print(f"No resume data files found in '{resume_data_dir}'.")
        return

    # Select resume file
    if len(resume_files) == 1:
        selected_file = resume_files[0]
        print(f"Found one resume file: {selected_file}")
    else:
        print("Multiple resume files found. Please choose one:")
        for i, f in enumerate(resume_files):
            print(f"  {i + 1}: {f}")
        
        while True:
            try:
                choice = int(input(f"Enter number (1-{len(resume_files)}):"))
                if 1 <= choice <= len(resume_files):
                    selected_file = resume_files[choice - 1]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    resume_data_path = os.path.join(resume_data_dir, selected_file)
    
    # Load data files
    print(f"Loading resume data from {resume_data_path}...")
    resume_data = load_yaml(resume_data_path)
    layout_config = load_yaml('layout-config.yml')
    
    if not resume_data or not layout_config:
        print("Failed to load required YAML files")
        return
    
    print("Generating HTML...")
    html_content = generate_html(resume_data, layout_config)
    
    # Write output file
    output_file = f"{Path(selected_file).stem}.html"
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Resume generated successfully: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()
