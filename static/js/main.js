// Handle post reactions
function handleReaction(postId, reactionType, emoji = null) {
    const formData = new FormData();
    formData.append('type', reactionType);
    if (emoji) formData.append('emoji', emoji);

    fetch(`/post/${postId}/react`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const button = document.querySelector(`[data-reaction="${reactionType}"][data-post="${postId}"]`);
        const counter = button.querySelector('.reaction-count');
        
        if (data.status === 'added') {
            button.classList.add('active');
            if (counter) counter.textContent = parseInt(counter.textContent) + 1;
        } else if (data.status === 'removed') {
            button.classList.remove('active');
            if (counter) counter.textContent = parseInt(counter.textContent) - 1;
        }
    })
    .catch(error => console.error('Error:', error));
}

// Preview markdown content
function previewMarkdown(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    if (input && preview) {
        input.addEventListener('input', function() {
            fetch('/api/preview-markdown', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ content: input.value })
            })
            .then(response => response.json())
            .then(data => {
                preview.innerHTML = data.html;
            })
            .catch(error => console.error('Error:', error));
        });
    }
}

// Handle comment form submission
function handleCommentSubmit(event, postId) {
    event.preventDefault();
    const form = event.target;
    const content = form.querySelector('textarea[name="content"]').value;

    fetch(`/post/${postId}/comment`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Append new comment to the list
            const commentsList = document.querySelector('.comments-list');
            commentsList.insertAdjacentHTML('afterbegin', data.html);
            form.reset();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Handle infinite scroll for posts
let isLoading = false;
let currentPage = 1;

function loadMorePosts() {
    if (isLoading) return;
    
    const postsContainer = document.querySelector('.posts-container');
    if (!postsContainer) return;
    
    const loadMoreTrigger = document.querySelector('.load-more-trigger');
    if (!loadMoreTrigger) return;
    
    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !isLoading) {
            isLoading = true;
            currentPage++;
            
            fetch(`/api/posts?page=${currentPage}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.posts.length > 0) {
                    postsContainer.insertAdjacentHTML('beforeend', data.html);
                    isLoading = false;
                } else {
                    observer.unobserve(loadMoreTrigger);
                    loadMoreTrigger.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                isLoading = false;
            });
        }
    });
    
    observer.observe(loadMoreTrigger);
}

// Initialize features when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize markdown preview
    previewMarkdown('content', 'preview');
    
    // Initialize infinite scroll
    loadMorePosts();
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Handle file upload preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const preview = document.querySelector('.image-preview');
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Handle tag input
function initializeTagInput() {
    const tagInput = document.querySelector('.tag-input');
    if (!tagInput) return;
    
    tagInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            const tag = this.value.trim();
            if (tag) {
                const tagsContainer = document.querySelector('.tags-container');
                const tagElement = document.createElement('span');
                tagElement.className = 'tag';
                tagElement.textContent = tag;
                tagElement.innerHTML += '<button type="button" class="tag-remove">&times;</button>';
                tagsContainer.appendChild(tagElement);
                this.value = '';
                updateTagsField();
            }
        }
    });
    
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('tag-remove')) {
            e.target.parentElement.remove();
            updateTagsField();
        }
    });
}

function updateTagsField() {
    const tags = Array.from(document.querySelectorAll('.tag'))
        .map(tag => tag.textContent.slice(0, -1).trim());
    document.querySelector('input[name="tags"]').value = tags.join(',');
}

// Initialize all features
initializeTagInput();