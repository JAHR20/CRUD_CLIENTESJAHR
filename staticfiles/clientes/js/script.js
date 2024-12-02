const header = document.querySelector("header");

window.addEventListener("scroll", function (){
    header.classList.toggle("sticky", this.window.scrollY > 60)
})

/* agregrar un evento click al elemento de clase btn

document.querySelector('.btn').addEventListener("click", function(){
    alert('¡Contactando con desarrollador!')
})

// agregrar un evento click a cada uno de los elementos encontrados de clase .btn
document.querySelectorAll('.btn').forEach(function(button){
    button.addEventListener('click', function(){
        alert('¡Contactando con desarrollador!')
    })
})*/

// funcion para el boton 'pedido'
document.getElementById('btn-pedido').addEventListener('click', function(){
    alert('¡Contactando con desarrollador espere un momento!')
})

// funcion para el boton 'promocion'
document.getElementById('btn-promocion').addEventListener('click', function(){
    alert('¡redirigiendo a la promoción!')
})


document.querySelectorAll('.navbar a[href^="#"]').forEach(function(enlace){
    enlace.addEventListener('click', function(e){
        e.preventDefault();
        // desplazamoeto suave
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        })
    })
})

// cambiar las imagenes de fondo de la sección home

const imagenesJahr = [
    'desarrollojahr.jpg',
    'img/react.jpg',
    'img/swift.jpg',
    'img/angular.jpg',
    'img/R.jpg',
    'img/nodejs.jpg'
];

const homeSection = document.querySelector('.home-JAHR');
const intervalo = 4000;  // 4000 ms = 4s

let indiceImagen = 0;

function cambiarFondoJahr(){
    homeSection.style.backgroundImage = `linear-gradient(45deg, rgb(45, 172, 211, 0.6),
     rgba(161, 40, 237, 0.6)),url(${imagenesJahr[indiceImagen]})`;
     indiceImagen = (indiceImagen + 1) % imagenesJahr.length;
} 

setInterval(cambiarFondoJahr, intervalo)

// Menú para pantallas pequeñas 
let menujahr = document.querySelector('#menu-icon');
let navbarjahr = document.querySelector('.navbar');
let enlacesjahr = document.querySelectorAll('.navbar a');

menujahr.onclick = () => {
    navbarjahr.classList.toggle('open')
    menujahr.classList.toggle('bx-x')
}

enlacesjahr.forEach(link => {
    link.onclick = () => {
        navbarjahr.classList.remove('open')
        menujahr.classList.remove('bx-x')
    }
})



var typed = new Typed('#typed', {
    strings: ['Proyectos escalables','Trabajos de calidad','Contactanos estamos para servirle'],
    typeSpeed: 40,
    loop: "true",
    backSpeed: 20,
});
