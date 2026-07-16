
function queryDate() {
    const dateInput = document.getElementById("dateQuery").value;
    if (dateInput) {
        window.location.href = `../date/${dateInput}.html`;
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
// Ask submission is dynamic (only works if FastAPI backend is alive, otherwise logs warning)
async function submitAskQuery() {
    alert("動態問事關聯分析功能僅在本地運行 (FastAPI) 時支援，靜態 GitHub Pages 僅提供今日天時瀏覽。");
}
