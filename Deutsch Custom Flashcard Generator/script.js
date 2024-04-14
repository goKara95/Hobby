let flashcards = [];
let currentCardIndex = 0;

function handleFileSelect() {
    const file = document.getElementById('file-input').files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        const fileContent = event.target.result;
        console.log(fileContent)
        flashcards = parseFlashcards(fileContent);
        if (flashcards.length > 0) {
            renderCard();
        } else {
            alert('Invalid file format. Please upload a text file with correct format.');
        }
    };
    reader.readAsText(file);
}

function parseFlashcards(content) {
    const lines = content.split('\n');
    const flashcards = [];
    lines.forEach(line => {
        const parts = line.trim().split(' ');
        if (parts.length >= 3 && parts[0] === 'W') {
            const type = parts[0];
            const artikel = parts[1];
            const word = parts[2]
            const meaning = parts[3];
            console.log({ type, artikel, word, meaning });
            flashcards.push({ type, artikel, word, meaning });
        }

        else if (parts.length >= 3 && parts[0] === 'V') {
            const type = parts[0];
            const meaning = parts[1];
            const word = parts[6];
            const forms = parts.slice(2).join(' ');
            flashcards.push({type, word, meaning, forms});
        }
        else if (line.trim().length > 0) {
            console.error(`Invalid line format: ${line}`);
        }});
    return flashcards;
}

function renderCard() {
    const card = flashcards[currentCardIndex];
    const frontContent = document.querySelector('.front-content');
    const backContent = document.querySelector('.back-content');
    frontContent.textContent = card.type === 'W' ? card.word : card.word; // Display verb without article on front
    backContent.innerHTML = card.type === 'W' ? `${card.artikel} ${card.word} - ${card.meaning}` :  getVerbForms(card.forms, card.meaning); // Display word with article and meaning on back or verb forms
}

function flipCard(cardElement) {
    cardElement.closest('.card').classList.toggle('is-flipped');
}

function showPrev() {
    currentCardIndex = (currentCardIndex - 1 + flashcards.length) % flashcards.length;
    renderCard();
}

function showNext() {
    currentCardIndex = (currentCardIndex + 1) % flashcards.length;
    renderCard();
}

function getVerbForms(verb, mean) {
    const forms = verb.split(' ');
    return `
        <div>${mean}</div>
        <div>ich ${forms[0]} ${mean}</div>
        <div>du ${forms[1]}</div>
        <div>er/sie/es ${forms[2]}</div>
        <div>wir ${forms[3]}</div>
        <div>ihr ${forms[4]}</div>
        <div>Sie ${forms[5]}</div>
    `;
}
