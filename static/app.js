// App.js for Qin Tian Jian 今日天時 MVP

function queryDate() {
    const dateInput = document.getElementById("dateQuery").value;
    if (dateInput) {
        window.location.href = `/date/${dateInput}`;
    }
}

function toggleAskForm() {
    const form = document.getElementById("askForm");
    const triggerBtn = document.querySelector(".ask-trigger-container button");
    
    if (form.classList.contains("ask-form-hidden")) {
        form.className = "ask-form-visible";
        triggerBtn.textContent = "隱藏問事面板";
    } else {
        form.className = "ask-form-hidden";
        triggerBtn.textContent = "展開問事面板";
    }
}

async function submitAskQuery() {
    const question = document.getElementById("actionInput").value;
    const eventType = document.getElementById("eventType").value;
    const constraint = document.getElementById("constraintInput").value;
    const date = document.getElementById("dateQuery").value;
    
    const resultBox = document.getElementById("askResult");
    const resultText = document.getElementById("askResultText");
    
    if (!question) {
        alert("請輸入您正在考慮的事務項目。");
        return;
    }
    
    resultBox.className = "ask-result-container";
    resultText.textContent = "正在透過今日天時運行分析關聯...";
    
    try {
        const response = await fetch("/api/daily/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                event_type: eventType,
                constraint: constraint || "無特別限制",
                date: date
            })
        });
        
        if (!response.ok) {
            throw new Error("API request failed.");
        }
        
        const data = await response.json();
        if (data.status === "success") {
            resultText.textContent = data.response;
        } else {
            resultText.textContent = "分析失敗，請重試。";
        }
    } catch (err) {
        console.error(err);
        resultText.textContent = "無法連接分析伺服器，請確認伺服器已開啟。";
    }
}

// Anonymous Session ID generation/retrieval
function getAnonymousSessionId() {
    let sid = localStorage.getItem("qtj_anonymous_session_id");
    if (!sid) {
        sid = 'sess_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        localStorage.setItem("qtj_anonymous_session_id", sid);
    }
    return sid;
}

let selectedReactionValue = null;

function selectReaction(reaction) {
    selectedReactionValue = reaction;
    
    // Toggle active state for buttons
    const btnIds = ["btn-resonant", "btn-partial", "btn-not_resonant"];
    btnIds.forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
            if (id === `btn-${reaction}`) {
                btn.classList.add("selected");
            } else {
                btn.classList.remove("selected");
            }
        }
    });
    
    // Show text area group
    const obsGroup = document.getElementById("observationGroup");
    if (obsGroup) {
        obsGroup.classList.remove("hidden");
    }
}

async function submitFeedback() {
    const observation = document.getElementById("feedbackObs").value;
    const date = document.getElementById("dateQuery").value;
    const anonymous_session_id = getAnonymousSessionId();
    
    const resultBox = document.getElementById("feedbackResult");
    const resultText = document.getElementById("feedbackResultText");
    
    if (!selectedReactionValue) {
        alert("請選擇今天的狀態反饋（有感、部分有感、沒有感覺）。");
        return;
    }
    
    resultBox.className = "feedback-result-container";
    resultText.textContent = "正在提交反饋...";
    
    try {
        const response = await fetch("/api/daily/feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                date: date,
                reaction: selectedReactionValue,
                observation: observation || null,
                anonymous_session_id: anonymous_session_id
            })
        });
        
        if (!response.ok) {
            throw new Error("Feedback API failed.");
        }
        
        const data = await response.json();
        resultText.textContent = data.message;
        
        if (data.status === "success") {
            // Hide feedback inputs on success to prevent double submission
            document.getElementById("observationGroup").classList.add("hidden");
            document.querySelector(".feedback-buttons").style.pointerEvents = "none";
        }
    } catch (err) {
        console.error(err);
        resultText.textContent = "無法連接反饋伺服器，請重試。";
    }
}
