/* =========================================
   FUNKCE PRO ŠUPLÍK ANALÝZY
========================================= */
let analysisOpen = false;

window.toggleAnalysis = function() {
    analysisOpen = !analysisOpen;
    const content = document.getElementById('analysis-content');
    const arrow = document.getElementById('analysis-arrow');
    
    if (content && arrow) {
        content.style.display = analysisOpen ? "block" : "none";
        arrow.textContent = analysisOpen ? "▲" : "▼";
    }
};

/* =========================================
   SYSTÉM 3 BAREVNÝCH REŽIMŮ (Light / Dark / Sand)
========================================= */
window.setTheme = function(theme) {
    document.body.classList.remove('dark-mode', 'sand-mode');
    
    // Univerzální hledání tlačítka podle jeho akce
    const themeBtn = document.querySelector('button[onclick*="toggleDarkMode"]');
    
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeBtn) themeBtn.textContent = '☕'; // Ikonka: Z tmavého půjdeme do pískového
    } else if (theme === 'sand') {
        document.body.classList.add('sand-mode');
        if (themeBtn) themeBtn.textContent = '☀️'; // Ikonka: Z pískového půjdeme do světlého
    } else {
        // Světlý režim
        if (themeBtn) themeBtn.textContent = '🌙'; // Ikonka: Ze světlého půjdeme do tmy
    }
    
    localStorage.setItem('gita_theme', theme); // Změnil jsem klíč na gita_theme
};

// Zpětná kompatibilita a inicializace při načtení
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('gita_theme') || 'light';
    setTheme(savedTheme);
});

// Přepínání přes tlačítko
window.toggleDarkMode = function() {
    const currentTheme = localStorage.getItem('gita_theme') || 'light';
    
    if (currentTheme === 'light') {
        setTheme('dark');
    } else if (currentTheme === 'dark') {
        setTheme('sand');
    } else {
        setTheme('light');
    }
};