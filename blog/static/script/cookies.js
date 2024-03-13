$(document).ready(function () {
    // Gérer l'acceptation des cookies
    $('#accept-cookies').on('click', function () {
        // Masquer la bannière
        $('#cookie-banner').hide();

        // Envoyer une requête pour accepter les cookies
        $.get('/cookies/accept/', function (data) {
            console.log(data);
        });

        // Définir le cookie_accepted sur True
        document.cookie = 'cookie_accepted=true;path=/';
        document.cookie = 'cookie_banner=true;path=/';
    });

    // Gérer le refus des cookies
    $('#block-cookies').on('click', function () {
        // Masquer la bannière
        $('#cookie-banner').hide();
        document.cookie = 'cookie_banner=true;path=/';
    });
});