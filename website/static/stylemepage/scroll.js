// scripts.js
const productContainer = document.getElementById('product-container');
const nextButton = document.getElementById('next-button');

let currentProductIndex = 0;

function displayProduct(index) {
    if (index >= 0 && index < products.length) {
        const product = products[index];
        const productHTML = `
            <div class="product">
                <img class="product-image" src="${product.image_URL}" alt="${product.product_name}">
                <h2>${product.product_name}</h2>
                <p>${product.description}</p>
                <p>${product.price}</p>
            </div>
        `;
        productContainer.innerHTML = productHTML;
    }
}

nextButton.addEventListener('click', () => {
    currentProductIndex = (currentProductIndex + 1) % products.length;
    displayProduct(currentProductIndex);
});

displayProduct(currentProductIndex);
