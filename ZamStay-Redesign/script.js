// Property data
const properties = [
    {
        id: 1,
        title: "Modern City Apartment",
        description: "Luxury 2-bedroom apartment in city center",
        type: "apartment",
        price: "$120/night",
        image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        amenities: ["Kitchen", "Laundry", "Parking", "WiFi", "Air Conditioning"],
        location: "Lusaka CBD",
        attractions: ["Manda Hill Mall - 2km", "Levy Junction - 3km", "Zambia National Museum - 1.5km"]
    },
    {
        id: 2,
        title: "Grand Hotel Lusaka",
        description: "5-star luxury hotel with premium amenities",
        type: "hotel",
        price: "$220/night",
        image: "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        amenities: ["Spa", "Pool", "Restaurant", "Conference Room", "24/7 Room Service"],
        location: "Longacres, Lusaka",
        attractions: ["Arcades Shopping Mall - 0.5km", "Levy Golf Course - 2km", "Zambia National Assembly - 3km"]
    },
    {
        id: 3,
        title: "Wilderness Safari Lodge",
        description: "Authentic lodge in the heart of nature",
        type: "lodge",
        price: "$180/night",
        image: "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        amenities: ["Fireplace", "Guided Tours", "Wildlife Viewing", "Restaurant", "Bar"],
        location: "South Luangwa National Park",
        attractions: ["Luangwa River - 0.2km", "Game Drive Starting Point - 1km", "Local Village - 5km"]
    },
    {
        id: 4,
        title: "Cozy Studio Apartment",
        description: "Compact studio perfect for solo travelers",
        type: "apartment",
        price: "$85/night",
        image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        amenities: ["Kitchenette", "WiFi", "Parking", "TV", "Workspace"],
        location: "Woodlands, Lusaka",
        attractions: ["East Park Mall - 1.5km", "University of Zambia - 3km", "Kalimba Reptile Park - 10km"]
    },
    {
        id: 5,
        title: "Business Hotel Suite",
        description: "Executive suite for business travelers",
        type: "hotel",
        price: "$190/night",
        image: "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        amenities: ["Business Center", "Gym", "Airport Shuttle", "Breakfast Included", "Meeting Rooms"],
        location: "Kabulonga, Lusaka",
        attractions: ["Dutch Reformed Church - 0.5km", "Kalimba Farms - 4km", "Lusaka Golf Club - 2km"]
    },
    {
        id: 6,
        title: "Riverside Eco-Lodge",
        description: "Sustainable lodge with river views",
        type: "lodge",
        price: "$150/night",
        image: "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        amenities: ["Solar Power", "Organic Garden", "Canoeing", "Bird Watching", "Campfire Area"],
        location: "Kafue River",
        attractions: ["Kafue National Park - 15km", "Fishing Spots - 0.1km", "Local Craft Market - 3km"]
    }
];

// Category-specific amenities
const categoryAmenities = {
    apartment: ["Kitchen", "Laundry", "Parking", "WiFi", "Living Area"],
    hotel: ["Pool", "Spa", "Restaurant", "24/7 Concierge", "Room Service"],
    lodge: ["Nature Views", "Guided Tours", "Campfire", "Wildlife", "Restaurant"]
};

// DOM elements
const propertyList = document.getElementById('propertyList');
const categoryButtons = document.querySelectorAll('.category-btn');

// Initialize with all properties
renderProperties(properties);

// Add event listeners to category buttons
categoryButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Update active button
        categoryButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        // Filter properties
        const category = button.getAttribute('data-category');
        let filteredProperties;
        
        if (category === 'all') {
            filteredProperties = properties;
        } else {
            filteredProperties = properties.filter(property => property.type === category);
        }
        
        // Render filtered properties
        renderProperties(filteredProperties);
    });
});

// Function to render properties
function renderProperties(propertiesToRender) {
    propertyList.innerHTML = '';
    
    propertiesToRender.forEach(property => {
        const propertyCard = document.createElement('div');
        propertyCard.className = 'property-card fade-in';
        
        // Get amenities for this property type
        const amenities = categoryAmenities[property.type] || property.amenities;
        
        propertyCard.innerHTML = `
            <div class="property-image-container">
                <img src="${property.image}" alt="${property.title}" class="property-image">
                <div class="price-overlay">${property.price}</div>
                <div class="property-title">
                    <h2>${property.title}</h2>
                    <p>${property.description}</p>
                </div>
            </div>
            
            <div class="property-details">
                <div class="amenities-section">
                    <div class="section-title">
                        <i class="fas fa-home"></i>
                        <span>Amenities</span>
                    </div>
                    <div class="amenities-list">
                        ${amenities.map(amenity => `
                            <div class="amenity-item">
                                <i class="fas fa-check-circle"></i>
                                <span>${amenity}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="map-section">
                    <div class="section-title">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>Location</span>
                    </div>
                    <div class="mini-map">
                        <div class="map-placeholder">
                            <i class="fas fa-map"></i>
                            <span>Map of ${property.location}</span>
                        </div>
                    </div>
                    <div class="map-address">
                        <i class="fas fa-location-dot"></i> ${property.location}
                    </div>
                </div>
                
                <div class="attractions-section">
                    <div class="section-title">
                        <i class="fas fa-umbrella-beach"></i>
                        <span>Nearby Attractions</span>
                    </div>
                    <div class="attractions-list">
                        ${property.attractions.map(attraction => `
                            <div class="attraction-item">${attraction}</div>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <div class="cta-section">
                <button class="book-btn" onclick="bookProperty(${property.id})">
                    <i class="fas fa-calendar-check"></i>
                    Book Now
                </button>
            </div>
        `;
        
        propertyList.appendChild(propertyCard);
    });
}

// Function to handle booking
function bookProperty(propertyId) {
    const property = properties.find(p => p.id === propertyId);
    alert(`Booking ${property.title} for ${property.price}! In a real app, this would redirect to a booking page.`);
}

// Simulate loading animation
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.property-card').forEach(card => {
        card.classList.add('fade-in');
    });
});
