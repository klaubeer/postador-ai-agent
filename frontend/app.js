let lang = localStorage.getItem("lang") || "pt"

// cria session id se não existir (uma por aba)
let sessionId = sessionStorage.getItem("session_id")

if (!sessionId) {
    sessionId = crypto.randomUUID()
    sessionStorage.setItem("session_id", sessionId)
}

console.log("SESSION:", sessionId)

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

const res = await fetch('http://127.0.0.1:8000/chat',{
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

const resposta =
      data.message
   || data.post
   || data.reply
   || "Erro ao gerar resposta"

appendMsg('bot', resposta)

}catch(err){

console.error(err)

appendMsg('bot','Erro ao conectar com o servidor')

}

}


function appendMsg(sender,text){

const div = document.createElement('div')

div.className = `msg ${sender}`

div.innerHTML = linkify(text)

const chat = document.getElementById('chat')

chat.appendChild(div)

chat.scrollTop = chat.scrollHeight

}


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
