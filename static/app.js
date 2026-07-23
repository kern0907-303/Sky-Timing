// App.js for Qin Tian Jian 今日天時 MVP - Local-first Interactive Engine

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

// Client-side local analyzer for instant response (even offline / static host)
function clientAnalyze(eventType, question, constraint) {
    if (typeof DAILY_TIMING === "undefined") {
        return "無法取得今日天時資訊，請重新載入網頁。";
    }
    
    const jc = DAILY_TIMING.jianchu;
    const clash = DAILY_TIMING.has_clash;
    const prim = DAILY_TIMING.primary_force;
    
    let suitability = "平順中立";
    let advice = "適合按部就班推進。";
    
    const expansion_actions = ["啟動", "合約", "情感約會", "大宗交易", "移徙入宅", "靈感企劃"];
    const consensus_actions = ["關係溝通", "商談"];
    const contraction_actions = ["關係斷捨離", "收尾", "大掃除"];
    const reflective_actions = ["冥想修行", "讀書學習", "調整", "靈感寫作", "收支結算"];
    
    if (clash) {
        if (expansion_actions.includes(eventType)) {
            suitability = "面臨阻力與考驗";
            advice = `今日日值歲破或能量衝突強烈，對於需要和諧共識或重大投入的「${eventType}」變數極多，建議放緩推進節奏，避免強求結果。`;
        } else if (consensus_actions.includes(eventType) || eventType === "靈感企劃") {
            suitability = "溝通變數增多";
            advice = `今日氣場存在交戰與沖煞，在「${eventType}」中容易出現意見分歧或思緒被打斷，建議抱持包容心，多聽少說，避免在此時做出硬性承諾。`;
        } else if (contraction_actions.includes(eventType)) {
            suitability = "阻力偏大且易耗能";
            advice = `天時能量波動劇烈，進行「${eventType}」時可能遇到拖延或突發枝節，且體力消耗較快，建議量力而行，不宜過度勉強。`;
        } else if (reflective_actions.includes(eventType)) {
            suitability = "心神易受干擾";
            advice = `今日外界干擾氣場較強，進行「${eventType}」時可能感到心神不寧或財務數據混亂。建議以小規模微調、記錄零散靈感或複習舊知識為主，避免做重大定案。`;
        } else {
            suitability = "變數與波動較多";
            advice = "天時能量存在交戰或沖煞，各類事務進展易生突發枝節，建議以彈性防禦為主，避免做重大定案。";
        }
    } else if (["建", "成", "開"].includes(jc)) {
        if (expansion_actions.includes(eventType)) {
            suitability = "深受天時支持";
            advice = `當前建除十二神氣場生機勃勃，主建立與擴充。對於向外開展、注入新生動能的「${eventType}」非常有利，能獲得強勁的順向推動力。`;
        } else if (consensus_actions.includes(eventType) || eventType === "讀書學習") {
            suitability = "有利拓展與交流";
            advice = `氣場開放，有利於「${eventType}」中的思想碰撞與秩序建立，容易達成共識或快速吸收新知識，是向外連結的極佳時機。`;
        } else if (contraction_actions.includes(eventType) || eventType === "收支結算") {
            suitability = "收斂阻力稍大";
            advice = `今日天時偏向擴張與建立，對於「${eventType}」等收尾或收納事宜容易產生拖延，建議先做評估與整理，暫緩強硬切斷。`;
        } else if (["冥想修行", "調整", "靈感寫作"].includes(eventType)) {
            suitability = "宜開啟新方向";
            advice = `今日適合為「${eventType}」規劃全新架構或開啟新篇章。適合冥想未來藍圖，或動筆寫下全新靈感的大綱框架。`;
        } else {
            suitability = "天時平順支持";
            advice = "天地氣流順暢，適合積極推動各項事務。";
        }
    } else if (["收", "閉", "執"].includes(jc)) {
        if (contraction_actions.includes(eventType) || eventType === "收支結算") {
            suitability = "極利於收斂與歸檔";
            advice = `本日能量主軸為收存與閉藏，最適合將多餘、耗能的事務收尾，或為不健康的關係/空間進行「${eventType}」整理，能獲得極佳的清明與安定力。`;
        } else if (["冥想修行", "讀書學習", "靈感寫作"].includes(eventType)) {
            suitability = "深受天時支持";
            advice = `天時氣流趨向內斂收攏，是進行「${eventType}」的黃金時機。此時心靈平靜、注意力容易集中，極易進入深度思考或靈感整理狀態。`;
        } else if (consensus_actions.includes(eventType) || eventType === "調整") {
            suitability = "偏向保守內省";
            advice = `大氣動能主收攏，在此氣流下進行「${eventType}」應避免過度強求對方的讓步，建議多從內部架構或底層邏輯進行微調，以守代攻。`;
        } else if (expansion_actions.includes(eventType)) {
            suitability = "拓展受限";
            advice = `大氣動能處於收斂封閉階段，此時若強行推動「${eventType}」等擴張性計劃，容易感到進展緩慢或反響冷淡，建議改採低調儲備與非公開測試策略。`;
        } else {
            suitability = "保守穩健為宜";
            advice = "能量趨於收縮，適合內部整理、補足細節，不宜盲目擴張。";
        }
    } else if (["破", "危", "除"].includes(jc)) {
        if (contraction_actions.includes(eventType) || eventType === "調整" || eventType === "收支結算") {
            suitability = "極佳的破舊立新時機";
            advice = `今日建除氣場帶有「破除、清除舊疾」的強大動能，若要進行「${eventType}」，能順應天時快速排除障礙、重獲新生，是除舊迎新的最佳時機。`;
        } else if (["冥想修行", "讀書學習", "靈感寫作"].includes(eventType)) {
            suitability = "適合打破瓶頸";
            advice = `今日適合打破思維定勢。在進行「${eventType}」時，若能主動挑戰難關、顛覆舊有認知或清除心靈毒素，將有突破性的收穫。`;
        } else if (consensus_actions.includes(eventType) || eventType === "靈感企劃") {
            suitability = "意見易生分歧";
            advice = `大氣中帶有碰撞與破裂的動能，進行「${eventType}」時容易因觀點不同而引發摩擦，建議保持彈性與冷靜，多加聆聽，避免情緒化爭執。`;
        } else if (expansion_actions.includes(eventType)) {
            suitability = "變數與衝突較多";
            advice = `大氣動能帶有波動與破裂之意，在此氣流下強行推動「${eventType}」等剛性契約或關係建立，容易因誤解而留下隱患，建議壓後或保持高度謹慎。`;
        } else {
            suitability = "變革與重組期";
            advice = "氣場較為波動，適合清理舊包袱，不宜草率做出重大承諾。";
        }
    }
    
    return `【天時關聯分析】：您所問的「${question}」（類型：${eventType}），在今日天時背景下，\n整體狀態呈現「${suitability}」。\n今日天時的主軸能量為「${prim}」。\n針對您提及的限制「${constraint}」：${advice}\n【建議今日採取的個人節奏】：穩健且順勢而為，不盲目逆氣場強求。`;
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
    
    // First: Run local analyzer for instant response (ensures working on GitHub Pages Static)
    setTimeout(() => {
        const localResult = clientAnalyze(eventType, question, constraint || "無特別限制");
        resultText.textContent = localResult;
    }, 300);
    
    // Second: Silently sync to backend if available (localhost FastAPI)
    try {
        await fetch("/api/daily/ask", {
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
    } catch (err) {
        // Silent catch for static hosting environments
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

// Local feedback logs display & analysis dashboard
function loadResonanceStats() {
    const statsBox = document.getElementById("resonanceStats");
    if (!statsBox) return;
    
    let feedbackLogs = JSON.parse(localStorage.getItem("qtj_feedback_logs") || "[]");
    
    if (feedbackLogs.length === 0) {
        statsBox.classList.add("hidden");
        return;
    }
    
    statsBox.classList.remove("hidden");
    
    // Calculate stats
    const total = feedbackLogs.length;
    let scoreSum = 0;
    feedbackLogs.forEach(log => {
        if (log.reaction === "resonant") scoreSum += 100;
        else if (log.reaction === "partial") scoreSum += 50;
    });
    const avgResonance = Math.round(scoreSum / total);
    
    document.getElementById("statTotal").textContent = total;
    document.getElementById("statRate").textContent = `${avgResonance}%`;
    
    // Display personalized insight
    let insight = "";
    if (avgResonance >= 80) {
        insight = "✨ 天人合一：您近期與天時運作能量高度同頻，對天時感知極其敏銳！您的直覺與步調皆符合天地氣流，多信任自身直覺即可水到渠成。";
    } else if (avgResonance >= 40) {
        insight = "⚖️ 漸入佳境：您能隱約感知環境動能的波瀾起伏。宜隨天時節奏主動微調做事步調，借力使力，即可獲得良好的平穩與助力。";
    } else {
        insight = "🌊 沉澱專注：目前您受外部氣場的影響較小，具備很強的個人自主信念。此時無須刻意迎合天時，順著自身真實想法專注前行即可。";
    }
    document.getElementById("statsInsight").textContent = insight;
    
    // Render history list
    const historyList = document.getElementById("feedbackHistoryList");
    historyList.innerHTML = "";
    
    // Show up to 5 most recent feedback entries
    const recentLogs = feedbackLogs.slice(-5).reverse();
    recentLogs.forEach(log => {
        const item = document.createElement("div");
        item.className = "history-item";
        
        const dateSpan = document.createElement("span");
        dateSpan.className = "history-date";
        dateSpan.textContent = log.date;
        
        const reactionSpan = document.createElement("span");
        reactionSpan.className = `history-reaction reaction-${log.reaction}`;
        const reactionLabels = {
            resonant: "有感",
            partial: "部分有感",
            not_resonant: "沒有感覺"
        };
        reactionSpan.textContent = reactionLabels[log.reaction] || log.reaction;
        
        item.appendChild(dateSpan);
        item.appendChild(reactionSpan);
        historyList.appendChild(item);
    });
}

// Helper to get the feedback date
function getFeedbackDate() {
    let date = null;
    const dateInput = document.getElementById("dateQuery");
    if (dateInput && dateInput.value) {
        date = dateInput.value;
    } else {
        const pathParts = window.location.pathname.split("/");
        const lastPart = pathParts[pathParts.length - 1];
        if (lastPart && lastPart.match(/^\d{4}-\d{2}-\d{2}$/)) {
            date = lastPart;
        } else {
            // Default to today's date in Taipei timezone
            const now = new Date();
            const offset = 8 * 60; // Taipei UTC+8
            const localTime = new Date(now.getTime() + (offset + now.getTimezoneOffset()) * 60000);
            date = localTime.toISOString().split('T')[0];
        }
    }
    return date;
}

// Check and pre-fill existing feedback for the current date
function checkExistingFeedback() {
    const date = getFeedbackDate();
    let feedbackLogs = JSON.parse(localStorage.getItem("qtj_feedback_logs") || "[]");
    const entry = feedbackLogs.find(log => log.date === date);
    
    if (entry) {
        // Pre-select button
        selectReaction(entry.reaction);
        
        // Pre-fill observation
        const obsInput = document.getElementById("feedbackObs");
        if (obsInput) {
            obsInput.value = entry.observation || "";
        }
        
        // Change submit button text
        const submitBtn = document.getElementById("btn-submit-feedback");
        if (submitBtn) {
            submitBtn.textContent = "更新回饋";
        }
        
        // Show success alert
        const resultBox = document.getElementById("feedbackResult");
        const resultText = document.getElementById("feedbackResultText");
        if (resultBox && resultText) {
            resultBox.classList.remove("hidden");
            resultText.textContent = "今天已成功記錄至您的天時日記，您可以隨時修改更新！";
        }
    }
}

async function submitFeedback() {
    const observation = document.getElementById("feedbackObs").value;
    const date = getFeedbackDate();
    const anonymous_session_id = getAnonymousSessionId();
    const resultBox = document.getElementById("feedbackResult");
    const resultText = document.getElementById("feedbackResultText");
    
    if (!selectedReactionValue) {
        alert("請選擇今天的狀態反饋（有感、部分有感、沒有感覺）。");
        return;
    }
    
    resultBox.classList.remove("hidden");
    resultText.textContent = "已成功記錄至您本地的天時日記！";
    
    // Update button text to show update capability
    const submitBtn = document.getElementById("btn-submit-feedback");
    if (submitBtn) {
        submitBtn.textContent = "更新回饋";
    }
    
    // 1. Save locally to LocalStorage
    let feedbackLogs = JSON.parse(localStorage.getItem("qtj_feedback_logs") || "[]");
    const existingIndex = feedbackLogs.findIndex(log => log.date === date);
    const newEntry = {
        date: date,
        reaction: selectedReactionValue,
        observation: observation || null,
        timestamp: new Date().toISOString()
    };
    
    if (existingIndex > -1) {
        feedbackLogs[existingIndex] = newEntry;
    } else {
        feedbackLogs.push(newEntry);
    }
    localStorage.setItem("qtj_feedback_logs", JSON.stringify(feedbackLogs));
    
    // 3. Update and show the stats analyzer immediately
    loadResonanceStats();
    
    // 4. Silently sync to backend if available (FastAPI)
    try {
        await fetch("/api/daily/feedback", {
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
    } catch (err) {
        // Silent catch for static hosting environments
    }
}

// Automatically load resonance statistics on page load
document.addEventListener("DOMContentLoaded", () => {
    loadResonanceStats();
    checkExistingFeedback();
});
