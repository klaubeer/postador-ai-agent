async function enviar(){

const input = document.getElementById('msg');
const texto = input.value.trim();

if(!texto) return;

appendMsg('user', texto);

input.value = '';

const res = await fetch('https://postador-ai-agent.onrender.com/chat',{
method:'POST',
headers:{
'Content-Type':'application/json'
},
body:JSON.stringify({
message:texto,
sessionId:'web-demo'
})
});

const data = await res.json();

appendMsg('bot', data.reply || 'Erro ao gerar resposta');

}

function appendMsg(sender,text){

const div=document.createElement('div');

div.className=`msg ${sender}`;

div.innerHTML=linkify(text);

document.getElementById('chat').appendChild(div);

document.getElementById('chat').scrollTop=
document.getElementById('chat').scrollHeight;

}

function linkify(text){

return text
.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,'<a href="$2" target="_blank">$1</a>')
.replace(/(https?:\/\/[^\s)]+)/g,'<a href="$1" target="_blank">$1</a>')
.replace(/\n/g,'<br>');

}
