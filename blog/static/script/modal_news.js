document.addEventListener('DOMContentLoaded', function () {
    var close_news = document.getElementById("close-news");
    var close_bp = document.getElementById("close-bp");
    var modal_news = document.getElementById("modal-news");
    var modal_bp = document.getElementById("modal-bp");
    var submit_email = document.getElementById("submit_email");
    var email_newsletter = document.getElementById("email_newsletter");
    var error_newsletter = document.getElementById("error_newsletter");
    var plu = document.getElementById("plu");
    var expired = document.getElementById("expired");
    var reasons = document.getElementById("reasons");

    if (close_news){
        close_news.addEventListener("click", function() {
            modal_news.remove();
            document.cookie = 'news_modal=true;path=/';
        })
    }

    if (close_bp){
        close_bp.addEventListener("click", function() {
            modal_bp.classList.toggle("hidden");
        })
    }

    if (submit_email){
        submit_email.addEventListener("click", function() {
            event.preventDefault()
            // Envoyer une requête pour accepter les cookies
            // Créer un objet FormData pour construire le corps de la requête
            var formData = new FormData();
            formData.append("email", email_newsletter.value);
            console.log("email_newsletter.value",email_newsletter.value)

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/newsletter', true);
            xhr.onload = function () {
                var response = JSON.parse(xhr.responseText);
                if (xhr.status === 200) {
                    modal_news.remove();
                    var expirationDate = new Date();
                    expirationDate.setDate(expirationDate.getDate() + 30);
                    var expires = expirationDate.toUTCString();
                    document.cookie = 'news_modal=true; expires=' + expires + '; path=/';
                }
                else{
                    // Accéder à la propriété 'status' de l'objet JSON
                    error_newsletter.innerText = response.status;
                    console.log('Request failed.  Returned status of ' + xhr.status + response);
                }
            };
            xhr.send(formData);
        })
    }

    if (plu){
        plu.addEventListener("click", function() {
            modal_bp.classList.toggle("hidden");
        })
    }

    if (expired){
        expired.addEventListener("click", function() {
            modal_bp.classList.toggle("hidden");
        })
    }

    if (reasons){
        reasons.addEventListener("click", function() {
            modal_bp.classList.toggle("hidden");
        })
    }

    if (modal_news.classList.contains('hidden')){
        window.addEventListener('scroll', function(event) {
            var scrollPercent = window.scrollY/(document.documentElement.scrollHeight - window.innerHeight);
            // Round the percentage to the nearest integer
            var scrollPercentRounded = Math.round(scrollPercent * 100);
            // If 75% of the page is scrolled down, show the modal 
            if (scrollPercentRounded > 50) {
                modal_news.classList.remove('hidden');
            }
        });
    }
});