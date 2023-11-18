// Fetch the persons from the JSON file
function loadItem() {
  return fetch("../../static/data/item_mock.json")
    .then((response) => response.json())
    .then((json) => json.item);
}

// Creates HTML element from given person
function createElement(item) {
  const btn = document.createElement("button");
  btn.setAttribute("class", "item_card");
  // btn.addEventListener("click", () => (location.href = item.content));
  //   btn.setAttribute("onClick", `location.href = ${item.content}`);

  const img = document.createElement("img");
  img.setAttribute("class", "thumbnail");
  img.setAttribute("src", item.thumbnail);
  img.setAttribute("width", "150px");
  img.setAttribute("heigth", "150px");

  const div = document.createElement("div");
  div.innerText = `${item.name} ${item.price}`;
  const li = document.createElement("li");
  li.setAttribute("class", "item");

  btn.append(img);
  btn.append(div);
  li.append(btn);

  return li;
}

document.addEventListener("DOMContentLoaded", function () {
  let items; // 변수 선언

  loadItem().then((data) => {
    items = data; // 아이템 데이터를 가져옴

    const itemsPerPage = 6;
    const totalPages = Math.ceil(items.length / itemsPerPage);
    let currentPage = 1;

    function showItems(page) {
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;

      items.forEach((item, index) => {
        const listItem = document.getElementById(`item-${index}`); // 각 아이템의 li 요소

        if (index >= startIndex && index < endIndex) {
          listItem.style.display = "block"; // 해당 페이지에 보여져야 하는 아이템 표시
        } else {
          listItem.style.display = "none"; // 그 외 아이템은 숨김
        }
      });
    }

    function updatePagination() {
      const pageNumbers = document.getElementById("page-numbers");
      pageNumbers.innerHTML = "";

      for (let i = 1; i <= totalPages; i++) {
        const pageNumber = document.createElement("span");
        pageNumber.textContent = i;
        if (i === currentPage) {
          pageNumber.classList.add("current-page");
        }

        pageNumber.addEventListener("click", function () {
          currentPage = i;
          showItems(currentPage);
          updatePagination();
        });

        pageNumbers.appendChild(pageNumber);
      }
    }

    function initPagination() {
      const container = document.querySelector(".item-overview");

      items.forEach((item, index) => {
        const li = createElement(item); // 각 아이템에 대한 li 생성
        li.setAttribute("id", `item-${index}`); // 각 li에 고유한 ID 부여
        container.appendChild(li); // 아이템 추가
      });

      showItems(currentPage);
      updatePagination();

      const prevButton = document.getElementById("prev");
      prevButton.addEventListener("click", function () {
        if (currentPage > 1) {
          currentPage--;
          showItems(currentPage);
          updatePagination();
        }
      });

      const nextButton = document.getElementById("next");
      nextButton.addEventListener("click", function () {
        if (currentPage < totalPages) {
          currentPage++;
          showItems(currentPage);
          updatePagination();
        }
      });
    }

    initPagination();
  });
});
