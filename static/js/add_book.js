// static/js/add_book_v2.js


export function initBookForm() {
    const titleInput = document.getElementById('id_title');
    if (!titleInput) return;

    const suggestionsBox = document.getElementById('title-suggestions-openlib');
    let currentSource = 'library'; // Source par défaut = votre bibliothèque

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
            let items = [];
            
            // Recherche d'abord dans votre bibliothèque
            if (currentSource === 'library') {
                const response = await fetch(`/api/search-books/?q=${encodeURIComponent(query)}`);
                if (!response.ok) throw new Error('Erreur réseau');
                items = await response.json();
                
                // Si aucun résultat, chercher dans les autres sources
                if (items.length === 0 && document.querySelector('.btn-source[data-source="openlibrary"]')) {
                    currentSource = 'openlibrary';
                    document.querySelector('.btn-source[data-source="openlibrary"]').click();
                    return;
                }
            } else {
                // Recherche dans les APIs externes
                const response = await fetch(`/api/book-suggestions/?source=${currentSource}&q=${encodeURIComponent(query)}`);
                if (!response.ok) throw new Error('Erreur réseau');
                items = await response.json();
            }
            
            displaySuggestions(items, titleInput, suggestionsBox, currentSource);
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

function displaySuggestions(items, titleInput, suggestionsBox, source) {
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
            <small class="source-badge">${source === 'library' ? 'Ma Bibliothèque' : source}</small>
        `;
        
        div.classList.add('suggestion-item');
        div.addEventListener('click', async () => {
            titleInput.value = item.title;
            suggestionsBox.innerHTML = '';
            
            // Si c'est de notre bibliothèque, on a déjà toutes les infos
            if (source === 'library') {
                // Solution dynamique - remplace tout updateBookDetails
                Object.keys(item).forEach(key => {
                    const field = document.getElementById(`id_${key}`);
                    if (field && field.type !== 'hidden' && item[key]) {
                        field.value = item[key];
                    }
                });

                // Gestion spéciale de l'image
                if (item.image_url) {
                    updateBookCover(item.image_url);
                }

                // Champ caché pour PublicBook existant
                let hiddenField = document.getElementById('public_book_id');
                if (!hiddenField) {
                    hiddenField = document.createElement('input');
                    hiddenField.type = 'hidden';
                    hiddenField.id = 'public_book_id';
                    hiddenField.name = 'public_book_id';
                    titleInput.parentNode.appendChild(hiddenField);
                }
                hiddenField.value = item.id;
            } else {
                const bookDetails = await fetchCompleteBookDetails(item.title, source);
                // Gardez l'ancienne méthode pour les sources externes
                updateBookDetails({...item, ...bookDetails});
            }
        });
        
        suggestionsBox.appendChild(div);
    });
}

// ... (le reste des fonctions reste inchangé)

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
    // Liste des champs spécifiques aux APIs externes
    const apiFields = {
        'author': 'id_author',
        'edition': 'id_edition', 
        'pageCount': 'id_pageCount',
        'cover_id': null, // Géré séparément
        'cover_url': null
    };

    // Remplissage des champs standards
    Object.entries(apiFields).forEach(([key, fieldId]) => {
        if (fieldId && item[key]) {
            const field = document.getElementById(fieldId);
            if (field) field.value = item[key];
        }
    });

    // Gestion spéciale des images
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