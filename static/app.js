document.getElementById("promptForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission

    const prompt = document.getElementById("prompt").value;

    // Send prompt to the backend server
    let formData = new FormData();
    formData.append("prompt", prompt);

    try {
        let response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            // Update video source dynamically
            const videoElement = document.getElementById("generatedVideo");
            videoElement.src = "/out/video.mp4";  // This assumes the file is served at this path
            videoElement.load();  // Reload the video with the new source

            // Make the video section visible
            document.getElementById("videoSection").style.display = "block";
            document.getElementById("videoSection").style.opacity = 1;

            // Scroll down to the video section based on viewport height
            const videoSection = document.getElementById("videoSection");
            const offset = window.innerHeight * 0.1;
            const sectionPosition = videoSection.getBoundingClientRect().top + window.scrollY;

            window.scrollTo({
                top: sectionPosition - offset,
                behavior: "smooth"
            });


        } else {
            console.error('Error generating video');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
