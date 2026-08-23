const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const fileInput = document.getElementById('fileInput');

// Minta izin notifikasi browser saat web dibuka pertama kali
if (Notification.permission !== "granted") {
    Notification.requestPermission();
}

function countWords(str) {
    return str.trim().split(/\s+/).filter(word => word.length > 0).length;
}

async function sendMessage() {
    const text = userInput.value;
    const file = fileInput.files[0];

    if (!text && !file) return;

    if (countWords(text) > 1000) {
        alert("Pesan terlalu panjang! Maksimal 1000 kata.");
        return;
    }

    appendMessage(text || (file ? `Mengirim file: ${file.name}` : ""), 'user-msg');
    userInput.value = '';
    
    const loadingId = appendMessage("AI sedang mengetik...", 'ai-msg loading');

    const formData = new FormData();
    formData.append("text", text);
    if (file) formData.append("file", file);

    try {
        const response = await fetch('http://localhost:8000/api/chat', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        document.getElementById(loadingId).remove();
        
        // JIKA TERKENA BLOKIR / PAYWALL
        if (data.status === "paywall") {
            appendMessage(data.reply, 'ai-msg');
            
            // Jalankan hitung mundur notifikasi di latar belakang browser
            startNotificationTimer(data.time_left_minutes);
        } else if (data.reply) {
            appendMessage(data.reply, 'ai-msg');
        }
    } catch (error) {
        document.getElementById(loadingId).remove();
        appendMessage("Gagal terhubung ke server backend.", 'ai-msg');
    }
    
    fileInput.value = '';
}

// Fungsi pengirim notifikasi setelah waktu tunggu habis
function startNotificationTimer(minutes) {
    const msDelay = minutes * 60 * 1000;
    
    setTimeout(() => {
        if (Notification.permission === "granted") {
            new Notification("AI SMARTH GENERATIV Aktif!", {
                body: "Waktu tunggu 1 jam selesai. Kuota gratis kamu sudah di-reset. Ayo mengobrol lagi!",
                icon: "https://flaticon.com"
            });
        } else {
            alert("🔔 Notifikasi: AI SMARTH GENERATIV sudah aktif kembali!");
        }
    }, msDelay);
}

function appendMessage(text, className) {
    const msgDiv = document.createElement('div');
    const uniqueId = 'msg-' + Date.now();
    msgDiv.id = uniqueId;
    msgDiv.className = `message ${className}`;
    msgDiv.innerText = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return uniqueId;
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

