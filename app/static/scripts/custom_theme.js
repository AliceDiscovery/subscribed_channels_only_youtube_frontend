const updateColorInput = (input, display) => () => {
    display.innerText = input.value;
};

document.querySelectorAll('#custom-theme .color-input')
    .forEach(node => {
        const span = node.querySelector('span');
        const input = node.querySelector('input');
        const onInput = updateColorInput(input, span);
        input.addEventListener('input', onInput);
        onInput() // Fixes issue where input is stored between page reloads.
    });
