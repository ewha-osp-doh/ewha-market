let currentPage = 1;

function renderReviews(pageNumber) {
  // 데이터 가져오기나 AJAX 요청을 통해 리뷰 데이터를 불러온다고 가정합니다.
  // 여기서는 샘플 데이터로 대체합니다.
  const reviews = [
    { title: "첫 번째 리뷰 제목", username: "ew*****님", rating: "★★★★☆", content: "내용 일부..." },
    { title: "두 번째 리뷰 제목", username: "ew*****님", rating: "★★★★★", content: "내용 일부..." },
    { title: "세 번째 리뷰 제목", username: "ew*****님", rating: "★★★☆☆", content: "내용 일부..." }
    // 페이지네이션을 위한 추가 데이터가 있을 것입니다.
  ];

  const container = document.querySelector('.review-container');
  container.innerHTML = ''; // 컨테이너를 비웁니다.

  // 현재 페이지에 해당하는 리뷰를 렌더링합니다.
  reviews.forEach(review => {
    const reviewElement = document.createElement('div');
    reviewElement.classList.add('review-item');
    
    const image = document.createElement('div');
    image.classList.add('review-image');
    // 여기에 image.src = review.imageUrl; 로 이미지 URL을 설정할 수 있습니다.
    
    const content = document.createElement('div');
    content.classList.add('review-content');
    content.innerHTML = `
      <h3>${review.title}</h3>
      <p>${review.username}</p>
      <p>${review.rating}</p>
      <p>${review.content}</p>
    `;
    
    reviewElement.appendChild(image);
    reviewElement.appendChild(content);
    
    container.appendChild(reviewElement);
  });
}

function changePage(increment) {
  currentPage += increment;
  // 페이지 번호를 업데이트하고, 해당 페이지의 리뷰를 렌더링합니다.
  document.getElementById('page-number').textContent = currentPage;
  renderReviews(currentPage);
}

// 초기 페이지 렌더링
renderReviews(currentPage);



// 뒤로가기 버튼 이벤트
document.getElementById('backButton').addEventListener('click', function() {
  // 이 예제에서는 간단히 콘솔에 메시지를 출력합니다만,
  // 실제로는 페이지를 이전 페이지로 이동시키는 로직이 들어가야 합니다.
  console.log('메인페이지로 돌아가기');
  // 예: window.location.href = '메인페이지URL';
});

// 페이지 로드 시 첫 페이지의 리뷰를 렌더링합니다.
renderReviews(currentPage);

