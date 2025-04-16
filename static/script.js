let categoryCounter = 1;
    let currentCategoryGroup = null;
    let stream = null;

    // Controle do Modal
    const cameraModal = document.getElementById('cameraModal');
    const modalCameraPreview = document.getElementById('modalCameraPreview');
    const modalCaptureButton = document.getElementById('modalCaptureButton');
    const modalCancelButton = document.getElementById('modalCancelButton');
    const modalConfirmButton = document.getElementById('modalConfirmButton');
    const modalCapturedImage = document.getElementById('modalCapturedImage');
    const modalPreviewList = document.getElementById('modalPreviewList');
    // Configuração inicial dos eventos
    document.addEventListener('DOMContentLoaded', () => {
      // Botão "Cancelar"
      modalCancelButton.addEventListener('click', () => {
        closeModal();
      });

      // Outros eventos...
    });
    // Abrir modal da câmera
    function openCameraModal(categoryGroup) {
      currentCategoryGroup = categoryGroup;
      cameraModal.style.display = "block";
      navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(s => {
          stream = s;
          modalCameraPreview.srcObject = stream;
        })
        .catch(() => {
          alert("Não foi possível acessar a câmera.");
          closeModal();
        });
    }

    // Fechar modal
    // Função para fechar o modal
    function closeModal() {
      // Esconde o modal
      cameraModal.style.display = "none";

      // Limpa o ID da categoria atual
      cameraModal.dataset.currentCategoryId = '';

      // Para a transmissão da câmera, se existir
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
      }

      // Remove as pré-visualizações de imagens capturadas
      modalPreviewList.innerHTML = '';

      // Esconde o botão "Confirmar Captura"
      modalConfirmButton.style.display = 'none';
    }

    // Capturar imagem
    modalCaptureButton.addEventListener('click', () => {
      modalCapturedImage.getContext('2d').drawImage(
        modalCameraPreview,
        0, 0,
        modalCapturedImage.width,
        modalCapturedImage.height
      );
      const dataUrl = modalCapturedImage.toDataURL('image/jpeg');
      const img = document.createElement('img');
      img.src = dataUrl;
      img.style.maxHeight = '50px';
      modalPreviewList.appendChild(img);
      modalConfirmButton.style.display = 'inline-block';
    });

    // Confirmar captura
    modalConfirmButton.addEventListener('click', () => {
      const images = Array.from(modalPreviewList.querySelectorAll('img')).map(img => img.src);
      const capturedImagesData = currentCategoryGroup.querySelector('.captured-images-data');
      const capturedImageList = currentCategoryGroup.querySelector('.captured-image-list');
      
      capturedImagesData.value = JSON.stringify(images);
      capturedImageList.innerHTML = images.map(url => `<li><img src="${url}" style="max-width:50px"></li>`).join('');
      closeModal();
    });

    // Adicionar nova categoria
    document.getElementById('addCategory').addEventListener('click', () => {
      const newCategory = document.createElement('div');
      newCategory.className = 'category-group';
      newCategory.dataset.categoryIndex = categoryCounter;
      newCategory.innerHTML = `
        <div class="form-group">
          <label>Livro:</label>
          <input type="text" class="category-name" name="category_name_${categoryCounter}" required>
        </div>
        <div class="form-group">
          <label>Imagens da Livro:</label>
          <input type="file" class="category-images" name="category_images_${categoryCounter}" multiple accept="image/*">
        </div>
        <div class="camera-controls">
          <button type="button" class="capture-button">Capturar Câmera</button>
          <ul class="captured-image-list"></ul>
          <input type="hidden" class="captured-images-data" name="captured_images_${categoryCounter}" value="[]">
        </div>
      `;
      document.getElementById('categories').appendChild(newCategory);
      categoryCounter++;
    });

    // Vincular eventos de captura para todas as categorias
    document.body.addEventListener('click', (e) => {
      if (e.target.classList.contains('capture-button')) {
        const categoryGroup = e.target.closest('.category-group');
        openCameraModal(categoryGroup);
      }
    });

    // Submeter formulário
    document.getElementById('uploadForm').addEventListener('submit', (e) => {
      e.preventDefault();
      document.querySelectorAll('.captured-images-data').forEach(input => {
        const images = Array.from(input.closest('.category-group').querySelectorAll('.captured-image-list img'))
          .map(img => img.src);
        input.value = JSON.stringify(images);
      });
      e.target.submit();
    });