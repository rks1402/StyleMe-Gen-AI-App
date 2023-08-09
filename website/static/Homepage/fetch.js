// script.js

// Function to fetch products from the API and populate the product container
async function fetchAndDisplayProducts() {
    const productContainer = document.getElementById('product-container');

    try {
        const response = await fetch('/get_all_product');
        const data = await response.json();

        if (response.status === 200) {
            // Loop through the fetched products and generate HTML for each product
            const productsHTML = data.map(product => `
                <div class="product">
                    <img src="${product.image}" alt="${product.name}">
                    <h3>${product.name}</h3>
                    <p>${product.description}</p>
                    <span class="price">${product.price}</span>
                    <button>Add to Cart</button>
                </div>
            `).join('');

            // Insert the generated HTML into the product container
            productContainer.innerHTML = productsHTML;
        } else {
            productContainer.innerHTML = 'Error fetching products.';
        }
    } catch (error) {
        productContainer.innerHTML = 'An error occurred.';
        console.error('Error fetching products:', error);
    }
}

// Call the function to fetch and display products when the page loads
window.addEventListener('load', fetchAndDisplayProducts);
