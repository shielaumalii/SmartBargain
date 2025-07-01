// === CSRF Token Setup ===
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// 1. Load Contact Messages for Seller Dashboard
let contactMessages = [];
let currentMessagePage = 1;
const messagesPerPage = 5;

function loadContactMessages(status = 'all', date = null) {
    fetch('/get_contact_messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ status, date })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            contactMessages = data.messages;
            renderContactMessages(contactMessages);
        } else {
            alert('Error loading messages.');
        }
    });
}


function renderContactMessages(messages) {
    const tbody = document.getElementById('messagesTableBody');
    const noData = document.getElementById('noMessagesRow');
    tbody.innerHTML = '';

    const startIndex = (currentMessagePage - 1) * messagesPerPage;
    const endIndex = startIndex + messagesPerPage;
    const pageMessages = messages.slice(startIndex, endIndex);

    if (!pageMessages || pageMessages.length === 0) {
        noData.style.display = '';
        return;
    }

    noData.style.display = 'none';

    pageMessages.forEach(msg => {
        const tr = document.createElement('tr');
        tr.onclick = () => showMessageModal(msg);
        tr.innerHTML = `
            <td style="padding: 8px;">${msg.name}</td>
            <td style="padding: 8px; text-align: center;">${msg.status}</td>
            <td style="padding: 8px; text-align: center;">${new Date(msg.date).toLocaleDateString()}</td>
        `;
        tbody.appendChild(tr);
    });

    renderMessagePagination(); // render page buttons
}

function renderMessagePagination() {
    const container = document.getElementById('messagePagination');
    container.innerHTML = '';

    const totalPages = Math.ceil(contactMessages.length / messagesPerPage);
    if (totalPages <= 1) return;

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.className = i === currentMessagePage ? 'active-page-btn' : 'page-btn';
        btn.onclick = () => {
            currentMessagePage = i;
            renderContactMessages(contactMessages);
        };
        container.appendChild(btn);
    }
}



// 2. Show Modal with Message Detail
function showMessageModal(msg) {
    document.getElementById('modalMsgName').innerText = msg.name;
    document.getElementById('modalMsgEmail').innerText = msg.email;
    document.getElementById('modalMsgMessage').innerText = msg.message;
    document.getElementById('modalMsgStatus').innerText = msg.status;
    document.getElementById('modalMsgDate').innerText = new Date(msg.date).toLocaleString();
    document.getElementById('messageModal').dataset.messageId = msg.id;
    document.getElementById('messageModal').style.display = 'block';
}

function closeMessageModal() {
    document.getElementById('messageModal').style.display = 'none';
}

function replyToMessage() {
    alert('Reply feature coming soon.');
}

// 3. Close a Contact Message (from Seller Dashboard)
function closeMessageThread() {
    const msgId = document.getElementById('messageModal').dataset.messageId;

    fetch('/close_contact_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ id: msgId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Message marked as closed.');
            closeMessageModal();
            loadContactMessages();  // reload dashboard
        } else {
            alert('Error closing message.');
        }
    });
}

// 4. Submit Contact Message (for Public Form)
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contactForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const name = document.getElementById("contactName").value.trim();
            const email = document.getElementById("contactEmail").value.trim();
            const message = document.getElementById("contactMessage").value.trim();
            const feedback = document.getElementById("contactFeedback");

            if (!name || !email || !message) {
                feedback.style.color = 'red';
                feedback.innerText = "All fields are required.";
                return;
            }

            fetch("/submit_contact_message/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ name, email, message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    feedback.style.color = 'green';
                    feedback.innerText = "Your message was submitted successfully.";
                    form.reset();
                } else {
                    feedback.style.color = 'red';
                    feedback.innerText = data.error || "Submission failed.";
                }
            })
            .catch(() => {
                feedback.style.color = 'red';
                feedback.innerText = "Network error. Please try again later.";
            });
        });
    }

    // === CONTACT MESSAGE FILTERS ===
    const statusFilter = document.getElementById("messageStatusFilter");
    const dateFilter = document.getElementById("messageDateFilter");

    function applyMessageFilters() {
        const status = statusFilter ? statusFilter.value : "all";
        const date = dateFilter ? dateFilter.value : null;
        currentMessagePage = 1;
        loadContactMessages(status, date);
    }

    if (statusFilter) {
        statusFilter.addEventListener("change", applyMessageFilters);
    }

    if (dateFilter) {
        dateFilter.addEventListener("change", applyMessageFilters);
    }

    // Auto-load messages if the table exists
    if (document.getElementById("messagesTableBody")) {
        loadContactMessages();  // default: all, no date
    }
});

function clearMessageFilters() {
    const statusFilter = document.getElementById('messageStatusFilter');
    const dateFilter = document.getElementById('messageDateFilter');

    if (statusFilter) statusFilter.value = 'all';
    if (dateFilter) dateFilter.value = '';

    currentMessagePage = 1;
    loadContactMessages('all', null);
}



