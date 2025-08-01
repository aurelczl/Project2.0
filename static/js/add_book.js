// static/js/add_book.js

export function initBookForm() {
    const titleInput = document.getElementById('id_title');
    if (!titleInput) return;

    const suggestionsBox = document.getElementById('title-suggestions-openlib');
    let currentSource = 'library';

    // Style de la boîte de suggestions
    suggestionsBox.style.position = 'absolute';
    suggestionsBox.style.zIndex = '1000';
    suggestionsBox.style.backgroundColor = '#f9f6ee';
    suggestionsBox.style.border = '1px solid #8b7a5e';
    suggestionsBox.style.borderRadius = '4px';
    suggestionsBox.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
    suggestionsBox.style.width = '100%';
    suggestionsBox.style.maxWidth = '800px';
    suggestionsBox.style.display = 'none';

    // Positionnement de la boîte de suggestions
    function positionSuggestionsBox() {
        const rect = titleInput.getBoundingClientRect();
        suggestionsBox.style.top = `${rect.bottom + window.scrollY}px`;
        suggestionsBox.style.left = `${rect.left + window.scrollX}px`;
        suggestionsBox.style.width = `${rect.width}px`;
    }

    // Gestion du changement de source
    document.querySelectorAll('.btn-source').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            document.querySelectorAll('.btn-source').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentSource = this.dataset.source;
            suggestionsBox.innerHTML = '';
            suggestionsBox.style.display = 'none';
            
            if (titleInput.value.trim().length >= 3) {
                handleSearch(titleInput.value.trim());
            }
        });
    });

    // Recherche avec délai
    let searchTimeout;
    titleInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = this.value.trim();
            if (query.length < 3) {
                suggestionsBox.innerHTML = '';
                suggestionsBox.style.display = 'none';
                return;
            }
            handleSearch(query);
        }, 300);
    });

    // Gestion de la recherche (inchangée)
    async function handleSearch(query) {
        try {
            let items = [];
            let endpoint = currentSource === 'library' 
                ? `/api/search-books/?q=${encodeURIComponent(query)}`
                : `/api/book-suggestions/?source=${currentSource}&q=${encodeURIComponent(query)}`;

            const response = await fetch(endpoint);
            if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);
            
            items = await response.json();
            
            if (!Array.isArray(items)) throw new Error('Format de données invalide');

            if (items.length > 0) {
                displaySuggestions(items);
                suggestionsBox.style.display = 'block';
                positionSuggestionsBox();
            } else {
                showNoResults();
            }
        } catch (error) {
            console.error('Erreur:', error);
            showError();
        }
    }

    // NOUVELLE VERSION DE L'AFFICHAGE DES SUGGESTIONS
    function displaySuggestions(items) {
        suggestionsBox.innerHTML = '';
        
        items.forEach(item => {
            const suggestionItem = document.createElement('div');
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.style.display = 'flex';
            suggestionItem.style.padding = '10px';
            suggestionItem.style.cursor = 'pointer';
            suggestionItem.style.borderBottom = '1px solid #e8e0d0';
            suggestionItem.style.alignItems = 'center';
            suggestionItem.style.gap = '15px';
            
            // Image du livre (si disponible)
            const imageUrl = item.image_url || 
                           (item.cover_id ? `https://covers.openlibrary.org/b/id/${item.cover_id}-S.jpg` : '');
            
            if (imageUrl) {
                const imgContainer = document.createElement('div');
                imgContainer.style.flexShrink = '0';
                imgContainer.style.width = '40px';
                imgContainer.style.height = '60px';
                imgContainer.style.display = 'flex';
                imgContainer.style.alignItems = 'center';
                imgContainer.style.justifyContent = 'center';
                imgContainer.style.backgroundColor = '#e8e0d0';
                imgContainer.style.overflow = 'hidden';
                
                imgContainer.innerHTML = `
                    <img src="${imageUrl}" 
                         style="max-height:100%; max-width:100%; object-fit: contain;"
                         onerror="this.style.display='none'">
                `;
                suggestionItem.appendChild(imgContainer);
            } else {
                // Placeholder si pas d'image
                const placeholder = document.createElement('div');
                placeholder.style.flexShrink = '0';
                placeholder.style.width = '40px';
                placeholder.style.height = '60px';
                placeholder.style.backgroundColor = '#e8e0d0';
                placeholder.style.display = 'flex';
                placeholder.style.alignItems = 'center';
                placeholder.style.justifyContent = 'center';
                placeholder.innerHTML = '📚';
                suggestionItem.appendChild(placeholder);
            }

            // Détails texte (titre + auteur)
            const textContainer = document.createElement('div');
            textContainer.style.flexGrow = '1';
            textContainer.style.minWidth = '0';
            
            textContainer.innerHTML = `
                <div style="font-weight:bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.title || 'Titre inconnu'}</div>
                ${item.author ? `<div style="font-size:0.9em; color:#666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.author}</div>` : ''}
            `;
            suggestionItem.appendChild(textContainer);

            // Gestion du clic (inchangée)
            suggestionItem.addEventListener('click', () => {
                titleInput.value = item.title;
                suggestionsBox.style.display = 'none';
                
                // Remplissage automatique de tous les champs
                fillFormFields({
                    author: item.author,
                    edition: item.edition,
                    pageCount: item.pageCount
                });

                // Gestion de l'image
                if (imageUrl) {
                    updateBookCover(imageUrl);
                }

                // Mise à jour de l'ID PublicBook si c'est de notre bibliothèque
                if (currentSource === 'library' && item.id) {
                    updatePublicBookId(item.id);
                }
            });

            // Effet hover
            suggestionItem.addEventListener('mouseenter', () => {
                suggestionItem.style.backgroundColor = '#e8e0d0';
            });
            
            suggestionItem.addEventListener('mouseleave', () => {
                suggestionItem.style.backgroundColor = '';
            });
            
            suggestionsBox.appendChild(suggestionItem);
        });
    }

    // Les fonctions suivantes restent inchangées
    function fillFormFields(fields) {
        Object.entries(fields).forEach(([name, value]) => {
            if (value) {
                const field = document.getElementById(`id_${name}`);
                if (field) field.value = value;
            }
        });
    }

    function updatePublicBookId(id) {
        let hiddenField = document.getElementById('public_book_id');
        if (!hiddenField) {
            hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.id = 'public_book_id';
            hiddenField.name = 'public_book_id';
            titleInput.parentNode.appendChild(hiddenField);
        }
        hiddenField.value = id;
    }

    function updateBookCover(imageUrl) {
        let imageContainer = document.getElementById('cover-image-container');
        if (!imageContainer) {
            imageContainer = document.createElement('div');
            imageContainer.id = 'cover-image-container';
            imageContainer.style.marginTop = '15px';
            document.getElementById('id_title').parentNode.insertAdjacentElement('afterend', imageContainer);
        }
        
        imageContainer.innerHTML = `
            <img src="${imageUrl}" 
                 style="max-height:150px; border:1px solid #ddd; border-radius:4px;"
                 onerror="this.style.display='none'">
            <button type="button" class="remove-cover" 
                    style="margin-left:10px; color:red; background:none; border:none; cursor:pointer;">
                × Supprimer
            </button>
        `;
        
        imageContainer.querySelector('.remove-cover').addEventListener('click', () => {
            imageContainer.innerHTML = '';
            const imageUrlField = document.getElementById('id_image_url');
            if (imageUrlField) imageUrlField.value = '';
        });
    }

    function showNoResults() {
        suggestionsBox.innerHTML = '<div style="padding:10px; text-align:center;">Aucun résultat trouvé</div>';
        suggestionsBox.style.display = 'block';
        positionSuggestionsBox();
    }

    function showError() {
        suggestionsBox.innerHTML = '<div style="padding:10px; color:red; text-align:center;">Erreur de chargement</div>';
        suggestionsBox.style.display = 'block';
        positionSuggestionsBox();
    }

    // Gestion des événements (inchangée)
    document.addEventListener('click', (e) => {
        if (!titleInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = 'none';
        }
    });

    titleInput.addEventListener('focus', positionSuggestionsBox);
    window.addEventListener('resize', positionSuggestionsBox);
}