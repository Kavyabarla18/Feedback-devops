// API Configuration - Change this if your backend is on a different host/port
const API_BASE_URL = 'http://localhost:5000/api';





// Global state
let selectedRating = 0;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeStarRating();
    initializeCharCounter();
    initializeFeedbackForm();
    loadFeedback();
    loadAnalytics();
});

// Page Navigation
function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    // Show selected page
    document.getElementById(`${pageName}-page`).classList.add('active');

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    event.target.closest('.nav-link').classList.add('active');

    // Reload data for specific pages
    if (pageName === 'home') loadFeedback();
    if (pageName === 'analytics') loadAnalytics();
}

// Star Rating System
function initializeStarRating() {
    const stars = document.querySelectorAll('.star-rating i');
    const ratingText = document.querySelector('.rating-text');

    stars.forEach(star => {
        star.addEventListener('click', function() {
            selectedRating = parseInt(this.dataset.rating);
            document.getElementById('rating').value = selectedRating;
            updateStars(selectedRating);
            ratingText.textContent = `${selectedRating} star${selectedRating > 1 ? 's' : ''}`;
        });

        star.addEventListener('mouseenter', function() {
            const rating = parseInt(this.dataset.rating);
            updateStars(rating, true);
        });
    });

    document.querySelector('.star-rating').addEventListener('mouseleave', function() {
        updateStars(selectedRating);
    });
}

function updateStars(rating, isHover = false) {
    const stars = document.querySelectorAll('.star-rating i');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('far');
            star.classList.add('fas', isHover && !selectedRating ? 'hover' : 'active');
        } else {
            star.classList.remove('fas', 'active', 'hover');
            star.classList.add('far');
        }
    });
}

// Character Counter
function initializeCharCounter() {
    const feedbackTextarea = document.getElementById('feedback');
    const charCount = document.getElementById('char-count');

    feedbackTextarea.addEventListener('input', function() {
        charCount.textContent = this.value.length;
        if (this.value.length > 900) {
            charCount.style.color = 'var(--danger-color)';
        } else {
            charCount.style.color = 'var(--text-light)';
        }
    });
}

// Form Submission
function initializeFeedbackForm() {
    const form = document.getElementById('feedback-form');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = {
            name: document.getElementById('name').value || 'Anonymous',
            email: document.getElementById('email').value,
            feedback: document.getElementById('feedback').value,
            rating: selectedRating,
            category: document.getElementById('category').value
        };

        // Validation
        if (!formData.feedback.trim()) {
            showToast('Please enter your feedback', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                showToast('Feedback submitted successfully!', 'success');
                form.reset();
                selectedRating = 0;
                updateStars(0);
                document.querySelector('.rating-text').textContent = 'Select rating';
                document.getElementById('char-count').textContent = '0';

                // Switch to home page after 1.5 seconds
                setTimeout(() => {
                    showPage('home');
                    document.querySelector('[href="#home"]').click();
                }, 1500);
            } else {
                showToast(result.error || 'Error submitting feedback', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Failed to connect to server. Please check if backend is running.', 'error');
        }
    });
}

// Load Feedback
async function loadFeedback() {
    const feedbackList = document.getElementById('feedback-list');
    feedbackList.innerHTML = '<div class="loading">Loading feedback...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/feedback`);
        const data = await response.json();

        const feedbackArray = data.feedback || data;

        if (feedbackArray.length === 0) {
            feedbackList.innerHTML = '<div class="loading">No feedback yet. Be the first to share your thoughts!</div>';
            return;
        }

        feedbackList.innerHTML = '';

        // Reverse to show most recent first
        feedbackArray.reverse().forEach(item => {
            const card = createFeedbackCard(item);
            feedbackList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading feedback:', error);
        feedbackList.innerHTML = '<div class="loading">Error loading feedback. Please check if backend is running on http://localhost:5000</div>';
    }
}

// Create Feedback Card
function createFeedbackCard(feedback) {
    const card = document.createElement('div');
    card.className = 'feedback-card';

    const sentiment = getSentiment(feedback.rating || 3);
    const stars = generateStars(feedback.rating || 0);
    const timeAgo = getTimeAgo(feedback.timestamp);

    card.innerHTML = `
        <div class="feedback-header">
            <div class="user-info">
                <i class="fas fa-user-circle"></i>
                <div class="user-details">
                    <h4>${feedback.name || 'Anonymous'}</h4>
                    ${feedback.email ? `<p>${feedback.email}</p>` : ''}
                </div>
            </div>
            <span class="sentiment-badge ${sentiment.class}">${sentiment.text}</span>
        </div>

        ${feedback.rating ? `<div class="rating">${stars}</div>` : ''}

        ${feedback.category ? `
            <div class="category-tag">
                <i class="fas fa-tag"></i>
                ${feedback.category}
            </div>
        ` : ''}

        <div class="feedback-content">
            ${feedback.feedback}
        </div>

        <div class="feedback-time">
            <i class="far fa-clock"></i>
            ${timeAgo}
        </div>
    `;

    return card;
}

// Generate Star HTML
function generateStars(rating) {
    let stars = '';
    for (let i = 0; i < 5; i++) {
        stars += i < rating ? '<i class="fas fa-star"></i>' : '<i class="far fa-star"></i>';
    }
    return stars;
}

// Get Sentiment
function getSentiment(rating) {
    if (rating >= 4) return { text: 'positive', class: 'positive' };
    if (rating >= 3) return { text: 'neutral', class: 'neutral' };
    return { text: 'negative', class: 'negative' };
}

// Time Ago Function
function getTimeAgo(timestamp) {
    if (!timestamp) return 'Recently';

    const now = new Date();
    const past = new Date(timestamp);
    const diffMs = now - past;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return past.toLocaleDateString();
}

// Load Analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE_URL}/feedback`);
        const data = await response.json();

        const feedbackArray = data.feedback || data;
        const total = feedbackArray.length;

        let positive = 0, neutral = 0, negative = 0;

        feedbackArray.forEach(item => {
            const rating = item.rating || 3;
            if (rating >= 4) positive++;
            else if (rating >= 3) neutral++;
            else negative++;
        });

        document.getElementById('total-feedback').textContent = total;
        document.getElementById('positive-feedback').textContent = positive;
        document.getElementById('neutral-feedback').textContent = neutral;
        document.getElementById('negative-feedback').textContent = negative;
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Toast Notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
