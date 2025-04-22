// Prediction page functionality
document.addEventListener("DOMContentLoaded", () => {
    // Navbar toggle functionality
    const navbarToggleBtn = document.getElementById("navbarToggle");
    const navbar = document.querySelector(".navbar");
    
    if (navbarToggleBtn && navbar) {
      // Initialize navbar visibility from localStorage or default to visible
      const isNavbarHidden = localStorage.getItem("navbarHidden") === "true";
      if (isNavbarHidden) {
        navbar.classList.add("hidden");
        updateToggleIcon(navbarToggleBtn, true);
      }
      
      navbarToggleBtn.addEventListener("click", () => {
        const isHidden = navbar.classList.toggle("hidden");
        localStorage.setItem("navbarHidden", isHidden);
        updateToggleIcon(navbarToggleBtn, isHidden);
      });
    }
    
    function updateToggleIcon(btn, isHidden) {
      if (isHidden) {
        btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M3 12H21M3 6H21M3 18H21"></path></svg>`;
      } else {
        btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M18 6L6 18M6 6L18 18"></path></svg>`;
      }
    }

    // Modal functionality
    const aboutLink = document.getElementById("aboutUsLink");
    const aboutModal = document.getElementById("aboutUsModal");
    const closeModal = document.querySelector(".close-modal");
    
    if (aboutLink && aboutModal) {
      aboutLink.addEventListener("click", () => {
        aboutModal.style.display = "block";
      });
      
      closeModal.addEventListener("click", () => {
        aboutModal.style.display = "none";
      });
      
      window.addEventListener("click", (event) => {
        if (event.target === aboutModal) {
          aboutModal.style.display = "none";
        }
      });
    }

    // Prediction form handling
    const form = document.getElementById("predictionForm");
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
  
        const magnitude = parseFloat(document.getElementById("magnitude").value);
        const location = document.getElementById("location").value.trim();
        const distance = parseFloat(document.getElementById("distance").value);
        const locality = document.getElementById("locality").value.trim();
  
        if (!magnitude || !location || !distance || !locality) {
          alert("Please fill in all fields.");
          return;
        }

        // Extract state from location (assuming format like "California")
        const state = location;
        
        // Determine locality type (assuming it's either "Urban" or "Rural")
        const locality_type = locality.toLowerCase();
        
        // Show loading indicator
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
          submitBtn.innerHTML = "Processing...";
          submitBtn.disabled = true;
        }
        
        // Send data to the API
        fetch('/api/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            magnitude: magnitude,
            state: state,
            locality_type: locality_type,
            distance_km: distance
          })
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          console.log("API Response:", data);
          
          // Store prediction results in localStorage
          const prediction = {
            magnitude,
            location,
            distance,
            locality,
            predictedSignificance: data.predicted_significance,
            severityScore: data.severity_score,
            instructions: data.instructions,
            impactLevel: getImpactLevel(data.severity_score),
            severityColor: getSeverityColor(data.severity_score),
            timestamp: new Date().toISOString(),
          };
          
          localStorage.setItem("earthquakePrediction", JSON.stringify(prediction));
          
          // (Optional) Store in history
          const history = JSON.parse(localStorage.getItem("predictionHistory")) || [];
          history.push(prediction);
          localStorage.setItem("predictionHistory", JSON.stringify(history));
          
          // Redirect to analytics page using the correct URL path
          window.location.href = "/analytics";
        })
        .catch(error => {
          console.error('Error:', error);
          alert('There was a problem with the prediction. Please try again.');
          // Reset button
          if (submitBtn) {
            submitBtn.innerHTML = "Predict";
            submitBtn.disabled = false;
          }
        });
      });
    }
    
    // Helper functions for determining impact level and color
    function getImpactLevel(severity) {
      if (severity >= 80) return "High";
      if (severity >= 40) return "Moderate";
      return "Low";
    }
    
    function getSeverityColor(severity) {
      if (severity >= 80) return "red";
      if (severity >= 40) return "orange";
      return "green";
    }
  
    // Analytics page functionality
    const predictionData = JSON.parse(localStorage.getItem("earthquakePrediction"));
  
    if (predictionData) {
      // Optional: Check if older than 24h
      const now = new Date();
      const predictionTime = new Date(predictionData.timestamp);
      const hoursPassed = (now - predictionTime) / 36e5;
      if (hoursPassed > 24) {
        localStorage.removeItem("earthquakePrediction");
        location.reload();
        return;
      }
  
      const bar = document.getElementById("impactBar");
      const container = document.getElementById("impactBarContainer");
      const details = document.getElementById("impactDetails");
      const noDataMsg = document.getElementById("noDataMessage");
  
      if (bar && container && details) {
        let width = "30%";
        if (predictionData.impactLevel === "Moderate") width = "60%";
        if (predictionData.impactLevel === "High") width = "90%";
  
        bar.style.width = width;
        bar.style.backgroundColor = predictionData.severityColor;
  
        details.innerHTML = `
          <strong>Magnitude:</strong> ${predictionData.magnitude}<br>
          <strong>Epicenter:</strong> ${predictionData.location}<br>
          <strong>Distance to Epicenter:</strong> ${predictionData.distance} km<br>
          <strong>Locality:</strong> ${predictionData.locality}<br>
          <strong>Predicted Impact:</strong> ${predictionData.impactLevel}<br>
          <strong>Significance:</strong> ${predictionData.predictedSignificance || 'N/A'}<br>
          <strong>Severity Score:</strong> ${predictionData.severityScore || 'N/A'}<br>
          <strong>Instructions:</strong><br>${predictionData.instructions || 'N/A'}
        `;
      }
  
    } else {
      const noDataMsg = document.getElementById("noDataMessage");
      if (noDataMsg) noDataMsg.style.display = "block";
    }
  });
  