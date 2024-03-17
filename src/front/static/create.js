const input = document.getElementById('header');
const label = document.getElementById('header-label');

input.addEventListener('focus', () => {
    console.log(123);
    label.style.scale = 1.1;
    label.style.color = '#2F80ED';
});

input.addEventListener('blur', () => {
    label.style.scale = 1;
    label.style.color = '#999';
});

const input1 = document.getElementById('text');
const label1 = document.getElementById('text-label');

input1.addEventListener('focus', () => {
    console.log(123);
    label1.style.scale = 1.1;
    label1.style.color = '#2F80ED';
});

input1.addEventListener('blur', () => {
    label1.style.scale = 1;
    label1.style.color = '#999';
});