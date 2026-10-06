document.addEventListener("DOMContentLoaded", () => {
    // 1. Text Area and Word Counter Setup
    const textArea = document.getElementById("news_text");
    const wordCounter = document.getElementById("word_count");
    const form = document.getElementById("analysis_form");
    const loader = document.getElementById("loader");
    
    if (textArea && wordCounter) {
        const updateWordCount = () => {
            const text = textArea.value.trim();
            const words = text ? text.split(/\s+/).length : 0;
            wordCounter.textContent = `${words} words`;
        };
        
        textArea.addEventListener("input", updateWordCount);
        updateWordCount(); // Initial call
    }
    
    // 2. Loading State Handling
    if (form && loader) {
        form.addEventListener("submit", (e) => {
            const text = textArea && textArea.value ? textArea.value.trim() : "";
            if (text.length > 0) {
                loader.classList.add("active");
            }
        });
    }
    
    // 3. Preset Fill Buttons
    const presetButtons = document.querySelectorAll(".preset-btn");
    if (presetButtons.length > 0 && textArea) {
        presetButtons.forEach(btn => {
            btn.addEventListener("click", () => {
                const type = btn.getAttribute("data-type");
                let presetText = "";
                
                if (type === "fake-space") {
                    presetText = "BREAKING NEWS!!! NASA Insiders just leaked top-secret video files showing the entire solar system was built inside an underground Hollywood warehouse. Scientists have been using CGI projectors for over 50 years to fake space missions and steal trillions of dollars from global tax systems. Shocking files reveal a secret project base in the desert where laser grids simulate stars and planet backdrops! Citizens must wake up and share this vital message immediately before the internet is shut down by deep state operatives!";
                } else if (type === "fake-health") {
                    presetText = "URGENT WARNING: Independent researchers have found that a common backyard dandelion weed completely cures cancer in 24 hours. The FDA has secretly banned all studies and sales of this weed to protect big pharmaceutical company profits. They are planning to introduce microchips to replace currency so they can control what medicine you can buy. Share this viral article now before it is deleted forever!";
                } else if (type === "true-politics") {
                    presetText = "The Senate voted to approve the bipartisan infrastructure bill today in a 68-32 vote, marking a rare moment of major cross-party agreement in Congress. The legislation allocates $1.2 trillion for infrastructure improvements, including major upgrades to roads, bridges, public transport, and clean water networks. The President praised the committee for its collaborative efforts. The local regional representative stated that over 80% of surveyed citizens support this measure, according to a recent census update.";
                } else if (type === "true-science") {
                    presetText = "NASA announced today that a robotic capsule carrying three astronauts from the International Space Station has successfully splashed down in the Pacific Ocean after a six-month scientific research mission. The crew conducted experiments on microgravity protein crystallization and tested an advanced water recycling mechanism that could support future Mars flights. NASA officials confirmed all team members are in excellent health and will undergo routine physiological adaptation protocols.";
                }
                
                textArea.value = presetText;
                // Dispatch input event to update word counter
                textArea.dispatchEvent(new Event("input"));
                
                // Smooth scroll to textarea
                textArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
        });
    }
    
    // 4. Gauge Animation on Result Page
    const meterFill = document.querySelector(".meter-fill");
    if (meterFill) {
        const confidenceVal = meterFill.getAttribute("data-confidence");
        // Trigger width transition with a small delay for a visual entrance effect
        setTimeout(() => {
            meterFill.style.width = `${confidenceVal * 100}%`;
        }, 150);
    }
});
