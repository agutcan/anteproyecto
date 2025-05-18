// Contador regresivo
const scheduledAt = new Date("{{ match.scheduled_at|date:'c' }}");
const countdownElement = document.getElementById("countdown");

function updateCountdown() {
    const now = new Date();
    const diff = scheduledAt - now;

    if (diff <= 0) {
        countdownElement.textContent = "¡El partido ha comenzado!";
        clearInterval(timer);
        return;
    }

    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    countdownElement.textContent = `${hours}h ${minutes}m ${seconds}s`;
}

updateCountdown();
const timer = setInterval(updateCountdown, 1000);