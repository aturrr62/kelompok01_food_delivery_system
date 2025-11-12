// 🔧 UTILITIES & API GATEWAY INTEGRATION
const API_GATEWAY = 'http://localhost:5000';
const DEBUG_MODE = true;

// Universal API Call function
async function apiCall(endpoint, options = {}) {
    try {
        if (DEBUG_MODE) console.log(`🔄 Calling: ${API_GATEWAY}/${endpoint}`);
        
        const response = await fetch(`${API_GATEWAY}/${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        if (DEBUG_MODE) console.log(`✅ Response from ${endpoint}:`, data);
        return data;
        
    } catch (error) {
        console.error(`❌ API Call failed [${endpoint}]:`, error);
        return { 
            success: false, 
            error: 'Service unavailable. Please try again later.' 
        };
    }
}

// Utility Functions
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white font-semibold z-50 ${
        type === 'success' ? 'bg-green-500' : 
        type === 'error' ? 'bg-red-500' : 'bg-blue-500'
    }`;
    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        messageDiv.style.transition = 'opacity 0.5s';
        setTimeout(() => messageDiv.remove(), 500);
    }, 3000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

// Cart Management
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function clearCart() {
    localStorage.removeItem('cart');
    updateCartCount();
}

function addToCart(item) {
    const cart = getCart();
    const existingItem = cart.find(cartItem => cartItem.id === item.id);
    
    if (existingItem) {
        existingItem.quantity = (existingItem.quantity || 1) + 1;
    } else {
        cart.push({ ...item, quantity: 1 });
    }
    
    saveCart(cart);
    showMessage('Item added to cart!', 'success');
}

function updateCartCount() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
    const cartCount = document.getElementById('cart-count');
    
    if (cartCount) {
        if (totalItems > 0) {
            cartCount.textContent = totalItems;
            cartCount.classList.remove('hidden');
        } else {
            cartCount.classList.add('hidden');
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
});