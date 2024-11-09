document.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript carregado!");

    const imagemLinkInput = document.getElementById('imagemLink');
    const imagemUploadInput = document.getElementById('imagemUpload');
    const previewImage = document.getElementById('previewImage');

    if (!imagemLinkInput) {
        console.error("Elemento com ID 'imagemLink' não encontrado!");
    }

    if (!imagemUploadInput) {
        console.error("Elemento com ID 'imagemUpload' não encontrado!");
    }

    if (!previewImage) {
        console.error("Elemento com ID 'previewImage' não encontrado!");
    }

    // Atualizar pré-visualização ao inserir o link da imagem
    imagemLinkInput?.addEventListener('input', () => {
        const link = imagemLinkInput.value;
        console.log("Link da imagem inserido:", link);
        if (link) {
            previewImage.src = link;
        }
    });

    // Atualizar pré-visualização ao fazer upload da imagem
    imagemUploadInput?.addEventListener('change', (event) => {
        const file = event.target.files[0];
        console.log("Imagem upload:", file);
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                console.log("Imagem carregada:", e.target.result);
                previewImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
