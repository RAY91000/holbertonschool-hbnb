function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
	return null;
}

document.addEventListener('DOMContentLoaded', () => {
	const loginForm = document.getElementById('login-form');
	const errorMsg = document.getElementById('error-message');

	if (loginForm) {
		loginForm.addEventListener('submit', async (event) => {
			event.preventDefault();

			const email = document.getElementById('email').value;
			const password = document.getElementById('password').value;

			try {
				const response = await fetch('http://localhost:5000/api/v1/auth/login', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ email, password })
				});

				if (response.ok) {
					const data = await response.json();
					document.cookie = `token=${data.access_token}; path=/`;
					window.location.href = 'index.html';
				} else {
					const errText = await response.text();
					errorMsg.style.display = 'block';
					errorMsg.textContent = `Login failed: ${errText}`;
				}
			} catch (error) {
				errorMsg.style.display = 'block';
				errorMsg.textContent = 'An error occurred during login.';
			}
		});
	}

	const loginLink = document.getElementById('login-link');
	const placesList = document.getElementById('places-list');
	const priceFilter = document.getElementById('price-filter');
	const token = getCookie('token');

	if (loginLink) {
		loginLink.style.display = token ? 'none' : 'inline';
	}

	if (placesList) {
		fetchPlaces(token).then(places => {
			displayPlaces(places);

			if (priceFilter) {
				priceFilter.addEventListener('change', () => {
					const value = priceFilter.value;
					const filtered = places.filter(place => {
						if (value === 'all') return true;
						return place.pricePerNight <= parseFloat(value);
					});
					displayPlaces(filtered);
				});
			}
		});
	}

	const placeDetails = document.getElementById('place-details');
	const reviewsList = document.getElementById('reviews-list');
	const addReviewSection = document.getElementById('add-review');

	if (placeDetails) {
		const placeId = getPlaceIdFromURL();

		fetchPlaceDetails(placeId, token).then(data => {
			if (data) {
				displayPlaceDetails(data);
				displayReviews(data.reviews || []);
			}
		});

		if (addReviewSection) {
			addReviewSection.style.display = token ? 'block' : 'none';
		}
	}

	const reviewForm = document.getElementById('review-form');

	if (reviewForm) {
		if (!token) {
			window.location.href = 'index.html';
			return;
		}

		const placeId = getPlaceIdFromURL();
		const messageBox = document.getElementById('review-message');

		reviewForm.addEventListener('submit', async (event) => {
			event.preventDefault();

			const rating = parseFloat(document.getElementById('rating').value);
			const comment = document.getElementById('comment').value;

			try {
				const response = await fetch('http://localhost:5000/api/v1/reviews', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': `Bearer ${token}`
					},
					body: JSON.stringify({
						place_id: placeId,
						rating,
						comment
					})
				});

				if (response.ok) {
					messageBox.style.color = 'green';
					messageBox.textContent = 'Review submitted successfully!';
					messageBox.style.display = 'block';
					reviewForm.reset();
				} else {
					const errText = await response.text();
					messageBox.style.color = 'red';
					messageBox.textContent = `Error: ${errText}`;
					messageBox.style.display = 'block';
				}
			} catch (error) {
				messageBox.style.color = 'red';
				messageBox.textContent = 'An unexpected error occurred.';
				messageBox.style.display = 'block';
			}
		});
	}
});

async function fetchPlaces(token) {
	try {
		const response = await fetch('http://localhost:5000/api/v1/places/', {
			headers: {
				'Authorization': token ? `Bearer ${token}` : ''
			}
		});
		if (response.ok) {
			return await response.json();
		} else {
			return [];
		}
	} catch {
		return [];
	}
}

function displayPlaces(places) {
	const list = document.getElementById('places-list');
	list.innerHTML = '';
	places.forEach(place => {
		const card = document.createElement('div');
		card.className = 'place-card';
		card.innerHTML = `
			<h3>${place.name}</h3>
			<p>Price per night: $${place.pricePerNight}</p>
			<button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
		`;
		list.appendChild(card);
	});
}

function getPlaceIdFromURL() {
	const params = new URLSearchParams(window.location.search);
	return params.get('id');
}

async function fetchPlaceDetails(placeId, token) {
	try {
		const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
			headers: {
				'Authorization': token ? `Bearer ${token}` : ''
			}
		});
		if (response.ok) {
			return await response.json();
		}
	} catch {}
	return null;
}

function displayPlaceDetails(place) {
	const container = document.getElementById('place-details');
	container.innerHTML = `
		<h2>${place.name}</h2>
		<p><strong>Host:</strong> ${place.ownerName || 'Unknown'}</p>
		<p><strong>Price per night:</strong> $${place.pricePerNight}</p>
		<p><strong>Description:</strong> ${place.description}</p>
		<p><strong>Amenities:</strong> ${place.amenities?.join(', ') || 'None'}</p>
	`;
}

function displayReviews(reviews) {
	const container = document.getElementById('reviews-list');
	container.innerHTML = '';
	reviews.forEach(review => {
		const card = document.createElement('div');
		card.className = 'review-card';
		card.innerHTML = `
			<p><strong>${review.userName || 'Anonymous'}:</strong> ${review.comment}</p>
			<p>Rating: ${review.rating}</p>
		`;
		container.appendChild(card);
	});
}
