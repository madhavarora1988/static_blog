import os
import markdown2
from datetime import datetime

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
                    full_html = template.replace('{{ content }}', html_content)
                    full_html = full_html.replace('{{ title }}', title)

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

    # Create index.html
    index_content = "<h1>Welcome to My Blog</h1>"
    if os.path.exists("greetings.md"):
        with open("greetings.md", 'r', encoding='utf-8') as file:
            greeting = markdown2.markdown(file.read())
            index_content = greeting

    # Add post list
    index_content += "\n<h2>Posts</h2>\n<ul>"
    for post in posts_meta:
        date_str = post['date'].strftime('%Y-%m-%d')
        index_content += f'\n<li>[{date_str}] <a href="{post["url"]}">{post["title"]}</a></li>'
    index_content += "\n</ul>"

    # Create the full index HTML
    index_html = template.replace('{{ content }}', index_content)
    index_html = index_html.replace('{{ title }}', "My Blog")

    # Save index.html directly to docs/
    with open(index_output, 'w', encoding='utf-8') as file:
        file.write(index_html)
    print(f"Rendered {index_output}")

if __name__ == "__main__":
    main() 