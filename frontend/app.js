const wrapper = document.querySelector(".sliderWrapper");
const menuItems = document.querySelectorAll(".menuItem");

const products = [
    {
        id: 1,
        title: "Refuel Fried Rice Meal",
        price: 1500,
        img: "Images/2-REFUEL-FRIED-RICE-MEAL.jpg",
    },
    {
        id: 2,
        title: "Refuel Spicy Rice Meal",
        price: 1500,
        img: "Images/3-REFUEL-SPICY-RICE-MEAL.jpg",
    },
    {
        id: 3,
        title: "Refuel Max Fried Rice Meal",
        price: 3500,
        img: "Images/7-REFUEL-MAX-FRIED-RICE-MEAL.jpg",
    },
    {
        id: 4,
        title: "Refuel Max Spaghetti",
        price: 3500,
        img: "Images/8-REFUEL-MAX-SPAGHETTI-MEAL.jpg",
    },
    {
        id: 5,
        title: "BBQ Chicken",
        price: 3500,
        img: "Images/BBQ Chicken.jpg",
    },
];

let chosenProduct = products[0];

const currentProductImg = document.querySelector(".productImg");
const currentProductTitle = document.querySelector(".productTitle");
const currentProductPrice = document.querySelector(".productPrice");
const currentProductQuant = document.querySelectorAll(".size");

if (wrapper && menuItems.length > 0 && currentProductImg && currentProductTitle && currentProductPrice) {
    menuItems.forEach((item, index) => {
        item.addEventListener("click", () => {
            wrapper.style.transform = `translateX(${-100 * index}vw)`;
            chosenProduct = products[index];
            currentProductTitle.textContent = chosenProduct.title;
            currentProductPrice.textContent = "N " + chosenProduct.price;
            currentProductImg.src = chosenProduct.img;
        });
    });
}

// currentProductQuant.forEach((size, index) => {
//     size.addEventListener("click", () => {
//       currentProductQuant.forEach((size) => {
//         size.style.backgroundColor = "white";
//         size.style.color = "black";
//       });
//       size.style.backgroundColor = "black";
//       size.style.color = "white";
//     });
//   });
  
if (currentProductQuant.length > 0) {
    currentProductQuant.forEach((size) => {
        size.addEventListener("click", () => {
            currentProductQuant.forEach((value) => {
                value.style.backgroundColor = "white";
                value.style.color = "black";
            });

            size.style.backgroundColor = "black";
            size.style.color = "white";
        });
    });
}

const productButton = document.querySelector(".productButton");
const payment = document.querySelector(".payment");
const close = document.querySelector(".close");

if (productButton && payment && close) {
    productButton.addEventListener("click", () => {
        payment.style.display = "flex";
    });

    close.addEventListener("click", () => {
        payment.style.display = "none";
    });
}