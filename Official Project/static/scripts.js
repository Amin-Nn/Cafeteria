
let currentRatingItemId = null;
let currentRatingValue = 0;


function showRatingModal(button) {
    const itemId = button.getAttribute('data-item-id');
    const itemName = button.getAttribute('data-item-name');
    
    currentRatingItemId = itemId;
    currentRatingValue = 0;
    document.getElementById('itemName').textContent = itemName;
    document.getElementById('comment').value = '';
    document.getElementById('ratingText').textContent = 'Select a rating';
    
    
    document.querySelectorAll('.star').forEach(star => {
        star.classList.remove('active');
    });
    
    document.getElementById('ratingModal').style.display = 'block';
}


function closeRatingModal() {
    document.getElementById('ratingModal').style.display = 'none';
}


function setRating(value) {
    currentRatingValue = value;
    
    
    document.querySelectorAll('.star').forEach((star, index) => {
        if (index < value) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
    
    
    const texts = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
    document.getElementById('ratingText').textContent = texts[value];
}


function submitRating() {
    if (currentRatingValue === 0) {
        alert('Please select a rating');
        return;
    }
    
    const comment = document.getElementById('comment').value;
    
    fetch('/api/ratings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: currentRatingItemId,
            rating: currentRatingValue,
            comment: comment
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Thank you for your rating!');
            closeRatingModal();
            loadRatings(currentRatingItemId);
        } else {
            alert('Error submitting rating');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting rating');
    });
}


function loadRatings(itemId) {
    fetch(`/api/ratings?item_id=${itemId}`)
    .then(response => response.json())
    .then(data => {
        const ratingDisplay = document.getElementById(`rating-${itemId}`);
        if (ratingDisplay) {
            const avgRating = data.avg_rating || 0;
            const count = data.count || 0;
            
            
            let starDisplay = '';
            for (let i = 0; i < 5; i++) {
                if (i < Math.round(avgRating)) {
                    starDisplay += '★';
                } else {
                    starDisplay += '☆';
                }
            }
            
            ratingDisplay.innerHTML = `
                <span class="stars">${starDisplay}</span>
                <span class="rating-count">(${count} rating${count !== 1 ? 's' : ''})</span>
            `;
        }
    })
    .catch(error => console.error('Error loading ratings:', error));
}


function showFeedbackModal() {
    document.getElementById('feedbackName').value = '';
    document.getElementById('feedbackEmail').value = '';
    document.getElementById('feedbackMessage').value = '';
    document.getElementById('feedbackModal').style.display = 'block';
}


function closeFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'none';
}


function submitFeedback() {
    const name = document.getElementById('feedbackName').value || 'Anonymous';
    const email = document.getElementById('feedbackEmail').value;
    const message = document.getElementById('feedbackMessage').value;
    
    if (!message.trim()) {
        alert('Please enter a message');
        return;
    }
    
    fetch('/api/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            email: email,
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Thank you for your feedback!');
            closeFeedbackModal();
        } else {
            alert('Error submitting feedback');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting feedback');
    });
}


window.onclick = function(event) {
    const ratingModal = document.getElementById('ratingModal');
    const feedbackModal = document.getElementById('feedbackModal');
    
    if (event.target === ratingModal) {
        ratingModal.style.display = 'none';
    }
    if (event.target === feedbackModal) {
        feedbackModal.style.display = 'none';
    }
};


document.addEventListener('DOMContentLoaded', function() {
    const ratingElements = document.querySelectorAll('[id^="rating-"]');
    ratingElements.forEach(element => {
        const itemId = element.id.replace('rating-', '');
        loadRatings(itemId);
    });
});