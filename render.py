import os
import markdown2
from datetime import datetime
import re
import html

def main():
    # Define the directory containing the Markdown files
    posts_dir = './docs/posts'
    output_dir = './docs/blog'
    index_output = './docs/index.html'

    # Read template.html
    with open("template.html", 'r', encoding='utf-8') as file:
        template = file.read()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(posts_dir, exist_ok=True)

    # List to store post metadata for index page
    posts_meta = []

    # Iterate over all dirs in the posts directory
    if os.path.exists(posts_dir):
        for post_directory in os.listdir(posts_dir):
            post_path = os.path.join(posts_dir, post_directory)
            if os.path.isdir(post_path):
                # Construct full file path
                file_path = os.path.join(post_path, 'post.md')
                
                if os.path.exists(file_path):
                    # Read the Markdown file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        md_content = file.read()

                    # Extract title from first h1
                    title = md_content.split("# ", 1)[1].split("\n")[0] if "# " in md_content else post_directory

                    # Convert Markdown to HTML
                    html_content = markdown2.markdown(
                        md_content,
                        extras=['fenced-code-blocks', 'header-ids', 'metadata']
                    )

                    # Fix image paths (use absolute path from site root)
                    html_content = html_content.replace(
                        '<img src="',
                        f'<img src="posts/{post_directory}/'
                    )

                    # Create the full HTML content
                    full_html = template.replace('<!--DAILY_THOUGHTS-->', html_content)
                    full_html = full_html.replace('<!--ARTICLES-->', '')
                    full_html = full_html.replace('{{ title }}', title)
                    full_html = full_html.replace('{{ base }}', '..')

                    # Save post metadata for index
                    posts_meta.append({
                        'title': title,
                        'url': f'blog/{post_directory}.html',
                        'date': datetime.fromtimestamp(os.path.getctime(file_path))
                    })

                    # Save the HTML file
                    html_path = os.path.join(output_dir, f'{post_directory}.html')
                    with open(html_path, 'w', encoding='utf-8') as file:
                        file.write(full_html)
                    print(f"Rendered {post_directory} to {html_path}")

    # Sort posts by date, newest first
    posts_meta.sort(key=lambda x: x['date'], reverse=True)

    # --- Daily Thoughts Section ---
    daily_dir = './docs/daily'
    daily_entries = []
    if os.path.exists(daily_dir):
        for fname in os.listdir(daily_dir):
            if fname.endswith('.md'):
                date_str = fname.replace('.md', '')
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    continue
                with open(os.path.join(daily_dir, fname), 'r', encoding='utf-8') as f:
                    md_content = f.read()
                    html_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'header-ids', 'metadata'])
                daily_entries.append({'date': date_obj, 'html': html_content})
        daily_entries.sort(key=lambda x: x['date'], reverse=True)

    # Prepare daily thoughts HTML
    daily_html = ""
    if daily_entries:
        daily_html += "<h2>Daily Thoughts</h2>"
        for entry in daily_entries:
            date_heading = entry['date'].strftime('%B %-d, %Y')
            daily_html += f'\n<h3>{date_heading}</h3>\n{entry["html"]}'

    # Prepare articles HTML
    articles_html = "<h2>Articles</h2>\n<ul>"
    for post in posts_meta:
        day = post['date'].day
        month = post['date'].strftime('%B')
        suffix = 'th' if 11<=day<=13 else {1:'st',2:'nd',3:'rd'}.get(day%10, 'th')
        date_str = f"{day}{suffix} {month}"
        articles_html += f'\n<li><strong>[{date_str}]</strong> <a href="{post["url"]}">{post["title"]}</a></li>'
    articles_html += "\n</ul>"

    # Inject into template
    index_html = template.replace('<!--DAILY_THOUGHTS-->', daily_html)
    index_html = index_html.replace('<!--ARTICLES-->', articles_html)
    index_html = index_html.replace('{{ title }}', "Madhav Arora's Blog")
    index_html = index_html.replace('{{ base }}', '.')

    # Save index.html directly to docs/
    with open(index_output, 'w', encoding='utf-8') as file:
        file.write(index_html)
    print(f"Rendered {index_output}")

    # Render About and Subscribe pages
    for page in [
        ("about.md", "About", "about.html"),
        ("subscribe.md", "Subscribe", "subscribe.html"),
        ("tools.md", "Tools", "tools.html")
    ]:
        md_file, page_title, html_file = page
        if os.path.exists(md_file):
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
                html_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'header-ids', 'metadata'])
            page_html = template.replace('<!--DAILY_THOUGHTS-->', html_content)
            page_html = page_html.replace('<!--ARTICLES-->', '')
            page_html = page_html.replace('{{ title }}', page_title)
            page_html = page_html.replace('{{ base }}', '.')
            with open(os.path.join('docs', html_file), 'w', encoding='utf-8') as f:
                f.write(page_html)
            print(f"Rendered docs/{html_file}")

if __name__ == "__main__":
    main() 