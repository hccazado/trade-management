window.addEventListener("load", () => {

    startTime(clock)
})

function startTime() {

    clock = document.getElementById("clock")

    const now = new Date();

    clock.innerHTML = "Data: " + now.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).replace(",", " -");
}