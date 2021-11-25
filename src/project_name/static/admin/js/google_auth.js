function initSignin() {
    const client_id = document.querySelector('meta[name="google-signin-client_id"]').content;
    auth2 = gapi.auth2.init({
        client_id: client_id,
        scope: 'profile email'
    });

    const signupButton = document.querySelector('.google_login');
    auth2.attachClickHandler(signupButton, {}, onSignedUp);
}

function onSignedUp(googleUser) {
    const id_token = googleUser.getAuthResponse().id_token;
    loginWithGoogle(id_token);
}

async function loginWithGoogle(id_token) {
    if (id_token === null) {
        console.error('Google id_token not found.');
        return;
    };

    const response = await fetch("/api/auth/google/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({token: id_token})
    });

    const result = await response.json()
    if (response.ok) {
        window.location.replace('/');
    } else {
        showErrors(result);
        console.error(result);
    }
}

async function showErrors(errors) {
    const errorMessages = new Array();
    if (Array.isArray(errors)) {
        errorMessages = errors;
    } else if (errors.detail) {
        errorMessages.push(errors.detail);
    } else if (errors.title) {
        errorMessages.push(errors.title);
    } else if (errors.status) {
        errorMessages.push(errors.status);
    } else {
        errorMessages.push(errors.toString());
    }

    const errorList = document.querySelector('.gauth.errors');
    errorList.innerHTML = '';
    for (const error of Object.values(errorMessages)) {
        const li = document.createElement('li');
        li.appendChild(document.createTextNode(error));
        errorList.appendChild(li);
    }
    errorList.classList.remove('hidden');
}

window.addEventListener('load', () => {
    gapi.load('auth2', initSignin);
});