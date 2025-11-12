// 🔧 UTILITIES & API GATEWAY INTEGRATION - ENHANCED VERSION
const API_GATEWAY = 'http://localhost:5000';
const DEBUG_MODE = true;

// Enhanced API Call function with better error handling
async function apiCall(endpoint, options = {}) {
    const startTime = Date.now();
    
    try {
        if (DEBUG_MODE) {
            console.log(`🔄 API Call: ${API_GATEWAY}/${endpoint}`, options);
        }
        
        const response = await fetch(`${API_GATEWAY}/${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const responseTime = Date.now() - startTime;
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`❌ HTTP Error ${response.status}:`, errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        
        const data = await response.json();
        
        if (DEBUG_MODE) {
            console.log(`✅ API Response [${endpoint}]:`, data);
            console.log(`⏱️ Response time: ${responseTime}ms`);
        }
        
        return data;
        
    } catch (error) {
        console.error(`❌ API Call failed [${endpoint}]:`, error);
        return { 
            success: false, 
            error: error.message || 'Service unavailable. Please try again later.' 
        };
    }
}

// ========== CART MANAGEMENT FUNCTIONS ==========
function getCart() {
    const cart = localStorage.getItem('foodDeliveryCart');
    return cart ? JSON.parse(cart) : [];
}

function saveCart(cart) {
    localStorage.setItem('foodDeliveryCart', JSON.stringify(cart));
    updateCartCount();
}

function addToCart(item) {
    const cart = getCart();
    const existingItem = cart.find(cartItem => cartItem.id === item.id);
    
    if (existingItem) {
        existingItem.quantity += item.quantity || 1;
    } else {
        cart.push({
            ...item,
            quantity: item.quantity || 1
        });
    }
    
    saveCart(cart);
    showMessage(`✅ ${item.name} berhasil ditambahkan ke keranjang!`, 'success');
}

function updateCartQuantity(itemId, newQuantity) {
    const cart = getCart();
    const itemIndex = cart.findIndex(item => item.id === itemId);
    
    if (itemIndex !== -1) {
        if (newQuantity <= 0) {
            cart.splice(itemIndex, 1);
            showMessage('Item dihapus dari keranjang', 'info');
        } else {
            cart[itemIndex].quantity = newQuantity;
        }
        saveCart(cart);
        
        // Update UI if on cart page
        if (window.location.pathname.includes('cart.html')) {
            displayCartItems();
            updateCartSummary();
        }
    }
}

function removeFromCart(itemId) {
    const cart = getCart();
    const filteredCart = cart.filter(item => item.id !== itemId);
    saveCart(filteredCart);
    
    // Update UI if on cart page
    if (window.location.pathname.includes('cart.html')) {
        displayCartItems();
        updateCartSummary();
    }
    
    showMessage('Item dihapus dari keranjang', 'info');
}

function clearCart() {
    localStorage.removeItem('foodDeliveryCart');
    updateCartCount();
}

function getCartTotal() {
    const cart = getCart();
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
}

function updateCartCount() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElements = document.querySelectorAll('#cart-count');
    
    cartCountElements.forEach(element => {
        if (totalItems > 0) {
            element.textContent = totalItems;
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    });
}

// ========== UI UTILITY FUNCTIONS ==========
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

function showMessage(message, type = 'info') {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message-popup');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-popup fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm`;
    
    switch (type) {
        case 'success':
            messageDiv.className += ' bg-green-500 text-white';
            break;
        case 'error':
            messageDiv.className += ' bg-red-500 text-white';
            break;
        case 'warning':
            messageDiv.className += ' bg-yellow-500 text-white';
            break;
        default:
            messageDiv.className += ' bg-blue-500 text-white';
    }
    
    messageDiv.innerHTML = `
        <div class="flex items-center justify-between">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(messageDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentElement) {
            messageDiv.remove();
        }
    }, 5000);
}

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    
    // Add click handlers for navigation
    const cartLinks = document.querySelectorAll('a[href*="cart.html"]');
    cartLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = 'cart.html';
        });
    });
});

// ========== DEMO DATA FUNCTIONS ==========
function getSampleRestaurants() {
    return [
        {
            id: 1,
            name: "Warung Bakso Malang",
            description: "Bakso Malang autentik dengan kuah yang gurih",
            image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop",
            rating: 4.5,
            deliveryTime: "30-45 menit",
            deliveryFee: 15000,
            category: "Indonesian",
            isOpen: true
        },
        {
            id: 2,
            name: "Pizza Express",
            description: "Pizza Italia dengan topping segar",
            image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop",
            rating: 4.3,
            deliveryTime: "25-40 menit",
            deliveryFee: 12000,
            category: "Italian",
            isOpen: true
        },
        {
            id: 3,
            name: "Sushi Zen",
            description: "Sushi segar langsung dari dapur Jepang",
            image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop",
            rating: 4.7,
            deliveryTime: "35-50 menit",
            deliveryFee: 20000,
            category: "Japanese",
            isOpen: true
        }
    ];
}

function getSampleMenuItems(restaurantId) {
    const menus = {
        1: [
            { id: 101, name: "Bakso Solo", price: 25000, description: "Bakso daging sapi dengan kuah kaldu", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" },
            { id: 102, name: "Bakso Goreng", price: 20000, description: "Bakso digoreng crispy", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" },
            { id: 103, name: "Mie Ayam", price: 18000, description: "Mie ayam dengan pangsit", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" }
        ],
        2: [
            { id: 201, name: "Pizza Margherita", price: 85000, description: "Pizza dengan keju mozzarella dan basil", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" },
            { id: 202, name: "Pizza Pepperoni", price: 95000, description: "Pizza dengan pepperoni dan keju", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" },
            { id: 203, name: "Pizza Quattro Formaggi", price: 115000, description: "Pizza dengan 4 jenis keju", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" }
        ],
        3: [
            { id: 301, name: "Salmon Sushi", price: 75000, description: "Sushi salmon segar", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" },
            { id: 302, name: "California Roll", price: 55000, description: "Roll dengan crab dan avocado", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" },
            { id: 303, name: "Tempura Udon", price: 65000, description: "Udon kuah dengan tempura", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop" }
        ]
    };
    
    return menus[restaurantId] || [];
}

// Export functions for global use
window.getCart = getCart;
window.addToCart = addToCart;
window.updateCartQuantity = updateCartQuantity;
window.removeFromCart = removeFromCart;
window.clearCart = clearCart;
window.getCartTotal = getCartTotal;
window.formatCurrency = formatCurrency;
window.showMessage = showMessage;
window.updateCartCount = updateCartCount;
window.getSampleRestaurants = getSampleRestaurants;
window.getSampleMenuItems = getSampleMenuItems;