document.addEventListener('DOMContentLoaded', function() {
    const chatButton = document.getElementById('chatbot-button');
    const chatWindow = document.getElementById('chatbot-window');
    const closeButton = document.querySelector('.chatbot-close');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.querySelector('.typing-indicator');
    
    // Toggle chat window
    chatButton.addEventListener('click', function() {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            chatInput.focus();
        }
    });

    // Close chat window
    closeButton.addEventListener('click', function(e) {
        e.stopPropagation();
        chatWindow.classList.remove('active');
    });

    // Send message on Enter key
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && chatInput.value.trim() !== '') {
            sendMessage();
        }
    });

    // Send message when send button is clicked
    const sendButton = document.querySelector('.chatbot-input button');
    sendButton.addEventListener('click', function() {
        if (chatInput.value.trim() !== '') {
            sendMessage();
        }
    });

    // Send message function
    // ... các đoạn code cũ giữ nguyên ...

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (message === '') return;

        // Hiển thị tin nhắn User
        addMessage(message, 'user');
        chatInput.value = '';
        
        showTypingIndicator();
        
        try {
            // Gửi đến Django View bạn vừa tạo
            const response = await fetch('/chatbot/ask/', { // Hãy đảm bảo URL này khớp với urls.py
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Django yêu cầu CSRF token cho POST
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) throw new Error('Lỗi phản hồi từ server');

            const data = await response.json();
            
            hideTypingIndicator();
            
            // Hiển thị câu trả lời cuối cùng từ API 8001
            addMessage(data.reply, 'bot');

        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage('Xin lỗi, tôi gặp khó khăn khi kết nối với máy chủ.', 'bot');
        }
    }

    // Đừng quên hàm lấy CSRF Token để không bị lỗi 403
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender + '-message');
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'flex';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Add initial greeting
    window.addEventListener('load', function() {
        setTimeout(() => {
            addMessage('Xin chào! Tôi là trợ lý ảo của cửa hàng. Tôi có thể giúp gì cho bạn hôm nay?', 'bot');
        }, 1000);
    });
});
