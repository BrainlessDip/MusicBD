// Add these new functions
function toggleMinimize() {
  player.classList.toggle("minimized");
}

let currentPath = "";
const search = document.querySelector(".search");
const content = document.getElementById("content");
const breadcrumb = document.getElementById("breadcrumb");
const player = document.getElementById("player");
const audio = document.getElementById("audio");
const playingName = document.getElementById("playing-name");
const metaTitle = document.getElementById("meta-title");
const metaArtist = document.getElementById("meta-artist");
const metaAlbum = document.getElementById("meta-album");
const metaDuration = document.getElementById("meta-duration");

async function loadContent(path = "/download") {
  try {
    const res = await fetch(`/api${path}`);
    const data = await res.json();
    currentPath = path;
    updateBreadcrumb();
    renderContent(data.data);
  } catch (err) {
    console.error("Error loading content:", err);
  }
}

function renderContent(data) {
  content.innerHTML = "";

  if (currentPath !== "/download") {
    addItem("..", "📁", () => {
      const parentPath =
        currentPath.split("/").slice(0, -1).join("/") || "/download";
      loadContent(parentPath);
    });
  }

  Object.entries(data).forEach(([name, path]) => {
    if (name === "Back to Parent Directory") return;
    const isMusic = path.endsWith(".html");
    addItem(name, isMusic ? "🎵" : "📁", () => {
      isMusic ? playMusic(path, name) : loadContent(path);
    });
  });
}

function addItem(name, icon, onClick) {
  const item = document.createElement("div");
  item.className = "item";
  item.innerHTML = `
        <div class="item-icon">${icon}</div>
        <div class="item-name">${name.replace(
          /\s*\(music\.com\.bd\)\s*/g,
          ""
        )}</div>
        
      `;
  item.onclick = onClick;
  content.appendChild(item);
}

function updateBreadcrumb() {
  const parts = currentPath.split("/").filter(Boolean);
  let path = "";
  breadcrumb.innerHTML = `
        <span onclick="loadContent('/download')">Home</span>
        ${parts
          .map((part, i) => {
            path += `/${part}`;
            if (["browse", "download"].includes(part)) return "";
            const isLast = i === parts.length - 1;
            return `
              <span class="separator">/</span>
              <span class="${isLast ? "current" : ""}" ${
              !isLast ? `onclick="loadContent('${path}')"` : ""
            }>${part}</span>
            `;
          })
          .join("")}
      `;
}

async function playMusic(path, name) {
  try {
    const res = await fetch(`/api${path}`);
    const data = await res.json();
    if (data.data.stream_url) {
      player.classList.add("active");
      audio.src = data.data.stream_url;
      audio.play();
      if (data.data.metadata) {
        const meta = data.data.metadata;
        metaTitle.textContent = meta.Title || displayName;
        playingName.textContent = meta.Title;
        metaArtist.textContent = meta.Artist || "Unknown";
        metaAlbum.textContent = meta.Album || "Unknown";
        metaDuration.textContent = meta["Play Time"] || "--:--";
      } else {
        metaTitle.textContent = displayName;
        playingName.textContent = name
          .replace(/\.mp3$|\s*\(music\.com\.bd\)\s*/gi, "")
          .trim();
        metaArtist.textContent = "Unknown";
        metaAlbum.textContent = "Unknown";
        metaDuration.textContent = "--:--";
      }
      if ("mediaSession" in navigator) {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: metaTitle.textContent,
          artist: metaArtist.textContent,
          album: metaAlbum.textContent,
        });

        navigator.mediaSession.setActionHandler("play", () => audio.play());
        navigator.mediaSession.setActionHandler("pause", () => audio.pause());

        navigator.mediaSession.setActionHandler("seekbackward", (details) => {
          audio.currentTime = Math.max(
            audio.currentTime - (details.seekOffset || 10),
            0
          );
        });

        navigator.mediaSession.setActionHandler("seekforward", (details) => {
          audio.currentTime = Math.min(
            audio.currentTime + (details.seekOffset || 10),
            audio.duration
          );
        });
      }
    }
  } catch (err) {
    console.error("Error playing music:", err);
  }
}

function closePlayer() {
  audio.pause();
  player.classList.remove("active");
  player.classList.remove("minimized");
}

search.addEventListener("input", (e) => {
  const term = e.target.value.toLowerCase();
  document.querySelectorAll(".item").forEach((item) => {
    const name = item.querySelector(".item-name").textContent.toLowerCase();
    item.style.display = name.includes(term) ? "" : "none";
  });
});

// Initial load
loadContent();
