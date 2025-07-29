// static/js/add_book.js

export function initBookForm() {
    const titleInput = document.getElementById('id_title');
    if (!titleInput) return;

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

    titleInput.addEventListeneconnr('input', async function() {
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
        div.addEventListener('click', async () => {
            titleInput.value = item.title;
            suggestionsBox.innerHTML = '';
            
            const bookDetails = await fetchCompleteBookDetails(item.title, item.source);
            updateBookDetails({...item, ...bookDetails});
        });
        
        suggestionsBox.appendChild(div);
    });
}

async function fetchCompleteBookDetails(title, source) {
    try {
        const response = await fetch(`/api/fetch-book-info/?title=${encodeURIComponent(title)}&source=${source}`);
        if (!response.ok) throw new Error('Erreur réseau');
        return await response.json();
    } catch (error) {
        console.error('Erreur:', error);
        return {};
    }
}

function updateBookDetails(item) {
    // Remplir l'auteur
    if (item.author) {
        const authorField = document.getElementById('id_author');
        if (authorField) authorField.value = item.author;
    }
    
    // Remplir l'édition
    if (item.edition) {
        const editionField = document.getElementById('id_edition');
        if (editionField) editionField.value = item.edition;
    }
    
    // Remplir le nombre de pages
    if (item.pageCount) {
        const pageCountField = document.getElementById('id_pageCount');
        if (pageCountField) pageCountField.value = item.pageCount;
    }
    
    // Gestion des images
    if (item.source === 'openlibrary' && item.cover_id) {
        updateBookCover(`https://covers.openlibrary.org/b/id/${item.cover_id}-M.jpg`);
    } 
    else if ((item.source === 'babelio' || item.source === 'booknode') && item.cover_url) {
        const fullUrl = item.cover_url.startsWith('http') ? item.cover_url : `https://www.babelio.com${item.cover_url}`;
        updateBookCover(fullUrl);
    }
}

function updateBookCover(imageUrl) {
    let imageContainer = document.getElementById('cover-image-container');
    if (!imageContainer) {
        imageContainer = document.createElement('div');
        imageContainer.id = 'cover-image-container';
        imageContainer.style.marginTop = '10px';
        document.getElementById('id_title').parentNode.insertAdjacentElement('afterend', imageContainer);
    }
    
    imageContainer.innerHTML = `
        <img src="${imageUrl}" 
             style="max-height:200px; border:1px solid #ddd; border-radius:4px;"
             onerror="this.style.display='none'">
        <button type="button" class="remove-cover" 
                style="margin-left:10px; color:red; background:none; border:none; cursor:pointer;">
            × Supprimer
        </button>
    `;
    
    // Gestion du bouton de suppression
    imageContainer.querySelector('.remove-cover').addEventListener('click', () => {
        imageContainer.innerHTML = '';
        const imageUrlField = document.getElementById('id_image_url_field');
        if (imageUrlField) imageUrlField.value = '';
    });
}