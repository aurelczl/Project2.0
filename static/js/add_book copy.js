// static/book_form.js

export function initBookForm() {
    const titleInput = document.getElementById('id_title');
    if (!titleInput) return; // Si pas sur un formulaire de livre
    
    const suggestionsBox = document.getElementById('title-suggestions-openlib');
    let currentSource = 'openlibrary';

    // Gestion du changement de source
    document.querySelectorAll('.btn-source').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.btn-source').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentSource = this.dataset.source;
            suggestionsBox.innerHTML = '';
        });
    });

    titleInput.addEventListener('input', async function() {
        const query = this.value.trim();
        if (query.length < 3) {
            suggestionsBox.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/api/book-suggestions/?source=${currentSource}&q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Erreur réseau');
            
            const items = await response.json();
            displaySuggestions(items, titleInput, suggestionsBox);
        } catch (error) {
            console.error('Error:', error);
            suggestionsBox.innerHTML = '<div class="suggestion-item">Erreur de chargement</div>';
        }
    });

    // Fermer les suggestions quand on clique ailleurs
    document.addEventListener('click', (e) => {
        if (!titleInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.innerHTML = '';
        }
    });
}

function displaySuggestions(items, titleInput, suggestionsBox) {
    suggestionsBox.innerHTML = '';
    
    if (!items || items.length === 0) {
        suggestionsBox.innerHTML = '<div class="suggestion-item">Aucun résultat trouvé</div>';
        return;
    }

    items.forEach(item => {
        const div = document.createElement('div');
        div.innerHTML = `
            <strong>${item.title}</strong>
            ${item.author ? `<br><small>${item.author}</small>` : ''}
            <small class="source-badge">${item.source}</small>
        `;
        
        div.classList.add('suggestion-item');
        div.addEventListener('click', () => {
            titleInput.value = item.title;
            suggestionsBox.innerHTML = '';
            fillBookDetails(item);
        });
        
        suggestionsBox.appendChild(div);
    });
}

function fillBookDetails(item) {
    if (item.author) {
        const authorField = document.getElementById('id_author');
        if (authorField) authorField.value = item.author;
    }
    
    if (item.source === 'openlibrary' && item.cover_id) {
        const imageUrl = `https://covers.openlibrary.org/b/id/${item.cover_id}-M.jpg`;
        updateBookCover(imageUrl);
    }
}

function updateBookCover(imageUrl) {
    let imageContainer = document.getElementById('cover-image-container');
    if (!imageContainer) {
        imageContainer = document.createElement('div');
        imageContainer.id = 'cover-image-container';
        document.getElementById('id_title').parentNode.insertAdjacentElement('afterend', imageContainer);
    }
    imageContainer.innerHTML = `<img src="${imageUrl}" style="max-height:200px; margin-top:10px;">`;
}