from src.api import api_bp
from quart import jsonify, request
from src.utils.handle_requests import fetch_content
from urllib.parse import urlparse, unquote

async def scrape_list_group_items(url: str):
    soup = await fetch_content(url)
    links =  [(a.text.strip().split('\n')[0], unquote(urlparse(a["href"]).path.rstrip('/'))) for a in soup.find_all("a", class_="list-group-item")]
    filtered_links = [link for link in links if not link[1].endswith('.zip.html')]
    sorted_links = sorted(filtered_links, key=lambda x: x[1].endswith(('.mp3.html')))
    return dict(sorted_links)

@api_bp.route('/download/', defaults={"letter": None, "name": None, "song_album": None, "song": None, "section": None}, methods=["GET"], strict_slashes=False)
@api_bp.route('/download/<section>', defaults={"letter": None, "name": None, "song_album": None, "song": None}, methods=["GET"], strict_slashes=False)
@api_bp.route('/download/<section>/<letter>', defaults={"name": None, "song_album": None, "song": None}, methods=["GET"],strict_slashes=False)
@api_bp.route('/download/<section>/<letter>/<name>', defaults={"song_album": None, "song": None}, methods=["GET"], strict_slashes=False)
@api_bp.route('/download/<section>/<letter>/<name>/<song_album>', defaults={"song": None}, methods=["GET"], strict_slashes=False)
@api_bp.route('/download/<section>/<letter>/<name>/<song_album>/<song>', methods=["GET"], strict_slashes=False)
async def unified_download(section, letter, name, song_album, song):
    base_url = f"https://music.com.bd/download/{section}" if section else "https://music.com.bd/download"

    # Construct URL based on provided parts
    if song:
        url = f"{base_url}/{letter}/{name}/{song_album}/{song}"
    elif song_album:
        url = f"{base_url}/{letter}/{name}/{song_album}"
    elif letter and name:
        url = f"{base_url}/{letter}/{name}"
    elif letter:
        url = f"{base_url}/{letter}"
    else:
        url = base_url
    print(url)
    if url.endswith('download/browse'):
      url = "https://music.com.bd/download"
    if ".mp3" in url:
      data = await handle_mp3(url)
    else:
      data = await scrape_list_group_items(url)
    data.pop('Back to Parent Directory') if 'Back to Parent Directory' in data else None
    return jsonify({"data": data}), 200

async def handle_mp3(url):
   soup = await fetch_content(url)
   stream = soup.find("source", {"type": "audio/mpeg"})
   metadata = {}
   for li in soup.select('ul.list-group li'):
    key, sep, value = li.get_text(strip=True).partition(':')
    a_tag = li.find('a')
    metadata[key] = a_tag.text.lstrip() if a_tag else value.strip()
   if stream and stream.get("src"):
    return {"stream_url": stream.get("src"),"metadata": metadata}
   return "stream url not found"