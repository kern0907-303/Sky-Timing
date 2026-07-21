
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
