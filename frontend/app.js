// ---- sessão ----
let sessionId = sessionStorage.getItem("session_id")
if (!sessionId) {
  sessionId = crypto.randomUUID()
  sessionStorage.setItem("session_id", sessionId)
}

let lastPost = ""
let lastLegenda = ""
let lastHashtags = ""
let lastImageUrl = ""
let sending = false

const API_URL = window.location.hostname === "localhost"
  ? "http://127.0.0.1:8000"
  : ""

const chat = document.getElementById("chat")
const input = document.getElementById("msg")
const sendBtn = document.getElementById("sendBtn")


// ---- enviar mensagem ----

async function enviar() {
  const texto = input.value.trim()
  if (!texto || sending) return

  appendMsg("user", texto)
  input.value = ""
  setSending(true)

  const typing = showTyping()

  try {
    const res = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: texto, session_id: sessionId })
    })

    const data = await res.json()

    removeTyping(typing)

    if (data.post) {
      lastPost = data.post
      lastImageUrl = data.image_url || ""
      appendPost(data.post, data.image_url)
      return
    }

    appendMsg("bot", data.message || "Erro ao gerar resposta.")

  } catch (err) {
    console.error(err)
    removeTyping(typing)
    appendMsg("bot", "Erro ao conectar com o servidor.")
  } finally {
    setSending(false)
  }
}


// ---- controle de envio ----

function setSending(val) {
  sending = val
  sendBtn.disabled = val
  input.disabled = val
  if (!val) input.focus()
}


// ---- mensagem simples ----

function appendMsg(sender, text) {
  const div = document.createElement("div")
  div.className = `msg ${sender}`
  div.innerHTML = `<div class="msg-content">${formatText(text)}</div>`
  chat.appendChild(div)
  scrollToBottom()
}


// ---- post card ----

function appendPost(text, imageUrl) {
  const div = document.createElement("div")
  div.className = "msg bot"
  div.style.maxWidth = "100%"

  // parse seções
  let legenda = ""
  let hashtags = ""

  if (text.includes("Hashtags")) {
    const parts = text.split(/🏷️\s*Hashtags\s*\n?/)
    legenda = parts[0].replace(/✍️\s*Legenda\s*\n?/, "").trim()
    hashtags = (parts[1] || "").trim()
  } else {
    legenda = text.replace(/✍️\s*Legenda\s*\n?/, "").trim()
  }

  lastLegenda = legenda
  lastHashtags = hashtags

  // imagem com loading state — Pollinations pode demorar 1-2min
  let imageHtml = ""
  if (imageUrl) {
    imageHtml = `
      <div class="post-card-image-wrapper" id="img-wrapper">
        <div class="post-card-image-loading" id="img-loading">
          <div class="img-spinner"></div>
          <span>Gerando imagem...</span>
        </div>
        <img
          class="post-card-image"
          id="post-image"
          alt="Imagem do post"
          style="display:none"
        >
      </div>`
  }

  let bodyHtml = ""

  if (legenda) {
    bodyHtml += `
      <div class="post-card-section">
        <div class="post-card-label">Legenda</div>
        <div class="post-card-text">${formatText(legenda)}</div>
      </div>`
  }

  if (hashtags) {
    bodyHtml += `
      <div class="post-card-section">
        <div class="post-card-label">Hashtags</div>
        <div class="post-card-hashtags">${hashtags}</div>
      </div>`
  }

  div.innerHTML = `
    <div class="post-card">
      ${imageHtml}
      <div class="post-card-body">
        ${bodyHtml}
      </div>
      <div class="post-card-actions">
        ${legenda ? `<button onclick="copiarLegenda()">Copiar legenda</button>` : ""}
        ${hashtags ? `<button onclick="copiarHashtags()">Copiar hashtags</button>` : ""}
        ${imageUrl ? `<button onclick="baixarImagem()">Baixar imagem</button>` : ""}
        <button class="primary" onclick="recomecar()">Novo post</button>
      </div>
    </div>
  `

  chat.appendChild(div)
  scrollToBottom()

  // carrega imagem após inserir no DOM
  if (imageUrl) {
    loadPostImage(imageUrl)
  }
}


// ---- carregamento de imagem com retry ----

function loadPostImage(url) {
  const img = document.getElementById("post-image")
  const loading = document.getElementById("img-loading")
  if (!img || !loading) return

  let attempts = 0
  const maxAttempts = 3
  const retryDelay = 10000 // 10s — Pollinations permite 1 request por vez

  function tryLoad() {
    attempts++

    img.onload = function () {
      loading.style.display = "none"
      img.style.display = "block"
      scrollToBottom()
    }

    img.onerror = function () {
      if (attempts < maxAttempts) {
        loading.querySelector("span").textContent = `Gerando imagem... (tentativa ${attempts + 1})`
        setTimeout(tryLoad, retryDelay)
      } else {
        loading.querySelector("span").textContent = "Não foi possível carregar a imagem"
        loading.querySelector(".img-spinner").style.display = "none"
      }
    }

    // cache buster pra forçar nova tentativa
    img.src = url + `&t=${Date.now()}`
  }

  // primeira tentativa com delay de 3s — dá tempo do Pollinations iniciar geração
  setTimeout(tryLoad, 3000)
}


// ---- typing indicator ----

function showTyping() {
  const div = document.createElement("div")
  div.className = "msg typing"
  div.id = "typing-indicator"
  div.innerHTML = `
    <div class="msg-content">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>
  `
  chat.appendChild(div)
  scrollToBottom()
  return div
}

function removeTyping(el) {
  if (el && el.parentNode) el.parentNode.removeChild(el)
}


// ---- ações ----

function copiarLegenda() {
  if (!lastLegenda) return
  navigator.clipboard.writeText(lastLegenda)
  showToast("Legenda copiada!")
}

function copiarHashtags() {
  if (!lastHashtags) return
  navigator.clipboard.writeText(lastHashtags)
  showToast("Hashtags copiadas!")
}

function baixarImagem() {
  if (!lastImageUrl) return
  // abre em nova aba — CORS impede fetch direto do Pollinations
  window.open(lastImageUrl, "_blank")
  showToast("Imagem aberta em nova aba — clique com botão direito para salvar!")
}

function recomecar() {
  fetch(`${API_URL}/api/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId })
  }).catch(() => {})

  sessionId = crypto.randomUUID()
  sessionStorage.setItem("session_id", sessionId)

  lastPost = ""
  lastLegenda = ""
  lastHashtags = ""
  lastImageUrl = ""

  chat.innerHTML = ""

  appendMsg("bot", 'Oi! Eu sou o <strong>Postador</strong> — te ajudo a criar posts incríveis para redes sociais.<br><br>Me conta: o que você quer divulgar?')
}


// ---- toast ----

function showToast(text) {
  const existing = document.querySelector(".toast")
  if (existing) existing.remove()

  const toast = document.createElement("div")
  toast.className = "toast"
  toast.textContent = text
  toast.style.cssText = `
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    background: #8b5cf6;
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 13px;
    font-family: inherit;
    z-index: 100;
    animation: fadeIn 0.3s ease;
  `
  document.body.appendChild(toast)
  setTimeout(() => toast.remove(), 2000)
}


// ---- utils ----

function formatText(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>")
}

function scrollToBottom() {
  requestAnimationFrame(() => {
    chat.scrollTop = chat.scrollHeight
  })
}


// ---- keyboard ----

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") enviar()
})
