document.getElementById("promptForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission

    const prompt = document.getElementById("prompt").value;

    if (!prompt) {
        console.error('Prompt is empty!');
        return;
    }

    alert("Please wait a few minutes.. check your terminal");

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

            // Autoplay the video
            videoElement.play().catch(error => {
                console.error('Error trying to play the video:', error);
            });

            // Scroll to the bottom of the video section when the video is loaded
            videoElement.addEventListener('loadeddata', function() {
                const videoSectionBottom = videoSection.offsetTop + videoSection.offsetHeight; 

                window.scrollTo({
                    top: videoSectionBottom,
                    behavior: "smooth" 
                });
            });

        } else {
            console.error('Error generating video');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
