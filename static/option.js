// 'DOMContentLoaded' is an event that fires when the HTML document has been completely loaded.
// It's best practice to wrap your JS in this to make sure all HTML elements exist before you try to manipulate them.
document.addEventListener('DOMContentLoaded', () => {

    const normalView = document.getElementById('Normal');
    const advancedView = document.getElementById('Advanced');

    // Add a 'click' event listener to the "Normal" div
    if (normalView) {
        normalView.addEventListener('click', () => {
            // This function runs ONLY when 'normalView' is clicked
            const url = normalView.getAttribute('data-url');
            window.location.href = url; // Redirect
        });
    }

    // Add a 'click' event listener to the "Advanced" div
    if (advancedView) {
        advancedView.addEventListener('click', () => {
            // This function runs ONLY when 'advancedView' is clicked
            const url = advancedView.getAttribute('data-url');
            window.location.href = url; // Redirect
        });
    }
});