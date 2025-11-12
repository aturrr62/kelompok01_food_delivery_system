// 🏠 HOME PAGE - PANGGIL 2 SERVICES: restaurants + users
document.addEventListener('DOMContentLoaded', function() {
    loadHomepageData();
});

async function loadHomepageData() {
    try {
        showMessage('Loading data...', 'info');
        
        // PANGGIL 2 SERVICES BERBEDA melalui API Gateway
        const [restaurantsResponse, userResponse] = await Promise.all([
            apiCall('restaurants/api/restaurants'),  // Service: restaurants (rizki)
            apiCall('users/api/users/1')             // Service: users (ARTHUR)
        ]);

        if (restaurantsResponse.success) {
            displayRestaurants(restaurantsResponse.data || []);
        } else {
            displayRestaurants(getSampleRestaurants()); // Fallback data
        }

        if (userResponse.success) {
            displayUserWelcome(userResponse.data);
        } else {
            displayUserWelcome({ name: 'Guest' }); // Fallback
        }
        
    } catch (error) {
        console.error('Error loading homepage:', error);
        showMessage('Error loading data', 'error');
        // Fallback to sample data
        displayRestaurants(getSampleRestaurants());
        displayUserWelcome({ name: 'Guest' });
    }
}

function displayRestaurants(restaurants) {
    const container = document.getElementById('restaurants-list');
    
    if (!restaurants || restaurants.length === 0) {
        container.innerHTML = `
            <div class="col-span-3 text-center py-8">
                <i class="fas fa-utensils text-4xl text-gray-400 mb-4"></i>
                <p class="text-gray-600">Tidak ada restoran tersedia</p>
            </div>
        `;
        return;
    }

    const html = restaurants.map(restaurant => `
        <div class="bg-white rounded-2xl shadow-sm p-6 hover:shadow-md transition cursor-pointer border border-gray-100" 
             onclick="goToRestaurant(${restaurant.id})">
            <div class="w-full h-48 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg mb-4 flex items-center justify-center">
                <i class="fas fa-utensils text-4xl text-blue-600"></i>
            </div>
            <h4 class="font-bold text-lg text-gray-800 mb-2">${restaurant.name}</h4>
            <p class="text-gray-600 mb-2">${restaurant.cuisine_type || 'Indonesian Food'}</p>
            <p class="text-sm text-gray-500 mb-3">
                <i class="fas fa-map-marker-alt mr-1 text-blue-500"></i>
                ${restaurant.address || 'Location not specified'}
            </p>
            <div class="flex justify-between items-center">
                <span class="text-green-600 font-semibold">Buka</span>
                <span class="text-blue-600 font-semibold">Lihat Menu →</span>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function displayUserWelcome(user) {
    const welcomeElement = document.getElementById('welcome-message');
    if (welcomeElement && user) {
        welcomeElement.innerHTML = `
            <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
                <h3 class="font-semibold text-blue-800">Halo, ${user.name}! 👋</h3>
                <p class="text-blue-600 text-sm">Selamat datang di FoodDelivery</p>
            </div>
        `;
    }
}

function goToRestaurant(restaurantId) {
    window.location.href = `restaurant.html?id=${restaurantId}`;
}

// Sample data for fallback
function getSampleRestaurants() {
    return [
        {
            id: 1,
            name: "Restoran Padang Sederhana",
            cuisine_type: "Padang",
            address: "Jl. Merdeka No. 123",
            is_open: true
        },
        {
            id: 2,
            name: "Warung Jawa Timur",
            cuisine_type: "Jawa",
            address: "Jl. Sudirman No. 45",
            is_open: true
        },
        {
            id: 3,
            name: "Seafood Laut Biru",
            cuisine_type: "Seafood",
            address: "Jl. Pantai Indah No. 67",
            is_open: true
        }
    ];
}