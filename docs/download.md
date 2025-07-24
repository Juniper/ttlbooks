# Download Street 

This is the place to download all our contents in PDF.

</br>
<div id="pdfCarousel" class="carousel">
    <button class="nav" id="prev">
        <i class="fas fa-chevron-left"></i>
    </button>
    
    <div id="carouselItems" class="carousel-items"></div>
    
    <button class="nav" id="next">
        <i class="fas fa-chevron-right"></i>
    </button>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/js/all.min.js"></script> <!-- FontAwesome -->
<script>
    // Fetch the PDF list from the JSON file
    async function fetchPDFList() {
        try {
            const response = await fetch('./download/pdf-list.json');
            const pdfList = await response.json();
            populateCarousel(pdfList);
        } catch (error) {
            console.error("Failed to load PDF list:", error);
        }
    }

    // Populate the carousel with PDF items (icon + name)
    function populateCarousel(pdfList) {
        const carouselItemsContainer = document.getElementById('carouselItems');
        carouselItemsContainer.innerHTML = '';  // Clear previous items
        
        pdfList.forEach((pdfPath, index) => {
            const pdfName = pdfPath.split('/').pop();  // Extract file name (e.g., "NAME.pdf")
            const iconName = pdfName.replace('.pdf', '.png');  // Replace .pdf with .png for the icon
            
            // Assuming the icon files are located in the same directory as PDFs, you can update the path here
            const pdfIcon = `./download/${iconName}`;  
            const pdfItem = document.createElement('div');
            pdfItem.classList.add('carousel-item');
            pdfItem.innerHTML = `
                <img src="${pdfIcon}" alt="PDF Icon" class="pdf-icon">
                <p>${pdfName}</p>
            `;
            pdfItem.addEventListener('click', () => openPDF(`./download/${pdfPath}`));
            carouselItemsContainer.appendChild(pdfItem);
        });
    }

    // Function to open the PDF in a new window/tab
    function openPDF(pdfPath) {
        window.open(pdfPath, '_blank');
    }

    // Add event listeners for navigation buttons
    let currentIndex = 0;

    document.getElementById('next').addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % document.querySelectorAll('.carousel-item').length;
        updateCarouselPosition();
    });

    document.getElementById('prev').addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + document.querySelectorAll('.carousel-item').length) % document.querySelectorAll('.carousel-item').length;
        updateCarouselPosition();
    });

    // Update the carousel's position based on the current index
    function updateCarouselPosition() {
        const items = document.querySelectorAll('.carousel-item');
        items.forEach((item, index) => {
            if (index === currentIndex) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    // Initialize the carousel when the page loads
    document.addEventListener('DOMContentLoaded', fetchPDFList);
</script>

<style>
    /* Carousel container */
    .carousel {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        overflow: hidden;
        position: relative;
        padding: 20px 0;
    }

    /* Carousel items container */
    .carousel-items {
        display: flex;
        transition: transform 0.5s ease-in-out;
        justify-content: center;
    }

    /* Each carousel item */
    .carousel-item {
        margin: 0 20px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.3s ease;
    }

    /* Larger icons */
    .carousel-item img {
        width: 336px;  
        height: auto;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Item name */
    .carousel-item p {
        margin-top: 10px;
        font-size: 16px;
        font-weight: bold;
    }

    /* Active item highlight */
    .carousel-item.active {
        transform: scale(1.1);
        transition: transform 0.3s ease;
    }

    /* Navigation buttons */
    .nav {
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 10px;
        border: none;
        cursor: pointer;
        border-radius: 15%;
    }

    .nav:hover {
        background-color: rgba(0, 0, 0, 0.7);
    }

    /* Style for the left and right arrows */
    .nav i {
        font-size: 20px;
    }

    /* Adjusts the position of the buttons */
    .nav#prev {
        position: absolute;
        left: 20px;
    }

    .nav#next {
        position: absolute;
        right: 20px;
    }
</style>
