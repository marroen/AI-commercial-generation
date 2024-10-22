document.getElementById("promptForm").addEventListener("submit", function(event) {

    event.preventDefault(); // Prevent the form from submitting normally

    // Scroll down to the video section smoothly
    document.getElementById("videoSection").style.display = "block"; // Make the video section visible
    document.getElementById("videoSection").scrollIntoView({ behavior: "smooth" });

    // Fade in the video
    setTimeout(function() {
        document.getElementById("videoSection").style.opacity = 1;
    }, 500); // Delay to allow scroll animation to complete
});