let lang = localStorage.getItem("lang") || "pt"

// cria session id se não existir (uma por aba)
let sessionId = sessionStorage.getItem("session_id")

if (!sessionId) {
    sessionId = crypto.randomUUID()
    sessionStorage.setItem("session_id", sessionId)
}

console.log("SESSION:", sessionId)

let lastPost = ""
let lastImage = ""

const texts = {

pt:{
welcome:"👋 Olá! Eu sou <b>O Postador 🤖</b><br>Digite Oi para começar!",
placeholder:"Digite sua mensagem...",
send:"Enviar"
},

en:{
welcome:"👋 Hello! I'm <b>The Poster 🤖</b><br>Type Hi to start!",
placeholder:"Type your message...",
send:"Send"
}

}

function setLang(l){

lang = l

localStorage.setItem("lang",l)

document.getElementById("welcome").innerHTML = texts[l].welcome
document.getElementById("msg").placeholder = texts[l].placeholder
document.getElementById("sendBtn").innerText = texts[l].send

}

window.onload = function(){
setLang(lang)
}

async function enviar(){

const input = document.getElementById('msg')
const texto = input.value.trim()

if(!texto) return

appendMsg('user', texto)

input.value = ''

try{

const API_URL = "http://127.0.0.1:8000"

const res = await fetch(`${API_URL}/chat`,{
  method:'POST',
  headers:{
    'Content-Type':'application/json'
  },
  body:JSON.stringify({
    message:texto,
    session_id:sessionId
  })
})

const data = await res.json()

console.log("SERVER RESPONSE:", data)


// 🖼️ SE VEIO IMAGEM
if(data.image){

appendImage(data.image)
lastImage = data.image

return

}


// resposta normal
const resposta =
      data.message
   || data.post
   || data.reply
   || "Erro ao gerar resposta"

lastPost = resposta

appendPost(resposta)

}catch(err){

console.error(err)

appendMsg('bot','Erro ao conectar com o servidor')

}

}


// mensagem simples
function appendMsg(sender,text){

const div = document.createElement('div')

div.className = `msg ${sender}`

div.innerHTML = linkify(text)

const chat = document.getElementById('chat')

chat.appendChild(div)

chat.scrollTop = chat.scrollHeight

}


// POST COM BOTÕES
function appendPost(text){

const div = document.createElement('div')

div.className = "msg bot"

div.innerHTML = `
<div>${linkify(text)}</div>

<div style="margin-top:10px">

<button onclick="gerarImagem()">🎨 Gerar imagem</button>

<button onclick="copiarPost()">📋 Copiar post</button>

</div>
`

const chat = document.getElementById('chat')

chat.appendChild(div)

chat.scrollTop = chat.scrollHeight

}


// 🖼️ FUNÇÃO PARA MOSTRAR IMAGEM
function appendImage(base64){

const div = document.createElement('div')

div.className = "msg bot"

const img = document.createElement('img')

img.src = "data:image/png;base64," + base64
img.style.maxWidth = "300px"
img.style.borderRadius = "10px"
img.style.marginTop = "5px"

div.appendChild(img)

const btns = document.createElement("div")
btns.style.marginTop = "10px"

btns.innerHTML = `
<button onclick="baixarImagem()">⬇️ Baixar</button>
`

div.appendChild(btns)

const chat = document.getElementById('chat')

chat.appendChild(div)

chat.scrollTop = chat.scrollHeight

}


// 🎨 GERAR IMAGEM
async function gerarImagem(){

appendMsg("bot","🎨 Gerando imagem...")

const API_URL = "http://127.0.0.1:8000"

try{

const res = await fetch(`${API_URL}/gerar-imagem`,{
method:'POST',
headers:{
'Content-Type':'application/json'
},
body:JSON.stringify({
session_id:sessionId
})
})

const data = await res.json()

appendImage(data.image)

lastImage = data.image

}catch(err){

console.error(err)

appendMsg("bot","Erro ao gerar imagem")

}

}


// ⬇️ BAIXAR IMAGEM
function baixarImagem(){

if(!lastImage) return

const link = document.createElement("a")

link.href = "data:image/png;base64," + lastImage
link.download = "post.png"

link.click()

}


// 📋 COPIAR POST
function copiarPost(){

if(!lastPost) return

navigator.clipboard.writeText(lastPost)

appendMsg("bot","✅ Post copiado!")

}


// linkify
function linkify(text){

return text
.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,'<a href="$2" target="_blank">$1</a>')
.replace(/(https?:\/\/[^\s)]+)/g,'<a href="$1" target="_blank">$1</a>')
.replace(/\n/g,'<br>')

} 


document.getElementById("msg").addEventListener("keydown",function(e){

if(e.key==="Enter"){
enviar()
}

})
