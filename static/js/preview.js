document.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript carregado e pronto!");

    // Função para leitura de texto em voz alta usando Web Speech API
    function readTextAloud(text) {
        if ('speechSynthesis' in window) {
            console.log("Iniciando leitura do texto:", text);
            const speech = new SpeechSynthesisUtterance(text);
            speech.lang = 'pt-BR';

            // Tratamento de erro
            speech.onerror = (event) => {
                console.error("Erro na leitura em voz alta:", event);
            };

            // Falar o texto
            window.speechSynthesis.speak(speech);
        } else {
            alert('Seu navegador não suporta leitura em voz alta.');
            console.error('speechSynthesis não está disponível no navegador.');
        }
    }

    // Adicionar eventos para botões de leitura
    const readButtons = document.querySelectorAll(".btn-read-aloud");
    if (readButtons.length === 0) {
        console.error("Nenhum botão de leitura encontrado na página.");
    }

    readButtons.forEach(button => {
        button.addEventListener("click", () => {
            const textToRead = button.getAttribute("data-text");
            if (textToRead) {
                console.log("Texto para leitura:", textToRead);
                readTextAloud(textToRead);
            } else {
                console.error("Texto para leitura está vazio.");
            }
        });
    });
});
