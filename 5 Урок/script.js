window.addEventListener('load', () => {
    window.ethereum.enable().then(function(result){
    });
});

window.addEventListener('load', () => {
    if (typeof window.ethereum !== 'undefined') {
        console.log('MetaMask is installed!');
    }
});