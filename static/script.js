document.querySelectorAll('.dropbtn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent the click from bubbling up

        const dropdownContent = this.nextElementSibling;
        dropdownContent.classList.toggle('show');
        this.classList.toggle('expanded');
    });
});

// Close dropdowns if the user clicks outside of them
window.onclick = function(event) {
    // Check if the click was not on the dropdown button or inside the dropdown content
    if (!event.target.matches('.dropbtn') && !event.target.closest('.dropdown-content')) {
        document.querySelectorAll('.dropdown-content').forEach(content => {
            if (content.classList.contains('show')) {
                content.classList.remove('show');
                content.previousElementSibling.classList.remove('expanded'); // Remove expanded from button
            }
        });
    }
};




function startProcess() {
    // Collecting values
    const threads = document.getElementById('threads').value;
    const headless = document.getElementById('headless1').checked;
    const randomSleep = document.getElementById('random_sleep').value;
    const sleepBeforeQuit = document.getElementById('sleep_before_quit').value;
    const proxyHost = document.getElementById('proxy_host').value;
    const proxyPort = document.getElementById('proxy_port').value;
    const proxyUsername = document.getElementById('proxy_username').value;
    const proxyPassword = document.getElementById('proxy_password').value;
    const ouoLinks = document.getElementById('ouo_links').value;
    const randomLinks = document.getElementById('random_links').value;
    const cleanUp = document.getElementById('cleanup').checked;
    const apiKey = document.getElementById('wit_api_key').value;
    const ouo = document.getElementById('ouo').checked;
    const shrinkme = document.getElementById('shrinkme').checked;

    if (!apiKey || !ouoLinks || !randomLinks || !threads || !proxyHost || !proxyPort || !proxyPassword || !proxyUsername || !ouo && !shrinkme) {
        alert("Please fill in all required fields: that has *");
        return; // Stop the function if validation fails
    }
    const details = document.getElementById('details');
    if (cleanUp){
        details.textContent = "Cleaning before start this may take some time but its good for more threads";
    }
    else {
        details.textContent = "Started successfully";
    }

    
    // Creating an object to send
    const data = {
        threads,
        headless,
        randomSleep,
        sleepBeforeQuit,
        proxyHost,
        proxyPort,
        proxyUsername,
        proxyPassword,
        ouoLinks,
        randomLinks,
        cleanUp,
        apiKey,
        ouo,
        shrinkme
    };
    
    // Sending the data to Flask
    fetch('/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    
    // Storing values in local storage
    localStorage.setItem('threads', threads);
    localStorage.setItem('headless', headless);
    localStorage.setItem('randomSleep', randomSleep);
    localStorage.setItem('sleepBeforeQuit', sleepBeforeQuit);
    localStorage.setItem('proxyHost', proxyHost);
    localStorage.setItem('proxyPort', proxyPort);
    localStorage.setItem('proxyUsername', proxyUsername);
    localStorage.setItem('proxyPassword', proxyPassword);
    localStorage.setItem('ouoLinks',ouoLinks);
    localStorage.setItem('randomLinks',randomLinks);
    localStorage.setItem('cleanUp',cleanUp);
    localStorage.setItem('apiKey',apiKey);
    localStorage.setItem('ouo',ouo);
    localStorage.setItem('shrinkme',shrinkme);
    document.getElementById('start-btn').setAttribute("disabled","disabled");
}


function loadValues() {
    // Loading values from local storage
document.getElementById('threads').value = localStorage.getItem('threads') || '';
document.getElementById('headless1').checked = localStorage.getItem('headless') === 'true';
document.getElementById('random_sleep').value = localStorage.getItem('randomSleep') || '';
document.getElementById('sleep_before_quit').value = localStorage.getItem('sleepBeforeQuit') || '';
document.getElementById('proxy_host').value = localStorage.getItem('proxyHost') || '';
document.getElementById('proxy_port').value = localStorage.getItem('proxyPort') || '';
document.getElementById('proxy_username').value = localStorage.getItem('proxyUsername') || '';
document.getElementById('proxy_password').value = localStorage.getItem('proxyPassword') || '';
document.getElementById('ouo_links').value = localStorage.getItem('ouoLinks') || '';
document.getElementById('random_links').value = localStorage.getItem('randomLinks') || '';
document.getElementById('cleanup').checked = localStorage.getItem('cleanUp') || '';
document.getElementById('wit_api_key').value = localStorage.getItem('apiKey') || '';
document.getElementById('ouo').checked = localStorage.getItem('ouo') || '';
document.getElementById('shrinkme').checked = localStorage.getItem('shrinkme') || '';
}

// Load values when the page is loaded
window.onload = loadValues;

function stopProcess() {
    // Logic to stop the process (if applicable)
    fetch('/stop', {
        method: 'POST'
    })
    const details = document.getElementById('details');
    details.textContent = "Stopping the work";
    document.getElementById('start-btn').disabled = false;
}